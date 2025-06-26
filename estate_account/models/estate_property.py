from odoo import fields, models

class estate_property(models.Model):
    _inherit = "estate_property"

def sold_action(self):
    return super().sold_action()