# -*- coding: utf-8 -*-


{
    'name': 'HR payroll payment',
    'version': '10.0.0.0.1',
    'category': 'Human Resources',
    'sequence': 82,
    'summary': 'Manage salary payment and connect it to accounting and payroll for advance',
    'author': 'jburckel',
    'depends': ['hr_payroll'],
    'data': [
        'views/hr_payroll_advance_payment_view.xml',
        'data/ir_sequence_data.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
