from odoo import models, fields

class estate_property_type(models.Model):
    _name = "estate_property_type"
    _description = "types of property"

    name = fields.Char(required=True)