{
    "name": "Inter-company SO Numbering (B mirror / C prefix)",
    "summary": "Inter-company sale orders: B-惠州譽達 mirrors the source A number (B<digits>); C-鼎盛電鍍 uses its own C sequence",
    "description": """
When the intercompany rules auto-create a sale order:
* in company B (惠州譽達) from an A purchase order, name it B + the A order's
  digits (A's S00645 -> B00645);
* in company C (鼎盛電鍍) from a B purchase order, name it from a dedicated C
  sequence (C00001...).

Company A keeps its S sequence. Company/partner ids are fixed for this database
group: A=1, B=2, C=3.
""",
    "author": "ADAP.S",
    "version": "18.0.2.0.0",
    "depends": ["sale_purchase_inter_company_rules"],
    "data": [
        "data/sequence.xml",
    ],
    "license": "LGPL-3",
    "installable": True,
}
