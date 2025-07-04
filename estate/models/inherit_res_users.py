from odoo import fields, models

class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate_property", "salesperson", domain="[('state', 'in', ('new', 'offer_recived'))]")