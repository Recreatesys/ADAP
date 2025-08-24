from odoo import models, fields

class StockPicking(models.Model):

    _inherit = "stock.picking"

    pi_number = fields.Char(string="P/I No.", store=True)
    trade_terms = fields.Char(string="Trade Terms", store=True)
    remarks = fields.Char(string="Remarks", store=True)
    port_of_loading = fields.Char(string="Port of Loading", store=True)
    country_of_origin = fields.Many2one("res.country", string="Country of Origin", store=True)
    pl_number = fields.Char(string="PL No.", store=True)