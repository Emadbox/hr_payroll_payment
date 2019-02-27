# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from dateutil.relativedelta import relativedelta, MO, SU

from odoo import models, fields, api, exceptions, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class HrPayrollAdvancePayment(models.Model):
    _name = "hr.payroll.advance_payment"
    _description = "Advance payment"
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
            ('cancel', 'Cancelled'),
        ], string='Status', index=True, readonly=True, default='draft',
        track_visibility='onchange', copy=False)
    move_id = fields.Many2one('account.move', string='Journal Entry', readonly=True, index=True,
        ondelete='restrict', copy=False, help="Link to the automatically generated Journal Items.")
    number = fields.Char(related='move_id.name', store=True, readonly=True, copy=False)
    contract_id = fields.Many2one('hr.contract', string='Contract', required=True,
        help="The contract for which applied this input")
    reference = fields.Char(string='Vendor Reference', states={'draft': [('readonly', False)]}
       help="The receipt number or other reference of this advance payment.", readonly=True,
       states={'draft': [('readonly', False)]})
    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
    states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))

    @api.onchange('employee_id')
    def _get_contract(self):
        contracts = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id),('state', '!=', 'closed')])
        if contracts:
            self.contract_id = contracts.ids[0]

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            seq = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('hr.payroll.advance_payment') or _('New')
        else:
            seq = self.env['ir.sequence'].next_by_code('hr.payroll.advance_payment') or _('New')
        vals['name'] = seq
        return super(HrPayrollAdvancePayment, self).create(vals)
