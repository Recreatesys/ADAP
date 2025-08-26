from odoo import models, fields

class SaleOrder(models.Model):

    _inherit = "sale.order"

    lc_number = fields.Char(string="LC No", store=True)
    lc_issue_date = fields.Date(string="Issue Date", store=True)
    shipping_method = fields.Char(string="Shipping Method", store=True)
    loading_port = fields.Char(string="Loading Port", store=True)
    country_of_origin = fields.Many2one(comodel_name="res.country", string="Country of Origin", store=True)
