from odoo import models, fields
import logging
from odoo.modules.module import get_module_resource
from datetime import datetime, date
from collections import defaultdict
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar


_logger = logging.getLogger(__name__)

class AdapAccountReceivableReport(models.AbstractModel):

    _name = 'report.printlayouts.report_adap_account_receivable_report'
    _inherit = 'report.report_xlsx.abstract'


    def generate_xlsx_report(self, workbook, data, moves):

        report_name = f"{datetime.today().year}-{datetime.today().month}"
        sheet = workbook.add_worksheet(report_name)

        first_row_format = workbook.add_format({
            "font_size": 10,
            "align": 'center',
            "bg_color": "#BFBFBF",
            "border": 1,
        })

        first_row_format_with_bold = workbook.add_format({
            "font_size": 10,
            "align": 'center',
            "bg_color": "#BFBFBF",
            "border": 1,
            "bold": 1,
        })

        second_row_format = workbook.add_format({
            "font_size": 10,
            "bg_color": "#BFBFBF",
            "border": 1,
        })

        second_row_month_format = workbook.add_format({
            "font_size": 10,
            "valign": 'vcenter',
            "align": "center",
            "bold": 1,
            "bg_color": "#BFBFBF",
            "border": 1,
        })

        table_value_format = workbook.add_format({
            "font_size": 10,
            "align": "left",
            "border": 1,
        })

        table_number_format = workbook.add_format({
            "font_size": 10,
            "align": "right",
            "border": 1,
        })

        table_total_format = workbook.add_format({
            "font_size": 10,
            "align": "center",
            "bg_color": "#BFBFBF",
            "border": 1,
        })

        table_total_format_with_bold = workbook.add_format({
            "font_size": 10,
            "align": "center",
            "bg_color": "#BFBFBF",
            "border": 1,
            "bold": 1,
        })

        moves = self.env["account.move"].search([('status_in_payment', '=', 'not_paid')])
        month_mapping = {
            1: '一', 2: '二',
            3: '三', 4: '四',
            5: '五', 6: '六',
            7: '七', 8: '八',
            9: '九', 10: '十',
            11: '十一'
        }
        company_id = None
        today = datetime.today()
        if moves:
            company_id = 1 if moves[0].company_id.id == 1 else 2
        
        if company_id != 1:
            sheet.set_column(0, 0, 25.63)
            sheet.set_column(1, 1, 5.50)
            sheet.set_column(2, 2, 12.38)
            for col in range(3, 18):
                sheet.set_column(col, col, 12.13)
            
            sheet.merge_range("A1:B1", '人民币客户', first_row_format)
            sheet.write("C1", '本月', first_row_format)

            for col in range(3, 14):
                sheet.write(0, col, f"{month_mapping[col - 2]}个月期", first_row_format)
            sheet.write("O1", "合计", first_row_format)
            sheet.write("P1", "应收货款", first_row_format_with_bold)
            sheet.write("Q1", "備註", first_row_format_with_bold)

            sheet.write("A2", "公司名称", second_row_format)
            sheet.write("B2", "代号", second_row_format)
            curr_month_last = calendar.monthrange(today.year, today.month)[1]
            curr_display_date = datetime(today.year, today.month, curr_month_last)
            sheet.write("C2", curr_display_date.strftime("%Y/%m/%d"), second_row_month_format)

            partner_tracking, partner_totals = dict(), dict()
            timeframe = [curr_display_date.strftime("%y-%m")]

            for col in range(3, 14):
                prev_date = today - relativedelta(months=col-2)
                prev_year, prev_month = prev_date.year, prev_date.month
                prev_day = calendar.monthrange(prev_year, prev_month)[1]

                display_date = datetime(prev_year, prev_month, prev_day)
                timeframe.append(display_date.strftime("%Y-%m"))
                sheet.write(1, col, display_date.strftime("%Y/%m/%d"), second_row_month_format)
            
            sheet.write("O2", "RMB", second_row_month_format)
            sheet.write("P2", "RMB", second_row_month_format)
            sheet.write("Q2", "", second_row_month_format)

            earliest_date = display_date - relativedelta(months=1)

            for move in moves:
                if earliest_date.date() < move.invoice_date <= curr_display_date.date():
                    partner_name = move.partner_id.name
                    if partner_name not in partner_tracking:
                        partner_tracking[partner_name] = {times: 0 for times in timeframe}
                        partner_totals[partner_name] = {'total': 0, 'companyID': move.partner_id.company_registry or ''}
                    curr_key = move.invoice_date.strftime("%Y-%m")
                    if curr_key in partner_tracking[partner_name]:
                        partner_tracking[partner_name][curr_key] += move.amount_residual
                        partner_totals[partner_name]['total'] += move.amount_residual
            
            row = 2
            for partner, values in partner_tracking.items():
                sheet.write(f"A{row + 1}", partner, table_value_format)
                sheet.write(f"B{row + 1}", partner_totals[partner]['companyID'], table_value_format)
                start_col = 2
                for months, amount in values.items():
                    sheet.write(row, start_col, '{:,.2f}'.format(amount) if amount != 0 else '', table_number_format)
                    start_col += 1
                sheet.write(row, start_col, '{:,.2f}'.format(partner_totals[partner]['total']), table_number_format)
                start_col += 1
                sheet.write(row, start_col, '{:,.2f}'.format(partner_totals[partner]['total']), table_number_format)
                start_col += 1
                sheet.write(row, start_col, "", table_number_format)
                row += 1
            
            months_totals = defaultdict(int)
            for values in partner_tracking.values():
                for month, month_total in values.items():
                    months_totals[month] += month_total
            
            sheet.write(row, 0, '', table_value_format)
            sheet.write(row, 1, '', table_value_format)

            total_col = 2
            for _, totals in months_totals.items():
                sheet.write(row, total_col, '{:,.2f}'.format(totals), table_total_format)
                total_col += 1
            
            grand_total = sum([v['total'] for v in partner_totals.values()])
            sheet.write(row, total_col, '{:,.2f}'.format(grand_total), table_total_format)
            total_col += 1
            sheet.write(row, total_col, '{:,.2f}'.format(grand_total), table_total_format_with_bold)
            total_col += 1
            sheet.write(row, total_col, "", table_total_format_with_bold)
        

        else:
            sheet.set_column(0, 0, 33.57)
            sheet.set_column(1, 1, 5.14)
            sheet.set_column(2, 2, 8.14)
            sheet.set_column(3, 3, 5.86)
            sheet.set_column(4, 4, 7.14)
            for col in range(5, 18):
                sheet.set_column(col, col, 11.57)
            
            sheet.merge_range("A1:E1", '美元客戶', first_row_format)
            sheet.write("F1", '本月', first_row_format)

            for col in range(6, 17):
                sheet.write(0, col, f"{month_mapping[col - 5]}個月期", first_row_format)
            sheet.write("R1", "合計應收款", first_row_format)

            sheet.write("A2", "公司名稱", second_row_format)
            sheet.write("B2", "代號", second_row_format)
            sheet.write("C2", "地區", second_row_format)
            sheet.write("D2", "數期", second_row_format)
            sheet.write("E2", "品牌商", second_row_format)
            curr_month_last = calendar.monthrange(today.year, today.month)[1]
            curr_display_date = datetime(today.year, today.month, curr_month_last)
            sheet.write("F2", curr_display_date.strftime("%Y/%m/%d"), second_row_month_format)

            partner_tracking, partner_totals = dict(), dict()
            timeframe = [curr_display_date.strftime("%y-%m")]

            for col in range(6, 17):
                prev_date = today - relativedelta(months=col-5)
                prev_year, prev_month = prev_date.year, prev_date.month
                prev_day = calendar.monthrange(prev_year, prev_month)[1]

                display_date = datetime(prev_year, prev_month, prev_day)
                timeframe.append(display_date.strftime("%Y-%m"))
                sheet.write(1, col, display_date.strftime("%Y/%m/%d"), second_row_month_format)
            sheet.write("R2", "USD", second_row_month_format)

            earliest_date = display_date - relativedelta(months=1)

            for move in moves:
                if earliest_date.date() < move.invoice_date <= curr_display_date.date():
                    partner_name = move.partner_id.name
                    if partner_name not in partner_tracking:
                        partner_tracking[partner_name] = {times: 0 for times in timeframe}
                        partner_totals[partner_name] = {'total': 0, 'companyID': move.partner_id.company_registry or '', "country": move.partner_id.country_id.name or '', "payment_term": move.partner_id.property_payment_term_id.name or ''}
                    curr_key = move.invoice_date.strftime("%Y-%m")
                    if curr_key in partner_tracking[partner_name]:
                        partner_tracking[partner_name][curr_key] += move.amount_residual
                        partner_totals[partner_name]['total'] += move.amount_residual
            
            row = 2
            for partner, values in partner_tracking.items():
                sheet.write(f"A{row + 1}", partner, table_value_format)
                sheet.write(f"B{row + 1}", partner_totals[partner]['companyID'], table_value_format)
                sheet.write(f"C{row + 1}", partner_totals[partner]['country'], table_value_format)
                sheet.write(f"D{row + 1}", partner_totals[partner]['payment_term'], table_value_format)
                sheet.write(f"E{row + 1}", '', table_value_format)
                start_col = 5
                for months, amount in values.items():
                    sheet.write(row, start_col, '{:,.2f}'.format(amount) if amount != 0 else '', table_number_format)
                    start_col += 1
                sheet.write(row, start_col, '{:,.2f}'.format(partner_totals[partner]['total']), table_number_format)
                row += 1
            
            months_totals = defaultdict(int)
            for values in partner_tracking.values():
                for month, month_total in values.items():
                    months_totals[month] += month_total
            
            for col in range(5):
                sheet.write(row, col, '', table_value_format)

            total_col = 5
            for _, totals in months_totals.items():
                sheet.write(row, total_col, '{:,.2f}'.format(totals), table_total_format)
                total_col += 1
            
            grand_total = sum([v['total'] for v in partner_totals.values()])
            sheet.write(row, total_col, '{:,.2f}'.format(grand_total), table_total_format)
            



                    
                


            
            

        
            




