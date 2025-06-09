from odoo import models, fields, api
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

class estate_property_tag(models.Model):
    _name = "estate_property_offer"
    _description = "offers of properties"

    price = fields.Float()
    status = fields.Selection([('accepted','Accepted'),('refused','Refused')],copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate_property", required=True)
    vality = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_deadline", inverse="_vality")

    @api.depends("vality")
    def _deadline(self):
        if self.vality and self.create_date:
            self.date_deadline = self.create_date.date() + relativedelta(days=self.vality)
        else:
            self.date_deadline = self.date_deadline

    @api.depends("date_deadline")
    def _vality(self):
        if self.date_deadline and self.create_date:
            self.vality = self.date_deadline() - relativedelta(days=self.create_date)
        else:
            self.vality = self.vality