from odoo import fields, models


class AdapRedeliverConfirm(models.TransientModel):
    _name = "adap.redeliver.confirm"
    _description = "Re-deliver confirmation after a return"

    picking_id = fields.Many2one("stock.picking", string="Return")
    sale_order_id = fields.Many2one("sale.order", string="Sale Order")

    def action_yes(self):
        self.ensure_one()
        if self.picking_id and self.sale_order_id:
            self.picking_id._adap_redeliver_sale_outstanding(self.sale_order_id)
        return {"type": "ir.actions.act_window_close"}

    def action_no(self):
        return {"type": "ir.actions.act_window_close"}
