# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from dateutil.relativedelta import relativedelta, MO, SU

from odoo import models, fields, api, exceptions, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class HrPayrollPayment(models.Model):
    _name = "hr.payroll.payment"
    _description = "Payroll payment"
    _order = "payment_date desc"

    employee_id = fields.Many2one('hr.employee', string="Employee", required=True, ondelete='cascade', index=True)
    department_id = fields.Many2one('hr.department', string="Department", related="employee_id.department_id",
        readonly=True)
    payment_date = fields.Date(string="Payment date")
    amount = fields.Monetary(string="Payment amount", required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
        default=lambda self: self.env.user.company_id.currency_id)
    communication = fields.Char(string='Memo')
    journal_id = fields.Many2one('account.journal', string='Payment Journal',
        required=True, domain=[('type', 'in', ('bank', 'cash'))])
    company_id = fields.Many2one('res.company', related='journal_id.company_id', string='Company', readonly=True)
    state = fields.Selection([
            ('draft','Unposted'),
            ('posted', 'Posted'),
            ('deducted', 'Deducted'),
            ('cancel', 'Cancelled'),
        ], string='Status',track_visibility='onchange', index=True, readonly=True, default='draft', copy=False)
    payment_id = fields.Many2one('account.payment', string='Journal Entry', readonly=True, index=True,
        ondelete='restrict', copy=False, help="Link to the automatically generated Payment in accounting.")
    number = fields.Char(related='move_id.name', store=True, readonly=True, copy=False)
    contract_id = fields.Many2one('hr.contract', string='Contract', required=True,
        help="The contract for which applied this input")
    reference = fields.Char(string='Reference',readonly=True, states={'draft': [('readonly', False)]},
       help="The receipt number or other reference of this payment.")
    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
    states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    payment_type = fields.Selection([
    ('normal_payment', 'Normal payment'),
    ('advance_payment', 'Advance salary payment'),
    ], string='Payment type', default='normal_payment')
    percentage_by_payslip = fields.Float(string='Percentage by payslip', help="For advance payment, you can indicate the percentage of the payment you would like to deduct on payslip", default=100)

    @api.onchange('employee_id')
    def _get_contract(self):
        contracts = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id),('state', '!=', 'closed')])
        if contracts:
            self.contract_id = contracts.ids[0]

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            seq = self.env['ir.sequence'].next_by_code('hr.payroll.payment') or _('New')
        vals['name'] = seq
        return super(HrPayrollPayment, self).create(vals)

    @api.multi
    def post_payment(self):
        for pay in self:
            payment_vals = {
                'amount': pay.amount,
                'payment_date': pay.payment_date,
                'communication': pay.communication,
                'partner_id': self.partner_id.id,
                'partner_type': 'customer',
                'journal_id': pay.journal_id,
                'payment_type': 'outbound',
                'payment_method_id': self.env.ref('account.account_payment_method_manual_out').id
            }

            payment = self.env['account.payment'].create(payment_vals)
            payment.post()
            pay.write('payment_id': payment.id)
        return self.write({'state': 'posted'})

    @api.multi
    def cancel_payment(self):
        return self.write({'state': 'cancel'})
