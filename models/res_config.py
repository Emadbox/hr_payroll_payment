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

    payment_account = fields.Many2one(comodel_name='account.account', string='Debit account', domain=[('deprecated', '=', False)])
    advance_payment_account = fields.Many2one(comodel_name='account.account', string='Debit account', domain=[('deprecated', '=', False)])

    @api.multi
    def set_params(self):
        self.ensure_one()

        for field_name, key_name in PARAMS:
            value = getattr(self, field_name, '').id
            self.env['ir.config_parameter'].set_param(key_name, value)

    @api.multi
    def get_default_params(self):
        res = {}
        for field_name, key_name in PARAMS:
            value = self.env['ir.config_parameter'].get_param(key_name, '').strip()
            if value:
                res[field_name] = int(value)
        return res
