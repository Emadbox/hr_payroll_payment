# -*- coding: utf-8 -*-


{
    'name': 'HR payroll advance payment',
    'version': '10.0.0.0.1',
    'category': 'Human Resources',
    'sequence': 82,
    'summary': 'Manage salary advance payment and connect it to accounting and payroll',
    'author': 'jburckel',
    'depends': ['hr_payroll'],
    'data': [
        'views/hr_paroll_advance_payment_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
