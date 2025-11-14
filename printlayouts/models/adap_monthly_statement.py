from odoo import models, fields
import logging
from odoo.modules.module import get_module_resource
from datetime import datetime, date
from collections import defaultdict


_logger = logging.getLogger(__name__)

class AdapMonthlyStatment(models.AbstractModel):
    _name = 'report.printlayouts.report_adap_inter_statements'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, wizard):
        for obj in wizard:
            report_name = f"{obj.month} Statement"
            sheet = workbook.add_worksheet(report_name)

            main_title_format = workbook.add_format({
                "bold": 1,
                "font_size": 26,
                "valign": "vcenter",
                "align": "center"
            })

            address_format = workbook.add_format({
                "bold": 1,
                "font_size": 16
            })

            contact_info_format = workbook.add_format({
                "bold": 1,
                "font_size": 14
            })

            date_currency_format = workbook.add_format({
                "font_size": 13
            })

            document_info_block_format = workbook.add_format({
                "text_wrap": 1,
                "valign": "top",
                "align": "left",
                "font_size": 11,
                "left": 1,
                "right": 1,
                "top": 1,
                "bottom": 1
            })

            last_info_block_format = workbook.add_format({
                "font_size": 20,
                "valign": "vcenter",
                "align": "center",
                "left": 1,
                "right": 1,
                "top": 1,
                "bottom": 1
            })

            document_title_format = workbook.add_format({
                "font_size": 16,
                "bold": 1,
                "valign": "vcenter",
                "align": "center",
                "underline": 1

            })

            bottom_thick_format = workbook.add_format({
                "bottom": 2,
                "font_size": 12,
                "bold": 1
            })

            top_border_format = workbook.add_format({
                "top": 1
            })

            bottom_border_format = workbook.add_format({
                "bottom": 1
            })

            deduct_monthly_debt_section_format = workbook.add_format({
                "font_size": 12,
                "bold": 1
            })

            deduct_monthly_debt_section_label_format = workbook.add_format({
                "font_size": 12,
                "bold": 1,
                "align": "right"
            })

            top_border_double_bottom_border = workbook.add_format({
                "top": 1,
                "bottom": 6
            })

            special_total_format = workbook.add_format({
                "top": 1,
                "bottom": 6,
                "font_size": 12,
                "bold": 1
            })

            debt_section_format = workbook.add_format({
                "font_size": 12,
                "bold": 1
            })

            signature_text_format = workbook.add_format({
                "font_size": 13,
                "bold": 1
            })

            confirmation_text_format = workbook.add_format({
                "font_size": 13,
                "bold": 1,
                "bottom": 1
            })

            eoe_format = workbook.add_format({
                "font_size": 12,
                "align": "center",
                "top": 1
            })

            month_mapping = {
                "January": 1,
                "Feburary": 2,
                "March": 3,
                "April": 4,
                "May": 5,
                "June": 6,
                "July": 7,
                "August": 8,
                "September": 9,
                "October": 10,
                "November": 11,
                "December": 12
            }

            sheet.merge_range("E2:P5", "誉达金属塑胶制品（惠州）有限公司", main_title_format)
            sheet.write("F6", "惠州市博罗县园州镇河北片电域路北侧", address_format)
            sheet.write("F7", "电话: 752-6681618", contact_info_format)
            sheet.write("I7", "传真: 752-6681808", contact_info_format)
            sheet.write("O6", "日期", date_currency_format)
            sheet.write("O7", "貨幣", date_currency_format)
            sheet.write("P6", datetime.today().date().strftime("%d-%b-%Y"),date_currency_format)
            sheet.write("P7", "人民币 (RMB¥)", date_currency_format)
            sheet.merge_range("C9:H12", "客戶:\n地址:\n电话:\n传真:", document_info_block_format)
            sheet.merge_range("N9:Q11", "月结90天含税", last_info_block_format)
            sheet.merge_range("I14:M15", f"{datetime.now().year}年{month_mapping[obj.month]}月份对账单", document_title_format)

            for col in range(2, 19):
                sheet.write(16, col, None, bottom_thick_format)
            sheet.write("C17", "Date", bottom_thick_format)
            sheet.write("E17", "Delivery Note", bottom_thick_format)
            sheet.write("G17", "Purchase Order", bottom_thick_format)
            sheet.write("I17", "Description", bottom_thick_format)
            sheet.write("L17", "Remarks", bottom_thick_format)
            sheet.write("N17", "Quantity", bottom_thick_format)
            sheet.write("P17", "Unit", bottom_thick_format)
            sheet.write("Q17", "Weight", bottom_thick_format)
            sheet.write("R17", "Rate", bottom_thick_format)
            sheet.write("S17", "Amount", bottom_thick_format)

            row = 18
            if month_mapping[obj.month] == 12:
                next_month_start = date(datetime.now().year + 1, 1, 1)
            else:
                next_month_start = date(datetime.now().year, month_mapping[obj.month] + 1, 1)

            invoice_search_domain = [
                ('partner_id', '=', 1),
                ('state', '!=', 'cancel'),
                ('invoice_date', '>=', date(datetime.now().year, month_mapping[obj.month], 1)),
                ('invoice_date', '<', next_month_start), 
            ]

            
            invoices = self.env["account.move"].search(invoice_search_domain, order="invoice_date ASC")
            total = 0
            for records in invoices:
                purchase_delivery_pairs = {"purchase": [], "delivery": []}
                if records.invoice_origin:
                    sale_order = records.invoice_origin.split(',')
                    sale_order_list = [self.env["sale.order"].search([('name', '=', name)]) for name in sale_order]
                    for sales in sale_order_list:
                        purchase_records = sales._get_purchase_orders()
                        delivery_records = sales._get_outgoing_picking_records(sales.picking_ids)
                        for purchase in purchase_records:
                            purchase_delivery_pairs['purchase'].append(purchase.name)
                        for delivery in delivery_records:
                            purchase_delivery_pairs["delivery"].append(delivery.name)
                for lines in records.invoice_line_ids:
                    sheet.write(row, 2, lines.date.strftime("%d/%m/%Y"))
                    sheet.write(row, 4, ','.join(purchase_delivery_pairs['delivery']))
                    sheet.write(row, 6, ','.join(purchase_delivery_pairs['purchase']))
                    sheet.write(row, 8, lines.name)
                    sheet.write(row, 11, lines.remarks if lines.remarks else '')
                    sheet.write(row, 13, lines.quantity)
                    sheet.write(row, 15, lines.product_uom_id.name)
                    sheet.write(row, 16, lines.weight)
                    sheet.write(row, 17, lines.rate)
                    sheet.write(row, 18, lines.price_subtotal)
                    total += lines.price_subtotal
                row += 2
            
            # Go back to the previous row to draw the upper border
            row -= 1
            for col in range(2, 19):
                sheet.write(row, col, None, top_border_format)
            row += 1

            for col in range(2, 19):
                sheet.write(row, col, None, bottom_thick_format)
            sheet.write(row, 2, "Date", bottom_thick_format)
            sheet.write(row, 8, "Description", bottom_thick_format)
            sheet.write(row, 13, "Payment", bottom_thick_format)
            sheet.write(row, 18, "Amount", bottom_thick_format)

            row += 2

            target_date = date(datetime.now().year, month_mapping[obj.month] + 1, 1)

            invoice_month_paid, invoice_month_debt = defaultdict(int), defaultdict(int)
            all_invoice = self.env['account.move'].search([("partner_id", '=', 1), ('invoice_date', '<', target_date)])
            payment_record_list = []
            for invoice_rec in all_invoice:
                payment_info = invoice_rec.invoice_payments_widget
                invoice_month_debt[(invoice_rec.invoice_date.month, invoice_rec.invoice_date.year)] += invoice_rec.amount_residual
                if payment_info and payment_info['content']:
                    for payment_rec in payment_info['content']:
                        if payment_rec["date"].year == datetime.now().year and payment_rec["date"].month == month_mapping[obj.month]:
                            curr = [payment_rec["date"], payment_rec["amount"], payment_rec["journal_name"]]
                            payment_record_list.append(curr)
                            paid_invoice = self.env['account.move'].search([('id', '=', payment_rec['move_id'])])
                            invoice_date = paid_invoice.invoice_date
                            invoice_month_paid[invoice_date.month] += payment_rec['amount']
            
            payment_record_list.sort(key=lambda x: x[0])
            for rec in payment_record_list:
                sheet.write(row, 2, rec[0].strftime("%d/%m/%Y"))
                sheet.write(row, 8, rec[2])
                sheet.write(row, 13, f"({rec[1]})")
                sheet.write(row, 18, f"({rec[1]})")
                row += 2
            
            row -= 1
            for col in range(2, 19):
                sheet.write(row, col, None, top_border_format)
            row += 1

            sorted_invoice_month_debt = sorted(invoice_month_paid.items(), key=lambda x: (x[1], x[0]))
            for month, amount in sorted_invoice_month_debt:
                sheet.write(row, 13, f"扣減{month[0]}月份帐", deduct_monthly_debt_section_format)
                sheet.write(row, 15, "人民币 (RMB¥)", deduct_monthly_debt_section_format)
                sheet.write(row, 18, amount, deduct_monthly_debt_section_format)
                row += 1
            row += 1

            sheet.write(row, 13, "本月小计", deduct_monthly_debt_section_label_format)
            sheet.write(row, 15, "人民币 (RMB¥)", deduct_monthly_debt_section_format)
            sheet.write(row, 18, total, deduct_monthly_debt_section_format)
            row += 1
            sheet.write(row, 13, "本月扣帐", deduct_monthly_debt_section_label_format)
            sheet.write(row, 15, "人民币 (RMB¥)", deduct_monthly_debt_section_format)
            sheet.write(row, 18, invoice_month_paid[obj.month] if obj.month in invoice_month_paid else '', deduct_monthly_debt_section_format)
            row += 1
            sheet.write(row, 13, "总额", deduct_monthly_debt_section_label_format)
            sheet.write(row, 15, "人民币 (RMB¥)", deduct_monthly_debt_section_format)
            for col in range(17, 19):
                sheet.write(row, col, None, top_border_double_bottom_border)
            sheet.write(row, 18, total - invoice_month_paid[obj.month], special_total_format)
            row += 2

            
            selected_month = month_mapping[obj.month]
            current_year = datetime.now().year

            total_debt, remain = 0, 0
            for k, v in invoice_month_debt.items():
                c_month, c_year = k
                if c_year == current_year:
                    if c_month <= selected_month:
                        total_debt += v
                        remain += v
                elif c_year < current_year:
                    total_debt += v
                    remain += v

            sheet.write(row, 13, "本月结欠", debt_section_format)
            sheet.write(row, 15, f"{current_year}年{selected_month}月份", debt_section_format)
            sheet.write(row, 18, invoice_month_debt[(selected_month, current_year)] if invoice_month_debt[(selected_month, current_year)] > 0 else '', debt_section_format)
            sheet.write(row, 2, "签署及盖章确认:", signature_text_format)
            remain -= invoice_month_debt[(selected_month, current_year)]
            selected_month -= 1
            if selected_month == 0:
                selected_month = 12
                current_year -= 1
            row += 1

            sheet.write(row, 13, "欠款 1-30 天", debt_section_format)
            sheet.write(row, 15, f"{current_year}年{selected_month}月份", debt_section_format)
            sheet.write(row, 18, invoice_month_debt[(selected_month, current_year)] if invoice_month_debt[(selected_month, current_year)] > 0 else '', debt_section_format)
            remain -= invoice_month_debt[(selected_month, current_year)]
            selected_month -= 1
            if selected_month == 0:
                selected_month = 12
                current_year -= 1
            row += 1

            sheet.write(row, 13, "欠款 31-60 天", debt_section_format)
            sheet.write(row, 15, f"{current_year}年{selected_month}月份", debt_section_format)
            sheet.write(row, 18, invoice_month_debt[(selected_month, current_year)] if invoice_month_debt[(selected_month, current_year)] > 0 else '', debt_section_format)
            remain -= invoice_month_debt[(selected_month, current_year)]
            selected_month -= 1
            if selected_month == 0:
                selected_month = 12
                current_year -= 1
            row += 1

            sheet.write(row, 13, "欠款 61-90 天", debt_section_format)
            sheet.write(row, 15, f"{current_year}年{selected_month}月份", debt_section_format)
            sheet.write(row, 18, invoice_month_debt[(selected_month, current_year)] if invoice_month_debt[(selected_month, current_year)] > 0 else '', debt_section_format)
            remain -= invoice_month_debt[(selected_month, current_year)]
            selected_month -= 1
            if selected_month == 0:
                selected_month = 12
                current_year -= 1
            row += 1

            sheet.write(row, 13, "欠款 91 天以上", debt_section_format)
            sheet.write(row, 15, f"{current_year}年{selected_month}月份前", debt_section_format)
            sheet.write(row, 18, remain if remain > 0 else '', debt_section_format)
            row += 1

            for col in range(17, 19):
                sheet.write(row, col, None, top_border_double_bottom_border)
            sheet.write(row, 13, "总欠款", debt_section_format)
            sheet.write(row, 15, "人民币 (RMB¥)", debt_section_format)
            sheet.write(row, 18, total_debt if total_debt > 0 else '', special_total_format)
            for col in range(2, 7):
                sheet.write(row, col, None, bottom_border_format)
            row += 4

            for col in range(2, 19):
                sheet.write(row, col, None, bottom_border_format)
            sheet.write(row, 7, "烦请核对后签章回传至 传真 : (852) 2137 0444", confirmation_text_format)
            row += 2
            merge_range_f_string = str(f"J{row}:K{row}")
            sheet.merge_range(merge_range_f_string, "E & O.E", eoe_format)


            
            

        
            




