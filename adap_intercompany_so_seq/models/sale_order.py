from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # Set when the source A purchase order's remark changes AFTER this B SO was
    # created (so the user is warned the production remark was updated).
    x_po_remark_updated = fields.Boolean(
        string="惠州譽達备注已更新",
        copy=False,
        default=False,
    )
    x_po_remark_warn = fields.Char(compute="_compute_x_po_remark_warn")

    @api.depends("x_po_remark_updated")
    def _compute_x_po_remark_warn(self):
        for so in self:
            so.x_po_remark_warn = "⚠️" if so.x_po_remark_updated else ""

    def action_adap_ack_po_remark(self):
        """Acknowledge / clear the 'remark updated' warning."""
        self.write({"x_po_remark_updated": False})
