# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class HRPayrollPaymentConfigSettings(models.TransientModel):
    _name = 'hr.payroll.payment.config.settings'
    _inherit = 'res.config.settings'

    payment_account = fields.Many2one('account.account', 'Debit account', domain=[('deprecated', '=', False)])
    advance_payment_account = fields.Many2one('account.account', 'Debit account', domain=[('deprecated', '=', False)])

    @api.multi
    def set_payment_account(self):
        self.env['ir.config_parameter'].set_param(
            'payment_account', self.payment_account.id)
