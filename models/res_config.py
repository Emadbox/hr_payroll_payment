# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

PARAMS = [
    ("payment_account", "hr.payroll.payment.config.settings.payment_account"),
    ("advance_payment_account", "hr.payroll.payment.config.settings.advance_payment_account")
]


class HRPayrollPaymentConfigSettings(models.TransientModel):
    _name = 'hr.payroll.payment.config.settings'
    _inherit = 'res.config.settings'

    payment_account = fields.Many2one('account.account', 'Debit account', domain=[('deprecated', '=', False)])
    advance_payment_account = fields.Many2one('account.account', 'Debit account', domain=[('deprecated', '=', False)])

    @api.multi
    def set_params(self):
        self.ensure_one()

        for field_name, key_name in PARAMS:
            value = getattr(self, field_name, '').strip()
            self.env['ir.config_parameter'].set_param(key_name, value)

    def get_default_params(self, cr, uid, fields, context=None):
        res = {}
        for field_name, key_name in PARAMS:
            res[field_name] = self.env['ir.config_parameter'].get_param(key_name, '').strip()
        return res
