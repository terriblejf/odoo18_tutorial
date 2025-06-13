from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta, date

class estate_property_tag(models.Model):
    _name = "estate_property_offer"
    _description = "offers of properties"

    price = fields.Float(required=True)
    status = fields.Selection([('accepted','Accepted'),('refused','Refused')],copy=False, readonly=True)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate_property", required=True)
    vality = fields.Integer()
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'Only positive values.')
    ]

    @api.depends("vality")
    def _compute_date_deadline(self):
        if self.vality > 0:
            self.date_deadline = date.today() + timedelta(days=self.vality)
        else:
            self.date_deadline = self.date_deadline

    def _inverse_date_deadline(self):
        self.vality = 10

    def accept_action(self):
        ofertas = self.env['estate.property.offer'].search([])
        for oferta in ofertas:
            if oferta.status == 'accepted':
                raise UserError("There is an offer accepted alredy")
                return True
        if self.status == False:
            self.status = 'accepted'
        return True
    
    def refuse_action(self):
        if self.status == False:
            self.status = 'refused'
        return True
            