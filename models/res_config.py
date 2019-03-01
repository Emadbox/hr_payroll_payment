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

    def get_default_params(self, fields):
        res = {}
        res['payment_account'] = self.env['ir.values'].get_default('hr.payroll.payment.config.settings', 'payment_account')
        res['advance_payment_account'] = self.env['ir.values'].get_default('hr.payroll.payment.config.settings', 'advance_payment_account')
        return res

    @api.multi
    def set_payment_account_defaults(self):
        return self.env['ir.values'].sudo().set_default('hr.payroll.payment.config.settings', 'payment_account', self.payment_account.id)

    @api.multi
    def set_advance_payment_account_defaults(self):
        return self.env['ir.values'].sudo().set_default('hr.payroll.payment.config.settings', 'advance_payment_account', self.advance_payment_account.id)
