from odoo import models, fields


class StockMove(models.Model):

    _inherit = "stock.move"

    cartons = fields.Integer(string="Cartons", store=True)
    net_weight = fields.Float(string="Net Weight", store=True)
    gross_weight = fields.Float(string="Gross Weight", store=True)
    