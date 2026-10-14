{
    "name": "Return Re-deliver",
    "summary": "After validating a delivery return, ask whether to regenerate a delivery for the order's outstanding quantity",
    "description": """
When a customer-delivery return is validated and the sale order still has an
outstanding (undelivered) quantity, a pop-up asks whether to generate a new
delivery to re-fulfill the order. Answering Yes creates a delivery for the
outstanding quantity via the standard sale procurement rule.
""",
    "author": "ADAP.S",
    "version": "18.0.3.0.0",
    "depends": ["stock", "sale_stock", "printlayouts"],
    "data": [
        "security/ir.model.access.csv",
        "wizards/redeliver_confirm_views.xml",
        "views/stock_picking_views.xml",
    ],
    "license": "LGPL-3",
    "installable": True,
}
