# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import Warning, UserError
import logging,requests,datetime,hashlib,sys
import json
import logging
BUDGET_STATE = [
    ('draft', 'New'),
        ('dept_confirm', 'Waiting Department Approval'),
        ('ir_approve', 'Waiting IR Approval'),
        ('approve', 'Approved'),
        ('cancel', 'Cancelled'),
        ('reject', 'Rejected'),
]


class budget_project(models.Model):
    _name = 'budget.project'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _description = 'Budget Module'

    name = fields.Char(string="Number", index=True, readonly=True)

    employee_id = fields.Many2one("hr.employee", string="Department Lead")

    department_id = fields.Many2one("hr.department", string="Department Name")

    amount = fields.Float(string="Budget Amount")

    balance = fields.Float(string="Budget Balance")

    start_date = fields.Date(string="Start Date")

    end_date = fields.Date(string="Start Date")

    notes = fields.Text(string="Notes")

    state = fields.Selection(
        selection=BUDGET_STATE,
        string="Status",
        readonly=True, copy=False, index=True,
        tracking=3,
        default='draft')

    confirm_date = fields.Date(
        string='Confirmed Date',
        readonly=True,
        copy=False,
    )

    request_date = fields.Date(
        string='Requisition Date',
        default=fields.Date.today(),
        required=True,
    )

    employee_confirm_id = fields.Many2one(
        'hr.employee',
        string='Confirmed by',
        readonly=True,
        copy=False,
    )

    date_done = fields.Date(
        string='Date Done', 
        readonly=True, 
        help='Date of Completion of Purchase Requisition',
    )
    managerapp_date = fields.Date(
        string='Department Approval Date',
        readonly=True,
        copy=False,
    )
    manareject_date = fields.Date(
        string='Department Manager Reject Date',
        readonly=True,
    )
    userreject_date = fields.Date(
        string='Rejected Date',
        readonly=True,
        copy=False,
    )
    userrapp_date = fields.Date(
        string='Approved Date',
        readonly=True,
        copy=False,
    )

    approve_manager_id = fields.Many2one(
        'hr.employee',
        string='Department Manager',
        readonly=True,
        copy=False,
    )
    reject_manager_id = fields.Many2one(
        'hr.employee',
        string='Department Manager Reject',
        readonly=True,
    )
    approve_employee_id = fields.Many2one(
        'hr.employee',
        string='Approved by',
        readonly=True,
        copy=False,
    )
    reject_employee_id = fields.Many2one(
        'hr.employee',
        string='Rejected by',
        readonly=True,
        copy=False,
    )

    def requisition_confirm(self):
        for rec in self:
            manager_mail_template = self.env.ref('budget_project.email_confirm_budget')
            rec.employee_confirm_id = rec.employee_id.id
            rec.confirm_date = fields.Date.today()
            rec.state = 'dept_confirm'
            if manager_mail_template:
                manager_mail_template.send_mail(self.id)
            
    #@api.multi
    def requisition_reject(self):
        for rec in self:
            rec.state = 'reject'
            rec.reject_employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            rec.userreject_date = fields.Date.today()

    #@api.multi
    def manager_approve(self):
        for rec in self:
            rec.managerapp_date = fields.Date.today()
            rec.approve_manager_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            employee_mail_template = self.env.ref('budget_project.email_budget_project_iruser_custom')
            email_iruser_template = self.env.ref('budget_project.email_budget_project')
            employee_mail_template.sudo().send_mail(self.id)
            email_iruser_template.sudo().send_mail(self.id)
            rec.state = 'ir_approve'

    #@api.multi
    def user_approve(self):
        for rec in self:
            rec.userrapp_date = fields.Date.today()
            rec.approve_employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
            rec.state = 'approve'
    #@api.multi
    def reset_draft(self):
        for rec in self:
            rec.state = 'draft'
    
    #@api.multi
    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'
    
    @api.model
    def create(self, vals):
        name = self.env['ir.sequence'].next_by_code('budget.project.form.seq')
        vals.update({
            'name': name
            })
        res = super(budget_project, self).create(vals)
        return res
    

class budget_expenses(models.Model):
    _inherit = 'hr.expense.sheet'

    budget_id = fields.Many2one("budget.project", string="Budget", required=True,)

    def action_approve_expense_sheets(self):
        request_bugdet_validation = self.env['budget.project'].search([('id','=',self.budget_id.id)],order="id desc",limit=1)

        if request_bugdet_validation.balance > 0:
            pass
            
        else:

            raise UserError(_('You do not have allocations in your budget'))
            
        self._check_can_approve()
        self._validate_analytic_distribution()
        duplicates = self.expense_line_ids.duplicate_expense_ids.filtered(lambda exp: exp.state in {'approved', 'done'})
        if duplicates:
            action = self.env["ir.actions.act_window"]._for_xml_id('hr_expense.hr_expense_approve_duplicate_action')
            action['context'] = {'default_sheet_ids': self.ids, 'default_expense_ids': duplicates.ids}
            return action
        self._do_approve()
