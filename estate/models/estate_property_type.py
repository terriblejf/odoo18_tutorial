from odoo import models, fields, api

class estate_property_type(models.Model):
    _name = "estate_property_type"
    _description = "types of property"
    _order = "name"

    name = fields.Char(required=True)
    sequence = fields.Integer()
    property_ids = fields.One2many("estate_property","property_type_id")
    offer_ids = fields.One2many("estate_property_offer","property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")
    
    _sql_constraints = [
        ('unique_type_name', 'unique(name)', 'That property type does exist alredy.')
    ]
    
    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)