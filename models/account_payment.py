#-*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class account_payment(models.Model):
    _inherit = "account.payment"

    employee_payment_account = fields.Many2one('account.account', readonly=True)

    @api.one
    @api.depends('invoice_ids', 'payment_type', 'partner_type', 'partner_id')
    def _compute_destination_account_id(self):
        super(account_payment, self)._compute_destination_account_id(self)
        if self.employee_payment_account:
            self.destination_account_id = self.env['hr.payroll.payment.config.settings'].employee_payment_account.id
