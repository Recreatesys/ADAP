from odoo import models, fields
import logging
from odoo.modules.module import get_module_resource


_logger = logging.getLogger(__name__)

class ProformaInvoiceXlsx(models.AbstractModel):
    _name = 'report.printlayouts.report_adap_proforma_invoice'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, order):
        for obj in order:
            report_name = obj.name
            sheet = workbook.add_worksheet(report_name)

            # Formats
            title_format = workbook.add_format({
                "align": "right",
                "bold": 1,
                "font_size": 24
            })
            company_info_format = workbook.add_format({
                "align": "right",
                "font_size": 11
            })

            main_title_format = workbook.add_format({
                "bold": 1,
                "align": "center",
                "valign": "vcenter",
                "font_size": 22
            })

            document_info_header_format = workbook.add_format({
                "valign": "top",
                "align": "left",
                "font_size": 12,
                "text_wrap": 1,
            })

            document_info_value_format = workbook.add_format({
                "font_size": 13,
            })

            table_header_format = workbook.add_format({
                "font_size": 12,
                "bold": 1,
            })

            table_content_format = workbook.add_format({
                "font_size": 11,
            })

            document_end_content_format = workbook.add_format({
                "font_size": 13
            })

            disclaimer_bloack_area_format = workbook.add_format({
                "font_size": 13,
                "valign": "top",
                "align": "left",
                "text_wrap": 1
            })

            signature_format = workbook.add_format({
                "font_size": 13,
                "bold": 1,
            })

            bottom_border = workbook.add_format({
                "bottom": 1,
            })

             # Company Logo Area
            sheet.insert_image("B3", get_module_resource('printlayouts', 'static/src/img', 'company_logo.png'))

            # Company name / information section
            sheet.set_column("M:N", 13.57)
            sheet.merge_range("I3:N3", "ADAP.S ASIA COMPANY LIMITED", title_format)
            sheet.merge_range("L4:N4", '譽達亞洲有限公司', title_format)
            sheet.merge_range("G5:N5", 'UNIT 2803, 28/F, PROSPERITY PLACE 6SHING YIP STREET, KWUN TONG, KOWLOON, HONG KONG', company_info_format)
            sheet.merge_range("L6:N6", 'Tel: +852 2136 9454 Fax: +852 2137 04444', company_info_format)
            sheet.merge_range("M7:N7", 'Email: info@adapsasia.com', company_info_format)
            
            # Document Title
            sheet.merge_range("F11:I11", "Proforma Invoice", main_title_format)

            #Document Header Info
            customer_address_parts = [
                obj.partner_id.street if obj.partner_id.street else '',
                obj.partner_id.street2 if obj.partner_id.street2 else '',
                obj.partner_id.city if obj.partner_id.city else '',
                f"{obj.partner_id.state_id.name if obj.partner_id.state_id else ''} {obj.partner_id.zip if obj.partner_id.zip else ''}",
                obj.partner_id.country_id.name if obj.partner_id.country_id else ''
            ]
            formatted_customer_address = "\n".join(part for part in customer_address_parts if part)
            sheet.merge_range("B13:G23", str(f"Sold To:\n{formatted_customer_address}\nTaxID: {obj.partner_id.vat if obj.partner_id.vat else ''}\nFax: {obj.partner_id.x_studio_char_field_1ci_1j35oraga if obj.partner_id.x_studio_char_field_1ci_1j35oraga else ''}\nTel: {obj.partner_id.phone if obj.partner_id.phone else ''}"), document_info_header_format)

            delivery_address_parts = [
                obj.partner_shipping_id.street if obj.partner_shipping_id.street else '',
                obj.partner_shipping_id.street2 if obj.partner_shipping_id.street2 else '',
                obj.partner_shipping_id.city if obj.partner_shipping_id.city else '',
                f"{obj.partner_shipping_id.state_id.name if obj.partner_shipping_id.state_id else ''} {obj.partner_shipping_id.zip if obj.partner_shipping_id.zip else ''}",
                obj.partner_shipping_id.country_id.name if obj.partner_shipping_id.country_id else ''
            ]

            formatted_delivery_address = "\n".join(part for part in delivery_address_parts if part)
            sheet.merge_range("I13:N23", str(f"Ship To:\n{formatted_delivery_address}\nTaxID: {obj.partner_shipping_id.vat if obj.partner_shipping_id.vat else ''}\nFax: {obj.partner_shipping_id.x_studio_char_field_1ci_1j35oraga if obj.partner_shipping_id.x_studio_char_field_1ci_1j35oraga else ''}\nTel: {obj.partner_shipping_id.phone if obj.partner_shipping_id.phone else ''}"), document_info_header_format)

            sheet.write("B26", str(f"Need By: {obj.commitment_date if obj.commitment_date else''}"), document_info_value_format)
            po_origin = obj._get_purchase_orders()
            po_origin_ls = []
            for id in po_origin.ids:
                record = self.env["purchase.order"].browse(id)
                po_origin_ls.append(record.name)
            sheet.write("G26", f"PO Number: {', '.join(po_origin_ls)}", document_info_value_format)
            sheet.write("K26", str(f"Inco-Term: {obj.incoterm.name if obj.incoterm else ''}"), document_info_value_format)
            sheet.write("B28", str(f"Terms: {obj.payment_term_id.name if obj.payment_term_id else ''}"), document_info_value_format)
            sheet.write("G28", str(f"Sales Person: {obj.user_id.name if obj.user_id else ''}"), document_info_value_format)
            sheet.write("K28", str(f"Ship Via: {obj.shipping_method if obj.shipping_method else ''}"), document_info_value_format)

            # Table header
            sheet.write("B31", "Line", table_header_format)
            sheet.write("D31", "Part Number/Description", table_header_format)
            sheet.write("H31", "Order Qty", table_header_format)
            sheet.write("K31", "Unit Price", table_header_format)
            sheet.write("N31", "Amount", table_header_format)

            # Table content
            row, cnt = 32, 1
            for line in obj.order_line:
                sheet.write(row, 1, cnt, table_content_format)
                sheet.write(row, 3, line.name, table_content_format)
                sheet.write(row, 7, line.product_uom_qty, table_content_format)
                sheet.write(row, 10, line.price_unit, table_content_format)
                sheet.write(row, 13, line.price_subtotal, table_content_format)
                row += 2
                cnt += 1
            
            # Document end content
            row += 3
            sheet.write(row, 1, str(f"Inco-term: {obj.incoterm.name if obj.incoterm else ''}"), document_end_content_format)
            row += 1
            sheet.write(row, 1, str(f"Loading Port: {obj.loading_port if obj.loading_port else ''}"), document_end_content_format)
            row += 1
            sheet.write(row, 1, str(f"Country of Origin: {obj.country_of_origin.name if obj.country_of_origin else ''}"), document_end_content_format)
            row += 1
            sheet.write(row, 1, str(f"Payment term: {obj.payment_term_id.name if obj.payment_term_id else ''}"), document_end_content_format)
            
            # Document end fixed information
            row += 2
            sheet.write(row, 1, "Our bank account details", document_end_content_format)
            row += 1
            sheet.write(row, 1, "Beneficiary: ADAP.S ASIA COMPANY LIMITED", document_end_content_format)
            row += 1
            sheet.write(row, 1, "A/C No.: 112-324504-838", document_end_content_format)
            row += 1
            sheet.write(row, 1, "Bank: HSBC", document_end_content_format)
            row += 1
            sheet.write(row, 1, "Branch: 1 Queen's Road Central, Hong Kong", document_end_content_format)
            row += 1
            sheet.write(row, 1, "SWIFT: HSBCHKHHHKH", document_end_content_format)
            row += 2
            sheet.write(row, 1, "Disclaimer:", document_end_content_format)
            row += 1
            merge_range_string = str(f"B{row}:N{row+3}")
            sheet.merge_range(merge_range_string, "We have used reasonable effort to make prompt shipment and provide shipment schedule in advance" \
            ". However delivery scehdules are estimated and subject to change by third parties. We will not guarantee the accuracy of any delivery scehdule." \
            "Also we will not bear any loss incurred by change of schedule.", disclaimer_bloack_area_format)

            # Signature area 
            row += 12
            sheet.write(row, 1, "Issued By:", signature_format)
            sheet.write(row, 6, "Approved By:", signature_format)
            sheet.write(row, 11, "Confirmed By:", signature_format)

            row += 5
            for col in range(1, 4):
                sheet.write(row, col, None, bottom_border)

            for col in range(6, 10):
                sheet.write(row, col, None, bottom_border)
            
            for col in range(11, 15):
                sheet.write(row, col, None, bottom_border)