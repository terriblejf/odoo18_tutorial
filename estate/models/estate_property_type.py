from odoo import models, fields

class estate_property_type(models.Model):
    _name = "estate_property_type"
    _description = "types of property"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate_property","property_type_id")
    
    _sql_constraints = [
        ('unique_type_name', 'unique(name)', 'That property type does exist alredy.')
    ]