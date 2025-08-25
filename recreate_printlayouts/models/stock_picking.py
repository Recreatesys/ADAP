from odoo import models, fields, api

class StockPicking(models.Model):

    _inherit = "stock.picking"

    pi_number = fields.Char(string="P/I No.", store=True, compute="_compute_pi_number")
    trade_terms = fields.Char(string="Trade Terms", store=True)
    remarks = fields.Char(string="Remarks", store=True)
    port_of_loading = fields.Char(string="Port of Loading", store=True)
    country_of_origin = fields.Many2one("res.country", string="Country of Origin", store=True)
    pl_number = fields.Char(string="PL No.", store=True)
    shipment_date = fields.Date(string="Shipment Date", store=True)
    name_of_vessel = fields.Char(string="Vessel Name", store=True)
    voyage_number = fields.Char(string="Voyage No.", store=True)
    bill_of_lading_number = fields.Char(string="Bill of Ladding No.", store=True)

    @api.depends("origin")
    def _compute_pi_number(self):
        for order in self:
            order.pi_number = order.origin