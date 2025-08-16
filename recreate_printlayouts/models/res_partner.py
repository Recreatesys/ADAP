from odoo import models, fields

class ResPartner(models.Model):

    _inherit = "res.partner"

    fax_number = fields.Char(string="Fax Number")

