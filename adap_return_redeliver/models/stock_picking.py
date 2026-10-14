from odoo import _, api, fields, models
from odoo.tools import float_compare


class StockPicking(models.Model):
    _inherit = "stock.picking"

    x_refulfill_origin_id = fields.Many2one(
        "stock.picking",
        string="重新履行来源",
        index=True,
        copy=False,
        help="The original delivery that this transfer re-fulfils after a return.",
    )
    x_refulfill_ids = fields.One2many(
        "stock.picking", "x_refulfill_origin_id", string="重新履行交货"
    )
    x_refulfill_count = fields.Integer(compute="_compute_x_refulfill_count")

    @api.depends("x_refulfill_ids")
    def _compute_x_refulfill_count(self):
        for picking in self:
            picking.x_refulfill_count = len(picking.x_refulfill_ids)

    def button_validate(self):
        res = super().button_validate()
        # Only prompt when fully validated (True), it's a return of a customer
        # delivery, and the order still needs goods.
        if res is True:
            for picking in self:
                order = picking._adap_return_source_order()
                if order and picking._adap_has_outstanding(order):
                    return {
                        "type": "ir.actions.act_window",
                        "name": _("重新生成交货单"),
                        "res_model": "adap.redeliver.confirm",
                        "view_mode": "form",
                        "target": "new",
                        "context": {
                            "default_picking_id": picking.id,
                            "default_sale_order_id": order.id,
                        },
                    }
        return res

    def action_view_refulfill(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("重新履行交货"),
            "res_model": "stock.picking",
            "view_mode": "list,form",
            "domain": [("id", "in", self.x_refulfill_ids.ids)],
            "context": {"create": False},
        }

    def _adap_return_source_order(self):
        """Return the sale order this transfer is a *return* of, else False."""
        self.ensure_one()
        if self.picking_type_id.code != "incoming":
            return False
        if not self.move_ids.filtered(lambda m: m.origin_returned_move_id):
            return False  # not a return
        order = self.sale_id
        if not order:
            order = self.move_ids.mapped(
                "origin_returned_move_id.sale_line_id.order_id"
            )[:1]
        return order or False

    def _adap_has_outstanding(self, order):
        prec = self.env["decimal.precision"].precision_get("Product Unit of Measure")
        for line in order.order_line:
            if line.display_type or line.product_id.type != "consu":
                continue
            if float_compare(
                line.product_uom_qty, line.qty_delivered, precision_digits=prec
            ) > 0:
                return True
        return False

    def _adap_redeliver_sale_outstanding(self, order):
        """Create a delivery for the shortfall and link it back to the original
        delivery (the one this return came from), for the smart button."""
        old_delivery = self.move_ids.mapped("origin_returned_move_id.picking_id")[:1]
        before = set(order.picking_ids.ids)
        order.order_line._action_launch_stock_rule()
        new = order.picking_ids.filtered(
            lambda p: p.id not in before and p.picking_type_id.code == "outgoing"
        )
        if old_delivery and new:
            new.write({"x_refulfill_origin_id": old_delivery.id})
