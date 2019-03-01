# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class ResCompany(models.Model):
    _inherit = "res.company"
    payment_account = fields.Many2one(comodel_name='account.account', string='Debit account', domain=[('deprecated', '=', False)])
    advance_payment_account = fields.Many2one(comodel_name='account.account', string='Debit account', domain=[('deprecated', '=', False)])


class HRPayrollPaymentConfigSettings(models.TransientModel):
    _name = 'hr.payroll.payment.config.settings'
    _inherit = 'res.config.settings'

    payment_account = fields.Many2one(comodel_name='account.account', related='company_id.payment_account', string='Debit account', domain=[('deprecated', '=', False)])
    advance_payment_account = fields.Many2one(comodel_name='account.account', related='company_id.payment_account', string='Debit account', domain=[('deprecated', '=', False)])
