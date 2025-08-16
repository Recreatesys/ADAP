from odoo import models, fields

class AccountMove(models.Model):

    _inherit = "account.move"

    pi_number = fields.Char(string="P/I No.", store=True)
    trade_terms = fields.Char(string="Trade Terms", store=True)
    remarks = fields.Char(string="Remarks", store=True)
    port_of_loading = fields.Char(string="Port of Loading", store=True)
    country_of_origin = fields.Many2one("res.country", string="Country of Origin", store=True)
    net_weight = fields.Float(string="Net Weight", store=True)
    gross_weight = fields.Float(string="Gross Weight", store=True)
    



