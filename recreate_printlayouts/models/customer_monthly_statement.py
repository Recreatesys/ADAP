from odoo import models, fields
import logging
from odoo.modules.module import get_module_resource
from datetime import datetime


_logger = logging.getLogger(__name__)

class CustomerMonthlyStatement(models.AbstractModel):
    _name = 'report.recreate_printlayouts.report_adap_monthly_statements'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, wizard):
         for obj in wizard:
            report_name = f"{obj.partner_id.name} - Monthly Statement"
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

            address_block_section_format = workbook.add_format({
                "font_size": 14,
                "text_wrap": 1,
                "valign": "top",
            })

            document_info_value_format = workbook.add_format({
                "font_size": 14
            })

            table_top_border = workbook.add_format({
                "top": 1,
            })

            table_bottom_border = workbook.add_format({
                "bottom": 1,
            })

            top_bottom_border = workbook.add_format({
                "top": 1,
                "bottom": 1
            })

            table_header_format = workbook.add_format({
                "bold": 1,
                "font_size": 13,
                "top": 1
            })

            table_header_format_bottom_border = workbook.add_format({
                "bold": 1,
                "font_size": 13,
                "bottom": 1
            })

            total_balance_label_format = workbook.add_format({
                "bold": 1,
                "font_size": 13
            })

            total_balance_value_format = workbook.add_format({
                "bold": 1,
                "font_size": 13,
                "top": 1,
                "bottom": 6
            })

            top_border_double_bottom_border = workbook.add_format({
                "top": 1,
                "bottom": 6
            })

            due_date_value_format = workbook.add_format({
                "top": 1,
                "bottom": 1,
                "font_size": 13,
                "bold": 1
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
            sheet.merge_range("E11:L11", "Customer Monthly Statement", main_title_format)

             # Document Information section (Labels)
            sheet.write("B14", "Name", document_info_format)
            sheet.write("B15", "Address", document_info_format)
            sheet.write("K14", "Tel:", document_info_format)
            sheet.write("K15", "Fax:", document_info_format)
            sheet.write("K16", "Customer", document_info_format)
            sheet.write("B22", "Date", document_info_format)

            # Document Information section (Values)
            sheet.write("M14", obj.partner_id.phone if obj.partner_id.phone else '', document_info_value_format)
            sheet.write("M15", obj.partner_id.x_studio_char_field_1ci_1j35oraga if obj.partner_id.x_studio_char_field_1ci_1j35oraga else '', document_info_value_format)
            sheet.write("M16", obj.partner_id.name, document_info_value_format)
            sheet.merge_range("D15:H20", obj.partner_id.contact_address_complete if obj.partner_id.contact_address_complete else '', address_block_section_format)
            sheet.write("D22", f"{obj.start_date.strftime("%d %b %Y")} TO {obj.end_date.strftime("%d %b %Y")}", document_info_value_format)

            # Table Header
            for col in range(1, 15):
                sheet.write(23, col, None, table_top_border)
                sheet.write(24, col, None, table_bottom_border)
            
            sheet.write("B24", "Invoices", table_header_format)
            sheet.write("D24", "SO", table_header_format)
            sheet.write("F24", "B/L Date", table_header_format)
            sheet.write("H24", "Due Date", table_header_format)
            sheet.write("J24", "Invoice Amount", table_header_format)
            sheet.write("M24", "Debit", table_header_format)
            sheet.write("N24", "Credit", table_header_format)
            sheet.write("O24", "Balance", table_header_format)
            sheet.write("M25", "US$", table_header_format_bottom_border)
            sheet.write("N25", "US$", table_header_format_bottom_border)
            sheet.write("O25", "US$", table_header_format_bottom_border)

            # Table content 
            row = 26
            invoice_search_domain = [
                ('partner_id', '=', obj.partner_id.id),
                ('state', '!=', 'cancel'),
                ('state', '!=', 'paid'),
                ('invoice_date', '<=', obj.end_date),
                ('invoice_date', '>=', obj.start_date),
            ]

            invoices = self.env['account.move'].search(invoice_search_domain, order='invoice_date ASC')
            total_balance = 0
            for invoice in invoices:
                so_records = invoice.line_ids.sale_line_ids.order_id
                sheet.write(row, 1, invoice.name)
                sheet.write(row, 3, ','.join([so.name for so in so_records]))
                sheet.write(row, 5, invoice.invoice_date.strftime("%d %b %Y"))
                sheet.write(row, 7, invoice.invoice_date_due.strftime("%d %b %Y"))
                sheet.write(row, 9, invoice.amount_total)
                sheet.write(row, 12, invoice.amount_residual)
                payment_records = invoice.invoice_payments_widget
                total_paid_amount = 0
                if payment_records:
                    for pay_record in payment_records['content']:
                        total_paid_amount += pay_record["amount"]
                
                total_balance += invoice.amount_residual
                sheet.write(row, 13, total_paid_amount)
                sheet.write(row, 14, total_balance)
                row += 2
            
            # Total section
            row += 2
            sheet.write(row, 12, "Balance: US$", total_balance_label_format)
            for col in range(13, 15):
                sheet.write(row, col, None, top_border_double_bottom_border)
            sheet.write(row, 13, total_balance, total_balance_value_format)
            row += 2

            # Due Invoices section
            sheet.write(row, 4, "Not Yet Due", total_balance_label_format)
            sheet.write(row, 7, "0-30 Days", total_balance_label_format)
            sheet.write(row, 9, "31-60 Days", total_balance_label_format)
            sheet.write(row, 11, "61-90 Days", total_balance_label_format)
            sheet.write(row, 13, "Over 90 Days", total_balance_label_format)
            row += 1
            for col in range(1, 15):
                sheet.write(row, col, None, top_bottom_border)
            
            due_dates_dict = {
                "Not Yet Due": 0,
                "0-30": 0,
                "31-60": 0,
                "61-90": 0,
                "Over 90 Days": 0
            }
            
            today = datetime.today().date()
            for invoice in invoices:
                due_date = invoice.invoice_date_due
                diff = today - due_date
                days_diff = diff.days
                if days_diff < 0:
                    due_dates_dict['Not Yet Due'] += invoice.amount_residual
                elif 0 <= days_diff <= 30:
                    due_dates_dict["0-30"] += invoice.amount_residual
                elif 31 <= days_diff <= 60:
                    due_dates_dict["31-60"] += invoice.amount_residual
                elif 61 <= days_diff <= 90:
                    due_dates_dict["61-90"] += invoice.amount_residual
                else:
                    due_dates_dict["Over 90 Days"] += invoice.amount_residual
            
            sheet.write(row, 2, "US$", due_date_value_format)
            sheet.write(row, 4, due_dates_dict["Not Yet Due"], due_date_value_format)
            sheet.write(row, 7, due_dates_dict["0-30"], due_date_value_format)
            sheet.write(row, 9, due_dates_dict["31-60"], due_date_value_format)
            sheet.write(row, 11, due_dates_dict["61-90"], due_date_value_format)
            sheet.write(row, 13, due_dates_dict["Over 90 Days"], due_date_value_format)


            







