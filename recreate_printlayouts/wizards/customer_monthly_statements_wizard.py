from collections import defaultdict
from odoo.exceptions import ValidationError
from odoo import _, fields, models
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.tools import date_utils
import json
import logging

_logger = logging.getLogger(__name__)

class CustomerMonthlyStatements(models.TransientModel):
    _name = "account.customer.monthly.statements"
    _description = "Customer Monthly Statements"

    partner_id = fields.Many2one(comodel_name="res.partner", string="Customer", required=True, store=True)
    start_date = fields.Date(string='Start Date', default=lambda self: self._get_default_date(), store=True, required=True)
    end_date = fields.Date(string='End Date', default=datetime.today(), store=True, required=True)
    

    def _get_default_date(self):
        return (datetime.today() - relativedelta(years=1)).date()

    def action_button(self):
        _logger.info(self)
        return self.env.ref('recreate_printlayouts.action_adap_monthly_statements').report_action(self)
    
    def _get_report_filename(self):
        self.ensure_one()
        name = f"{self.partner_id.name} - Monthly Statement {self.start_date.strftime("%Y-%m-%d")} - {self.end_date.strftime("%Y-%m-%d")}"
        return name