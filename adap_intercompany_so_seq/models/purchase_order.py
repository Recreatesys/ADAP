import re

from odoo import models

# Fixed company ids for this database group (A=1, B=2, C=3).
COMPANY_B = 2
COMPANY_C = 3


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _prepare_sale_order_data(self, name, partner, company, direct_delivery_address):
        # `company` is the TARGET company the inter-company SO is created in;
        # `self` is the source purchase order.
        vals = super()._prepare_sale_order_data(
            name, partner, company, direct_delivery_address
        )
        if company.id == COMPANY_B:
            # B-惠州譽達 SO created from an A purchase order -> mirror A's number.
            bname = self._adap_b_mirror_name()
            if bname:
                vals["name"] = bname
        elif company.id == COMPANY_C:
            # C-鼎盛電鍍 SO created from a B purchase order -> own C sequence.
            cname = self.env["ir.sequence"].sudo().next_by_code("adap.sale.order.c")
            if cname:
                vals["name"] = cname
        return vals

    def _adap_b_mirror_name(self):
        """B<digits> derived from the source A sale order in this PO's origin."""
        self.ensure_one()
        m = re.match(r"^\s*S(\d+)", self.origin or "")
        if not m:
            return False  # unresolvable -> keep the intercompany default name
        base = "B" + m.group(1)
        name, n = base, 2
        SO = self.env["sale.order"].sudo()
        while SO.search_count([("company_id", "=", COMPANY_B), ("name", "=", name)]):
            name, n = "%s-%d" % (base, n), n + 1
        return name
