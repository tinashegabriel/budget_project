# -*- coding: utf-8 -*-
{
    'name': "budget_project",

    'summary': "Budgetting module to capture",

    'description': """
Budgetting module to capture
    """,

    'author': "Infinity Lines Of Code",
    'website': "https://iloc.co.zw",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','hr_expense','hr'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/seq.xml',
        'data/budget_approval.xml',
        'data/budget_project_approval.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

