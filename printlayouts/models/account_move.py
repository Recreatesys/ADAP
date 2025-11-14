from odoo import models, fields, api

class AccountMove(models.Model):

    _inherit = "account.move"

    pi_number = fields.Char(string="P/I No.", store=True, compute="_compute_invoice_origin")
    remarks = fields.Char(string="Remarks", store=True)
    port_of_loading = fields.Char(string="Port of Loading", store=True)
    country_of_origin = fields.Many2one("res.country", string="Country of Origin", store=True)
    net_weight = fields.Float(string="Net Weight", store=True)
    gross_weight = fields.Float(string="Gross Weight", store=True)
    total_value = fields.Char(string="Total Value", store=True)
    trade_term = fields.Char(string="Trade Term", store=True)


    @api.depends("invoice_origin")
    def _compute_invoice_origin(self):
        for order in self:
            order.pi_number = order.invoice_origin


class AccountMoveLine(models.Model):

    _inherit = "account.move.line"

    remarks = fields.Char(string="Remarks", store=True)
    weight = fields.Float(string="Weight", store=True)
    rate = fields.Float(string="Rate", store=True)
    
