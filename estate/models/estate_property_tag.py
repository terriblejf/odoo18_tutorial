from odoo import models, fields

class estate_property_tag(models.Model):
    _name = "estate_property_tag"
    _description = "tags of property"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('unique_tag_name', 'unique(name)', 'That tag does exist alredy.')
    ]