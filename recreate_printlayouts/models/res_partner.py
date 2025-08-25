from odoo import models, fields

class ResPartner(models.Model):

    _inherit = "res.partner"

    fax_number = fields.Char(string="Fax Number")
    irc_number = fields.Char(string="IRC No.")
    tin_number = fields.Char(string="TIN")

