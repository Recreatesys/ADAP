from odoo import models, fields
import logging
from odoo.modules.module import get_module_resource
from datetime import datetime


_logger = logging.getLogger(__name__)

class CertificateXlsx(models.AbstractModel):
    _name = 'report.recreate_printlayouts.report_adap_certificate'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, picking):
        for obj in picking:
            report_name = f'{obj.name} - Beneficiary Certificate'
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

            header_attn_format = workbook.add_format({
                "font_size": 14,
                "bottom": 1,
            })

            bottom_border = workbook.add_format({
                "bottom": 1,
            })

            main_content_label_format = workbook.add_format({
                "bold": 1,
                "font_size": 14
            })

            main_content_format = workbook.add_format({
                "bold": 1,
                "font_size": 14,
                "bottom": 1,
            })

            document_end_format = workbook.add_format({
                "font_size": 12
            })

            sheet.insert_image("B3", get_module_resource('recreate_printlayouts', 'static/src/img', 'company_logo.png'))
            sheet.write("N5", str(f"Date: {datetime.today().strftime('%B %d, %Y')}"), header_format)
            sheet.write("B11", obj.partner_id.contact_address_complete, header_format)
            sheet.write("B12", str(f"IRC NO. {obj.partner_id.irc_number if obj.partner_id.irc_number else ''}"), header_format)
            sheet.write("B13", str(f"BIN/VAT REGISTRATION NO. {obj.partner_id.vat if obj.partner_id.vat else ''}"), header_format)
            sheet.write("B14", str(f"TIN {obj.partner_id.tin_number if obj.partner_id.tin_number else ''}"), header_format)

            for column in range(1, 6):
                sheet.write(17, column, None, bottom_border)
            sheet.write("B18", "ATTN: TO WHOM IT MAY CONCERN", header_attn_format)

            sheet.merge_range("G21:N22", "CERTIFICATE", title_format)

            sheet.write("B26", "P/I No.:", main_content_label_format)
            sheet.write("B28", "Name of Vessel:", main_content_label_format)
            sheet.write("B30", "Voyage Number:", main_content_label_format)
            sheet.write("B32", "Shipment Date", main_content_label_format)
            sheet.write("B34", "Bill of Lading Number:", main_content_label_format)

            for row in range(25, 35, 2):
                for col in range(10, 16):
                    sheet.write(row, col, None, bottom_border)
            
            sheet.write("M26", obj.pi_number if obj.pi_number else '', main_content_format)
            sheet.write("M28", obj.name_of_vessel if obj.name_of_vessel else '', main_content_format)
            sheet.write("M30", obj.voyage_number if obj.voyage_number else '', main_content_format)
            sheet.write("M32", obj.shipment_date if obj.shipment_date else '', main_content_format)
            sheet.write("M34", obj.bill_of_lading_number if obj.bill_of_lading_number else '', main_content_format)

            sheet.write("B40", "L/C No. AND DATE 2352355 DATE of ISSUE 23525", main_content_label_format)

            sheet.write("L46", "ISSUED BY", header_format)
            for col in range(11, 16):
                sheet.write(50, col, None, bottom_border)
            sheet.write("L52", "AS AGENT OF CARRIER", document_end_format)
