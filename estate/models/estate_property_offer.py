from odoo import models, fields

class estate_property_tag(models.Model):
    _name = "estate_property_offer"
    _description = "offers of properties"

    price = fields.Float()
    status = fields.Selection([('accepted','Accepted'),('refused','Refused')],copy=False)
    partner_id = fields.Many2one("red.partner", required=True)
    property_id = fields.Many2one("estate_property", required=True)