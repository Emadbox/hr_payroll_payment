# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class HRPayrollPaymentConfigSettings(models.TransientModel):
    _name = 'hr.payroll.payment.config.settings'
    _inherit = 'res.config.settings'

    payment_account = fields.Many2one('account.account', string='Debit account', domain=[('deprecated', '=', False)])
    advance_payment_account = fields.Many2one('account.account', string='Debit account', domain=[('deprecated', '=', False)])

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            payment_account=self.env['ir.config_parameter'].sudo().get_param('hr.payroll.payment.payment_account')
            advance_payment_account=self.env['ir.config_parameter'].sudo().get_param('hr.payroll.payment.advance_payment_account')
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('hr.payroll.payment', self.payment_account)
        self.env['ir.config_parameter'].sudo().set_param('hr.payroll.payment', self.advance_payment_account)
