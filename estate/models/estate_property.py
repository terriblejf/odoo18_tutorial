from odoo import models, fields, api
from odoo.exceptions import UserError
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
    offer_ids = fields.One2many("estate_property_offer", "property_id")
    total_area = fields.Integer(compute="_total_area")
    best_price = fields.Float(compute="_best_price")

    @api.depends("living_area", "garden_area")
    def _total_area(self):
        self.total_area = self.living_area + self.garden_area
    
    @api.depends("offer_ids.price")
    def _best_price(self):
        if self.offer_ids:
            self.best_price = max(self.offer_ids.mapped('price'))
        else:
            self.best_price = self.best_price

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = False
            self.garden_orientation = False

    def sold_action(self):
        if self.state == 'sold':
            raise UserError("The property is already sold")
        elif self.state == 'cancelled':
            raise UserError("The property is cancelled")
        else:
            self.state = 'sold'
        return True
    
    def cancel_action(self):
        if self.state == 'sold':
            raise UserError("The property is sold")
        elif self.state == 'cancelled':
            raise UserError("The property is alredy cancelled")
        else:
            self.state = 'cancelled'
        return True
            
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'Only positive values.'),
        ('check_selling_price', 'CHECK(selling_price > 0)', 'Only positive values.'),
    ]

    