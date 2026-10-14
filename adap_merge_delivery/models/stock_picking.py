from odoo import _, models
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def action_adap_merge_deliveries(self):
        """Combine the selected open delivery orders (same customer) into one new
        delivery order with quantities pre-filled to the ordered amount, cancel the
        emptied originals, and open the new delivery for the user to validate/print."""
        pickings = self.filtered(lambda p: p.state not in ("done", "cancel"))
        if len(pickings) < 2:
            raise UserError(_("请选择至少两张未完成的交货单进行合并。\n"
                              "Select at least two open delivery orders to combine."))
        if any(p.picking_type_id.code != "outgoing" for p in pickings):
            raise UserError(_("只能合并交货单（出库）。\nOnly outgoing deliveries can be combined."))
        if len(pickings.mapped("picking_type_id")) != 1:
            raise UserError(_("只能合并相同作业类型的交货单。\n"
                              "Selected deliveries must share the same operation type."))
        if len(pickings.mapped("partner_id.commercial_partner_id")) != 1:
            raise UserError(_("只能合并同一客户的交货单。\n"
                              "Only delivery orders of the same customer can be combined."))

        pickings = pickings.sorted("id")
        first = pickings[0]
        combined = self.env["stock.picking"].create({
            "picking_type_id": first.picking_type_id.id,
            "partner_id": first.partner_id.id,
            "location_id": first.location_id.id,
            "location_dest_id": first.location_dest_id.id,
            "origin": ", ".join(pickings.mapped("name")),
            "company_id": first.company_id.id,
            "move_type": first.move_type,
        })

        # Move every open move onto the combined delivery (keeps sale line links,
        # reservations and demand), then cancel the now-empty source deliveries.
        moves = pickings.move_ids.filtered(lambda m: m.state not in ("done", "cancel"))
        moves.write({"picking_id": combined.id})
        for p in pickings:
            if not p.move_ids.filtered(lambda m: m.state not in ("done", "cancel")):
                p.action_cancel()
                p.message_post(body=_("已合并至 / Merged into %s", combined.name))

        combined.message_post(
            body=_("由以下交货单合并而成 / Combined from: %s", ", ".join(pickings.mapped("name")))
        )

        # Pre-fill the quantity to ship with the ordered quantity (not zero), so the
        # user can review and validate directly.
        for m in combined.move_ids:
            m.quantity = m.product_uom_qty
            m.picked = True

        return {
            "type": "ir.actions.act_window",
            "name": _("合并交货单 Combined Delivery"),
            "res_model": "stock.picking",
            "res_id": combined.id,
            "view_mode": "form",
            "views": [[False, "form"]],
        }
