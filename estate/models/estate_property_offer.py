from odoo import models, fields, api
from datetime import timedelta

class estate_property_tag(models.Model):
    _name = "estate_property_offer"
    _description = "offers of properties"

    price = fields.Float()
    status = fields.Selection([('accepted','Accepted'),('refused','Refused')],copy=False)
    partner_id = fields.Many2one("red.partner", required=True)
    property_id = fields.Many2one("estate_property", required=True)
    vality = fields.Integer(default=7)
    date_deadline = fields.Date()

    @api.depends("vality")
    def _deadline(self):
        if self.vality and self.create_date:
            self.date_deadline = self.create_date.date() + timedelta(days=self.vality)
        else:
            self.date_deadline = self.date_deadline

    @api.depends("date_deadline")
    def _vality(self):
        if self.date_deadline and self.create_date:
            self.vality = self.date_deadline() - timedelta(days=self.create_date)
        else:
            self.vality = self.vality