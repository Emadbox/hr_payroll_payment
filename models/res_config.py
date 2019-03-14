# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api

PARAMS = [
    ("payment_account", "hr.payroll.payment.config.settings.payment_account"),
    ("advance_payment_account", "hr.payroll.payment.config.settings.advance_payment_account"),
]

class HRPayrollPaymentConfigSettings(models.TransientModel):
    _name = 'hr.payroll.payment.config.settings'
    _inherit = 'res.config.settings'

    company_id = fields.Many2one('res.company', string='Company', required=True,
        default=lambda self: self.env.user.company_id)

    salary_payment_account_id = fields.Many2one(related='company_id.salary_payment_account_id', string='Debit account for payment', domain=[('deprecated', '=', False)])
    advance_salary_payment_account_id = fields.Many2one(related='company_id.advance_salary_payment_account_id', string='Debit account for advance', domain=[('deprecated', '=', False)])
