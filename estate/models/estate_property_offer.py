from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta, date


class estate_property_tag(models.Model):
    _name = "estate_property_offer"
    _description = "offers of properties"
    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False, readonly=True
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate_property", required=True)
    vality = fields.Integer()
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True, readonly=True)

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'Only positive values.')
    ]
    
    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res.property_id.state == 'new':
            res.property_id.state = 'offer_recived'
        return res
    
    @api.depends("vality")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = date.today() + timedelta(days=record.vality)
        
    def _inverse_date_deadline(self):
        for record in self:
            record.vality = (record.date_deadline - date.today()).days

    
    def accept_action(self):
        for record in self:
            for oferta in record.property_id.offer_ids:
                if oferta.status == "accepted":
                    raise UserError("There is an offer accepted alredy")
            if record.status == False:
                record.status = "accepted"
                record.property_id.salesperson = record.partner_id.id
                record.property_id.selling_price = record.price
                record.property_id.state = 'offer_accepted'
            return True

    def refuse_action(self):
        for record in self:
            if record.status == False:
                record.status = "refused"
            return True
        
