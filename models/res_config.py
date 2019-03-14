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

    payment_account = fields.Many2one(comodel_name='account.account', string='Debit account for payment', domain=[('deprecated', '=', False)])
    advance_payment_account = fields.Many2one(comodel_name='account.account', string='Debit account for advance', domain=[('deprecated', '=', False)])

    @api.multi
    def set_params(self):
        self.ensure_one()

        for field_name, key_name in PARAMS:
            value = getattr(self, field_name, '').id
            self.env['ir.config_parameter'].set_param(key_name, value)

    @api.model
    def get_default_params(self, fields):
        company = self.env.user.company_id
        return {
            'payment_account': company.salary_payment_account_id
            'advance_payment_account': company.advance_salary_payment_account_id
        }
