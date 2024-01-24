# -*- coding: utf-8 -*-
# from odoo import http


# class BudgetProject(http.Controller):
#     @http.route('/budget_project/budget_project', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/budget_project/budget_project/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('budget_project.listing', {
#             'root': '/budget_project/budget_project',
#             'objects': http.request.env['budget_project.budget_project'].search([]),
#         })

#     @http.route('/budget_project/budget_project/objects/<model("budget_project.budget_project"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('budget_project.object', {
#             'object': obj
#         })

