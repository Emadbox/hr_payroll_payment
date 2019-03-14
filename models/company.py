#-*- coding:utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class ResCompany(models.Model):
    _inherit = "res.company"

    salary_payment_account_id = fields.Many2one('account.account', string="Account for salary payment")
    advance_salary_payment_account_id = fields.Many2one('account.account', string="Account for advance salary payment")
