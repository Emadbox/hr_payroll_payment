# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class HRPayrollPaymentConfigSettings(models.TransientModel):
    _inherit = 'base.config.settings'

    payment_account = fields.Many2one('account.account', 'Debit Account', domain=[('deprecated', '=', False)])
    advance_payment_account = fields.Many2one('account.account', 'Debit Account', domain=[('deprecated', '=', False)])
