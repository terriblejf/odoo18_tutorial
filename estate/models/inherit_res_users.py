from odoo import fields, models

class inherit_res_users(models.Model):
    _inherit = "res_users"

    property_ids = fields.One2many("estate_property", "salesperson", domain="[('state', 'in', ('new', 'offer_recived'))]")