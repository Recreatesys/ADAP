{
    "name": "Print Layouts",
    "summary": "Includes all the print layouts for Adap",
    "author": "Lau Siu Hin",
    "version": "1.7",
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
    "installable": True,
    
}
