from odoo import models, fields
import logging
from odoo.modules.module import get_module_resource


_logger = logging.getLogger(__name__)

class CommercialInvoiceXlsx(models.AbstractModel):
    _name = 'report.recreate_printlayouts.report_adap_commercial_invoice'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, moves):
        for obj in moves:
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

            table_top_bottom_border = workbook.add_format({
                "top": 1,
                "bottom": 1
            })

            description_of_goods_format = workbook.add_format({
                "font_size": 14,
                "bold": 1,
                "top": 1,
                "bottom": 1,
                "valign": "top"
            })

            quantity_format = workbook.add_format({
                "font_size": 14,
                "align": "center",
                "bold": 1,
                "top": 1,
                "bottom": 1,
                "text_wrap": 1
            })

            unit_amount_format = workbook.add_format({
                "font_size": 14,
                "align": "right",
                "bold": 1,
                "top": 1,
                "bottom": 1,
                "text_wrap": 1
            })

            table_body_format = workbook.add_format({
                "font_size": 13
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
            sheet.insert_image("B3", get_module_resource('recreate_printlayouts', 'static/src/img', 'company_logo.png'))

            # Company name / information section
            sheet.set_column("M:N", 13.57)
            sheet.merge_range("I3:N3", "ADAP.S ASIA COMPANY LIMITED", title_format)
            sheet.merge_range("L4:N4", '譽達亞洲有限公司', title_format)
            sheet.merge_range("G5:N5", 'UNIT 2803, 28/F, PROSPERITY PLACE 6SHING YIP STREET, KWUN TONG, KOWLOON, HONG KONG', company_info_format)
            sheet.merge_range("L6:N6", 'Tel: +852 2136 9454 Fax: +852 2137 04444', company_info_format)
            sheet.merge_range("M7:N7", 'Email: info@adapsasia.com', company_info_format)
            
            # Document Title
            sheet.merge_range("F11:I11", "Commercial Invoice", main_title_format)

            # Document Information section (Labels)
            sheet.write("B14", "Messr.", document_info_format)
            sheet.write("K14", "Invoice No.", document_info_format)
            sheet.write("K15", "Date", document_info_format)
            sheet.write("K16", "Customer", document_info_format)
            sheet.write("K17", "P/I NO.", document_info_format)
            sheet.write("B22", "Salesman", document_info_format)

            # Document Information section (values)
            sheet.write("M14", moves.name, document_info_value_format)
            sheet.write("M15", moves.invoice_date.strftime("%Y-%m-%d"), document_info_value_format)
            sheet.write("M16", moves.partner_id.name, document_info_value_format)
            sheet.write("M17", moves.pi_number if moves.pi_number else None, document_info_value_format)
            sheet.write("D22", moves.user_id.name, document_info_value_format)
            messr_record = moves.partner_id.parent_id if moves.partner_id.parent_id else moves.partner_id
            sheet.write("D14", messr_record.name, document_info_value_format)
            sheet.write("D15", messr_record.contact_address_complete, document_info_value_format)
            fax_string = str(f"FAX: {moves.partner_id.x_studio_char_field_1ci_1j35oraga if moves.partner_id.x_studio_char_field_1ci_1j35oraga else ''}")
            phone_string = str(f'TEL: {moves.partner_id.phone}')
            sheet.write("D16", phone_string, document_info_value_format)
            sheet.write("D17", fax_string, document_info_value_format)


            # Table Header Info
            sheet.set_row(23, 42)
            sheet.set_column("G:J", 17.29)
            for column in range(1, 14):
                sheet.write(23, column, None, table_top_bottom_border)
            sheet.write("B24", "Description of goods", description_of_goods_format)
            sheet.write("G24", "Quantity\n(PCS)", quantity_format)
            sheet.write("J24", "UNIT PRICE\n(USD)", unit_amount_format)
            sheet.write("N24", "Amount\n(USD)", unit_amount_format)

            # Table line content
            row = 26
            for line in moves.line_ids:
                if line.product_id.name != False:
                    sheet.write(row, 1, line.product_id.name, table_body_format)
                    sheet.write(row, 6, '{:.2f}'.format(line.quantity), table_body_format)
                    sheet.write(row, 9, '{:.2f}'.format(line.price_unit), table_body_format)
                    sheet.write(row, 13, '{:.2f}'.format(line.price_unit), table_body_format)
                    row += 4
            
            # Total section
            sheet.write(row, 12, moves.currency_id.name, total_currency_format)
            sheet.write(row, 13, '{:.2f}'.format(moves.amount_total_signed), total_amount_format)
            row += 2

            # Total Amount in Words section
            list_amount_total_in_words = moves.amount_total_words.split()
            list_amount_total_in_words = list_amount_total_in_words[0:len(list_amount_total_in_words)-1]
            amount_total_in_words = ' '.join(list_amount_total_in_words).upper()
            sheet.write(row, 1, f'SAY {moves.currency_id.full_name.upper()} {amount_total_in_words} ONLY', bottom_text_format)
            row += 3

            # Trading Terms
            sheet.write(row, 1, "TRADING TERMS:", bottom_text_format)
            sheet.write(row, 4, str(f"TOTAL VALUE: {moves.currency_id.name} {moves.total_value if moves.total_value else ''}"), bottom_text_format)
            row += 1

            sheet.write(row, 4, str(f"TRADE TERM: {moves.trade_term if moves.trade_term else ''}"), bottom_text_format)
            row += 1

            sheet.write(row, 4, "ALL OTHER DETAILS AS PER BENEFICIARY'S SALES CONTRACT/PROFORMA", bottom_text_format)
            row += 1

            if moves.invoice_origin:
                invoice_origins = moves.invoice_origin.split(',')
                record_list = [self.env["sale.order"].search([('name', '=', name)]) for name in invoice_origins]
                origin_list_str = [f'{sale_record.name} DATED {sale_record.date_order.strftime("%Y.%m.%d")}' for sale_record in record_list]
                sheet.write(row, 4, str(f"INVOICE NO. {','.join(origin_list_str)} WHICH MUST APPEAR IN COMMERCIAL INVOICE."), bottom_text_format)
                row += 1

            sheet.write(row, 4, str(f"COUNTRY OF ORIGIN: {moves.country_of_origin.name if moves.country_of_origin else ''}"), document_end_text_format)
            row += 1

            sheet.write(row, 4, f"PORT OF LOADING: {moves.port_of_loading if moves.port_of_loading else ''}", document_end_text_format)
            row += 1

            hs_code_list = [line.product_id.hs_code for line in moves.line_ids if line.product_id and line.product_id.hs_code]
            sheet.write(row, 4, str(f"H.S.CODE {','.join(hs_code_list)}"), document_end_text_format)
            row += 1

            sheet.write(row, 4, "IMPORT UNDER BONDED WAREHOUSE", document_end_text_format)
            row += 1

            sheet.write(row, 4, "WE CERTIFY THAT COUNTRY OF ORIGIN HAVE BEEN CLEARLY MENTIONED ON EACH PACKAGE/CARTON/BAG/CONTAINER.", document_end_text_format)
            row += 2

            # Packing
            sheet.write(row, 1, "PACKING:", bottom_text_format)
            weight_string = str(f'NET WEIGHT: {moves.net_weight}KGS AND GROSSS WEIGHT: {moves.gross_weight}KGS')
            sheet.write(row, 4, weight_string, document_end_text_format)
            row += 1
            sheet.write(row, 4, "PACKING ARE EXPORT STANDARD SEA WORTHY", document_end_text_format)
            row += 2

            # Payment Term
            sheet.write(row, 1, "PAYMENT TERMS:", bottom_text_format)
            if moves.invoice_payment_term_id:
                sheet.write(row, 4, moves.invoice_payment_term_id.name, document_end_text_format)
            row += 1
            sheet.write(row, 4, "*OUR BANKS DETAILS:", document_end_text_format)
            row += 1
            sheet.write(row, 4, "BENEFICIARY: ADAP.S ASIA COMPANY LIMITED", document_end_text_format)
            row += 1
            sheet.write(row, 4, "BANK: HSBC HK", document_end_text_format)
            row += 1
            sheet.write(row, 4, "BANK ADDRESS: 1 QUEEN'S ROAD CENTRAL, HONG KONG", document_end_text_format)
            row += 2

            # Remarks
            sheet.write(row, 1, "REMARKS:", bottom_text_format)
            sheet.write(row, 4, moves.remarks if moves.remarks else '', document_end_text_format)
            row += 8

            # For and On Behalf
            sheet.write(row, 10, 'FOR AND ON BEHALF OF', bottom_text_format)
            row += 5

            # Signature box 
            merge_range = str(f'K{row}:M{row}')
            sheet.merge_range(merge_range, "ADAP.S ASIA COMPANY LTD.", signature_box_format)

            




