from odoo import models, fields
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta

class estate_property(models.Model):
    _name = "estate_property"
    _description = "property information"

    name = fields.Char(required = True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new','New'),
        ('offer_recived','Offer Recived'),
        ('offer_accepted','Offer Accepted'),
        ('sold','Sold'),
        ('cancelled','Cancelled')
    ], default='new', required=True, copy=False)
    property_type_id = fields.Many2one("estate_property_type", string="Property type")
    salesperson = fields.Many2one('res.users', string='Salesperson', copy=False, default=lambda self: self.env.user)
    buyer = fields.Char()
    tag_ids = fields.Many2many("estate_property_tag")
    offer_ids = fields.One2many(comodel="estate_property_offer")