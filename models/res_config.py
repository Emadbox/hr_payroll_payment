# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class HRPayrollPaymentConfigSettings(models.TransientModel):
    _name = 'hr.payroll.payment.config.settings'
    _inherit = 'res.config.settings'

    payment_account = fields.Many2one('account.account', 'Debit account', domain=[('deprecated', '=', False)])
    advance_payment_account = fields.Many2one('account.account', 'Debit account', domain=[('deprecated', '=', False)])

    @api.model
    def get_values(self):
        res = super(HRPayrollPaymentConfigSettings, self).get_values()
        payment_account = self.env['ir.config_parameter'].sudo().get_param(
            'payment_account',
            default=None
        )
        advance_payment_account = self.env['ir.config_parameter'].sudo().get_param(
            'advance_payment_account',
            default=None
        )
        res.update(payment_account=payment_account)
        res.update(advance_payment_account=advance_payment_account)
        return res

    @api.multi
    def set_values(self):
        super(HRPayrollPaymentConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'payment_account', self.payment_account
        )
        self.env['ir.config_parameter'].sudo().set_param(
            'advance_payment_account', self.advance_payment_account
        )
