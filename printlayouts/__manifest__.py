{
    "name": "Print Layouts",
    "summary": "Includes all the print layouts for Adap",
    "author": "Lau Siu Hin",
    "version": "1.8",
    "depends": ['base', 'account', 'contacts', "sale", "sale_pdf_quote_builder"],
    "data": [
        "security/ir.model.access.csv",
        "reports/reports.xml",
        "reports/proforma_invoice_inherit.xml",
        "reports/delivery_note.xml",
        "wizards/customer_monthly_statements_wizard.xml",
        "wizards/adap_monthly_statement_wizard_view.xml",
        "views/account_menuitems.xml",
        "views/account_move_view.xml",
        "views/res_partner_view.xml",
        "views/stock_move_line_view.xml",
        "views/stock_picking_view.xml",
        "views/sale_order_view.xml",
        "views/stock_picking_dn_cols.xml",
    ],
    # Repoints the user-menu "Documentation/文档" link to the local operations
    # manual (served from static/src/manual/). Also activated at runtime via an
    # ir.asset record on both databases, so it works without a module upgrade.
    "assets": {
        "web.assets_backend": [
            "printlayouts/static/src/js/user_menu_doc.js",
        ],
    },
    "installable": True,
    
}
