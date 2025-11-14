from odoo import models, fields
import logging
from odoo.modules.module import get_module_resource


_logger = logging.getLogger(__name__)

class PackingListXlsx(models.AbstractModel):
    _name = 'report.printlayouts.report_adap_packing_list'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, picking):
        for obj in picking:
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

            document_info_format = workbook.add_format({
                "bold": 1,
                "font_size": 14
            })

            table_top_border = workbook.add_format({
                "top": 1,
            })

            table_bottom_border = workbook.add_format({
                "bottom": 1
            })

            description_of_goods_format = workbook.add_format({
                "font_size": 14,
                "bold": 1,
                "top": 1,
            })

            quantity_format = workbook.add_format({
                "font_size": 14,
                "align": "center",
                "bold": 1,
                "top": 1,
                "text_wrap": 1
            })

            quantity_units_format = workbook.add_format({
                "font_size": 14,
                "align": "center",
                "bold": 1,
                "bottom": 1,
            })

            total_section_format = workbook.add_format({
                "top": 1,
                "bottom": 6
            })

            table_body_format = workbook.add_format({
                "font_size": 13
            })

            total_section_values_format = workbook.add_format({
                "font_size": 14,
                "top": 1,
                "bottom": 6,
                "bold": 1
            })

            total_currency_format = workbook.add_format({
                "font_size": 14,
                "bold": 1
            })

            total_amount_format = workbook.add_format({
                "font_size": 14,
                "top": 1,
                "bottom": 6
            })

            bottom_text_format = workbook.add_format({
                "font_size": 14,
            })

            signature_box_format = workbook.add_format({
                "font_size": 14,
                "top": 1,
            })

            document_info_value_format = workbook.add_format({
                "font_size": 14
            })

            document_end_text_format = workbook.add_format({
                "font_size": 14
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
            sheet.merge_range("F11:I11", "Packing List", main_title_format)

            # Document Information section (Labels)
            sheet.write("B14", "Deliver to:", document_info_format)
            sheet.write("K14", "PL No.", document_info_format)
            sheet.write("K15", "Date", document_info_format)
            sheet.write("K16", "Customer", document_info_format)
            sheet.write("K17", "P/I NO.", document_info_format)
            sheet.write("B21", "Invoice No.", document_info_format)
            sheet.write("B22", "Salesman", document_info_format)

            # Document Information section (values)
            sheet.write("M16", obj.partner_id.name, document_info_value_format)
            sheet.write("M15", obj.create_date.strftime("%Y-%m-%d"), document_info_value_format)
            sheet.write("M17", obj.pi_number, document_info_value_format)
            sheet.write("C22", obj.user_id.name, document_info_value_format)
            sheet.write("M14", obj.pl_number, document_info_value_format)
            sheet.write("C14", obj.partner_id.contact_address_complete, document_info_value_format)
            fax_string = str(f"FAX: {obj.partner_id.x_studio_char_field_1ci_1j35oraga if obj.partner_id.x_studio_char_field_1ci_1j35oraga else ''}")
            phone_string = str(f'TEL: {obj.partner_id.phone}')
            sheet.write("C16", phone_string, document_info_value_format)
            sheet.write("C17", fax_string, document_info_value_format)

            # Table Header Info
            sheet.set_row(23, 42)
            sheet.set_column("G:J", 17.29)
            sheet.set_column("B:B", 26.29)
            for column in range(1, 14):
                sheet.write(23, column, None, table_top_border)
                sheet.write(24, column, None, table_bottom_border)
            sheet.write("B24", "Description of goods", description_of_goods_format)
            sheet.write("B25", None, quantity_units_format)
            sheet.merge_range("E24:F24", "Quantity", quantity_format)
            sheet.write("E25", "(CTNS)", quantity_units_format)
            sheet.write("F25", "(PCS)", quantity_units_format)
            sheet.write("I24", "Meas.", quantity_format)
            sheet.write("I25", "(CBM)", quantity_units_format)
            sheet.write("L24", "N.W.", quantity_format)
            sheet.write("L25", "(KGS)", quantity_units_format)
            sheet.write("N24", "G.W.", quantity_format)
            sheet.write("N25", "(KGS)", quantity_units_format)


            total_net_weight, total_gross_weight = 0, 0
            total_cartons, total_units = 0, 0
            row = 26
            for line in obj.move_ids:
                if line.product_id.name != False:
                    sheet.write(row, 1, line.product_id.name, table_body_format)
                    sheet.write(row, 4, '{:.2f}'.format(line.cartons), table_body_format)
                    sheet.write(row, 5, '{:.2f}'.format(line.quantity), table_body_format)
                    sheet.write(row, 11, '{:.2f}'.format(line.net_weight), table_body_format)
                    sheet.write(row, 13, '{:.2f}'.format(line.gross_weight), table_body_format)
                    total_net_weight += line.net_weight
                    total_gross_weight += line.gross_weight
                    total_cartons += line.cartons
                    total_units += line.quantity
                    row += 4
            
            for column in range(1, 14):
                sheet.write(row, column, None, total_section_format)
            
            sheet.write(row, 1, 'TOTAL:', total_section_values_format)
            sheet.write(row, 4, '{:.2f}'.format(total_cartons), total_section_values_format)
            sheet.write(row, 5, '{:.2f}'.format(total_units), total_section_values_format)
            sheet.write(row, 11, '{:.2f}'.format(total_net_weight), total_section_values_format)
            sheet.write(row, 13, '{:.2f}'.format(total_gross_weight), total_section_values_format)

            row += 2

            sheet.write(row, 1, "TRADE TERMS:", bottom_text_format)
            if obj.trade_terms:
                sheet.write(row, 2, obj.trade_terms, document_end_text_format)
            row += 1

            sheet.write(row, 2, "COUNTRY OF ORIGIN:", document_end_text_format)
            if obj.country_of_origin:
                sheet.write(row, 5, obj.country_of_origin.name, document_end_text_format)
            row += 1

            sheet.write(row, 2, "PORT OF LOADING:", document_end_text_format)
            sheet.write(row, 5, obj.port_of_loading, document_end_text_format)
            row += 2

            sheet.write(row, 1, "PACKING:", bottom_text_format)
            weight_string = str(f'NET WEIGHT: {obj.shipping_weight}KGS AND GROSSS WEIGHT: {obj.weight}KGS')
            sheet.write(row, 2, weight_string, document_end_text_format)
            row += 1
            sheet.write(row, 2, "PACKING ARE EXPORT STANDARD SEA WORTHY", document_end_text_format)

            row += 1

            sheet.write(row, 1, "REMARKS:", bottom_text_format)
            sheet.write(row, 2, obj.remarks, document_end_text_format)
            

