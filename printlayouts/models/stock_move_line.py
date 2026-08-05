from odoo import models, fields


class StockMove(models.Model):

    _inherit = "stock.move"

    cartons = fields.Integer(string="Cartons", store=True)
    # Labels shown on the transfer. zh_CN/zh_TW translations (每箱净重/每箱毛重)
    # are applied at runtime on ir.model.fields (see deploy notes).
    net_weight = fields.Float(string="Net Weight/Box", store=True)
    gross_weight = fields.Float(string="Gross Weight/Box", store=True)
    