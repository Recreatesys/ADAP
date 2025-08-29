from odoo import models, fields
import logging
from odoo.modules.module import get_module_resource
from datetime import datetime


_logger = logging.getLogger(__name__)

class ShippingAdviseXlsx(models.AbstractModel):
    _name = 'report.recreate_printlayouts.report_adap_shipping_advise'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, picking):
        for obj in picking:
            report_name = f'{obj.name} - Shipping Adivce'
            sheet = workbook.add_worksheet(report_name)

             # Formats
            title_format = workbook.add_format({
                "align": "center",
                "bold": 1,
                "font_size": 20
            })

            header_format = workbook.add_format({
                "font_size": 14
            })

            addresses_block_format = workbook.add_format({
                "font_size": 14,
                "text_wrap": 1,
                "valign": "top",
            })

            header_attn_format = workbook.add_format({
                "font_size": 14,
                "bold": 1
            })

            bottom_border = workbook.add_format({
                "bottom": 1,
            })

            top_border = workbook.add_format({
                "top": 1,
            })

            table_header_format = workbook.add_format({
                "bold": 1,
                "font_size": 12
            })

            main_content_format = workbook.add_format({
                "font_size": 13,
            })

            main_content_bold_format = workbook.add_format({
                "font_size": 13,
                "bold": 1,
            })

            document_end_format = workbook.add_format({
                "font_size": 12
            })

            signature_section_format = workbook.add_format({
                "font_size": 12,
                "top": 1,
            })

            shipment_content_label = workbook.add_format({
                "font_size": 14,
                "bold": 1,
                "bottom": 1
            })

            last_company_name_format = workbook.add_format({
                "font_size": 18
            })

            sheet.insert_image("B3", get_module_resource('recreate_printlayouts', 'static/src/img', 'company_logo.png'))
            sheet.write("N5", str(f"Date: {datetime.today().strftime('%B %d, %Y')}"), header_format)

            sheet.write("B10", "TO:", header_attn_format)
            if obj.insurance_address:
                sheet.merge_range("B11:G17", obj.insurance_address, addresses_block_format)
            if obj.partner_id:
                sheet.merge_range("J11:O17", obj.partner_id.contact_address_complete, addresses_block_format)
            if obj.bank_address:
                sheet.merge_range("B19:G25", obj.bank_address, addresses_block_format)

            sheet.write("B27", "ATTN: TO WHOM IT MAY CONCERN", header_attn_format)
            
            sheet.merge_range("F29:L30", "***Shipment Advice***", title_format)

            sheet.write("C34", "P/I No.:", main_content_format)
            sheet.write("C36", "Date of Shipping:", main_content_format)
            sheet.write("C38", "ETA (on or about):", main_content_format)
            sheet.write("C40", "Name of Vessel:", main_content_format)
            sheet.write("C42", "Voyage Number:", main_content_format)
            sheet.write("C44", "Port of Loading:", main_content_format)
            sheet.write("C46", "Post of Discharge:", main_content_format)
            sheet.write("C48", "Bill(S) of Ladding:", main_content_format)
            sheet.write("C50", "Name of Carrier:", main_content_format)
            sheet.write("C52", "Name of Shipper:", main_content_format)
            sheet.write("C54", "Shipping Marks:", main_content_format)
            sheet.write("C56", "Invoice Value:", main_content_format)

            sheet.write("F34", obj.pi_number if obj.pi_number else '', main_content_format)
            sheet.write("F36", obj.shipment_date.strftime("%B %d, %Y") if obj.shipment_date else '', main_content_format)
            sheet.write("F38", obj.date_deadline.strftime("%B %d, %Y") if obj.date_deadline else '', main_content_format)
            sheet.write("F40", obj.name_of_vessel if obj.name_of_vessel else '', main_content_format)
            sheet.write("F42", obj.voyage_number if obj.voyage_number else '', main_content_format)
            sheet.write("F44", obj.port_of_loading if obj.port_of_loading else '', main_content_format)
            sheet.write("F46", obj.port_of_discharge if obj.port_of_discharge else '', main_content_format)
            sheet.write("F48", obj.bill_of_lading_number if obj.bill_of_lading_number else '', main_content_format)
            sheet.write("F50", obj.carrier_id.name if obj.carrier_id else '', main_content_format)
            sheet.write("F52", obj.user_id.name if obj.user_id else '', main_content_format)
            sheet.write("F54", obj.shipping_marks if obj.shipping_marks else '', main_content_format)
            invoice_origins = obj.origin.split(',')
            record = self.env["sale.order"].search([('name', '=', invoice_origins[-1])], limit=1)
            sheet.write("F56", record.amount_invoiced if record else '', main_content_format)

            for col in range(1, 4):
                sheet.write(58, col, None, bottom_border)
            sheet.write("B59", "SHIPMENT CONTENT:", shipment_content_label)

            sheet.write("B61", "Mode of Packing", table_header_format)
            sheet.write("G61", "Description of Goods", table_header_format)
            sheet.write("L61", "Quantity", table_header_format)

            row = 62
            total_gross_weight, total_net_weight, total_cartons = 0, 0, 0
            for line in obj.move_ids:
                sheet.write(row, 1, f"{line.cartons} CTNS", main_content_format)
                sheet.write(row, 6, line.name, main_content_format)
                sheet.write(row, 11, line.quantity, main_content_format)
                total_cartons += line.cartons
                total_gross_weight += line.gross_weight
                total_net_weight += line.net_weight
                row += 2
            
            sheet.write(row, 1, f"Container Number. {obj.container_number if obj.container_number else ''}", main_content_bold_format)
            sheet.write(row, 6, f"Seal Number. {obj.seal_number if obj.seal_number else ''}", main_content_bold_format)
            row += 3

            sheet.write(row, 1, f"TOTAL PACKAGES: {total_cartons}, TOTAL N.W.: {total_net_weight}KGS, TOTAL G.W.: {total_gross_weight}KGS", main_content_format)
            row += 2

            sheet.write(row, 1, 'COVER NOTE NO.BNIC/PB/MC-0334/06/2025 DATED 250626', main_content_bold_format)
            row += 2

            invoice_origins = obj.origin.split(',')
            record_list = [self.env["sale.order"].search([('name', '=', name)]) for name in invoice_origins]
            lc_no_ls, lc_date = [rec.lc_number for rec in record_list if rec.lc_number], [rec.lc_issue_date.strftime("%Y%m%d") for rec in record_list if rec.lc_issue_date]
            if lc_no_ls and lc_date:
                sheet.write(row, 1, f"L/C No. AND DATE {','.join(lc_no_ls)} DATE of ISSUE {','.join(lc_date)}", main_content_bold_format)
                row += 2
            
            sheet.write(row, 1, 'Remarks:', main_content_bold_format)
            row += 1

            sheet.write(row, 1, obj.remarks if obj.remarks else '', main_content_format)
            row += 8

            sheet.write(row, 1, "Yours faithfully,", main_content_format)
            row += 6

            for col in range(1, 5):
                sheet.write(row, col, None, top_border)
            sheet.write(row, 1, "ADAP.S ASIA COMPANY LIMITED", signature_section_format)
            row += 3

            sheet.write(row, 7, 'ADAP.S ASIA  COMPANY LIMITED', last_company_name_format)
            row += 1
            sheet.write(row, 5, 'UNIT 2803, 28/F, PROSPERITY PLACE 6 SHING YIP STREET, KWUN TONG KOWLOON, HONG KONG', document_end_format)
            row += 1
            sheet.write(row, 7, 'Tel:+852 2136 8454 Fax: +852 2137 0444 Email: info@adpsasia.com', document_end_format)


