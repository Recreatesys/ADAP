from collections import defaultdict
from odoo.exceptions import ValidationError
from odoo import _, fields, models
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.tools import date_utils
import json
import logging

_logger = logging.getLogger(__name__)

class AdapMonthlyStatementWizard(models.TransientModel):
    _name = "adap.monthly.statement.wizard"
    _description = "Adap Monthly Statements"

    month = fields.Selection(string="Month", selection=[
        ("January", "January"),
        ("Febuary", "Feburary"),
        ("March", "March"),
        ("April", "April"),
        ("May", "May"),
        ("June", "June"),
        ("July", "July"),
        ("August", "August"),
        ("September", "September"),
        ("October", "October"),
        ("November", "November"),
        ("December", "December")
    ], required=True)

    def action_button(self):
        return self.env.ref('recreate_printlayouts.action_adap_inter_statements').report_action(self)
    

    def _get_report_filename(self):
        self.ensure_one()
        name = f"{self.month} - {datetime.now().year} Statement"
        return name