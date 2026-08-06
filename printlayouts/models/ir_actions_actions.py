from odoo import models


class IrActionsActions(models.Model):
    _inherit = "ir.actions.actions"

    def get_bindings(self, model_name):
        """Hide the 鼎盛出库单 report from the stock.picking Print menu unless the
        user's active company is 鼎盛 (C). Odoo's report bindings can only be
        filtered by security group natively, so we post-filter get_bindings by
        the active company here."""
        result = super().get_bindings(model_name)
        if model_name == "stock.picking" and result.get("report"):
            ds = self.env.ref(
                "printlayouts.report_adap_delivery_out_ds", raise_if_not_found=False
            )
            if ds:
                company_c = self.env["res.company"].search(
                    [("name", "ilike", "鼎盛")], limit=1
                )
                if self.env.company != company_c:
                    reports = [a for a in result["report"] if a.get("id") != ds.id]
                    result = dict(result, report=reports)
        return result
