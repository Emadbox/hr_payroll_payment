# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class HRPayrollPaymentConfigSettings(models.TransientModel):
    _name = 'hr.payroll.payment.config.settings'
    _inherit = 'res.config.settings'

    payment_account = fields.Many2one('account.account', 'Debit account', domain=[('deprecated', '=', False)])
    advance_payment_account = fields.Many2one('account.account', 'Debit account', domain=[('deprecated', '=', False)])

    @api.multi
    def execute(self):
         values = {}
         res = super(HRPayrollPaymentConfigSettings, self).execute()
         values['payment_account'] = self.payment_account
         res.update({'payment_account': values['payment_account'] or False})

         return res
