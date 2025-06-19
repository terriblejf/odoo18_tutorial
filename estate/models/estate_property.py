from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class estate_property(models.Model):
    _name = "estate_property"
    _description = "property information"
    _order = "id desc"

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
    ], default='new', required=True, copy=False, readonly=True, computed="_offers_state")
    property_type_id = fields.Many2one("estate_property_type", string="Property type", options="{'no_create': True, 'no_create_edit': True}")
    salesperson = fields.Many2one('res.partner', string='Salesperson', copy=False)
    buyer = fields.Char()
    tag_ids = fields.Many2many("estate_property_tag")
    offer_ids = fields.One2many("estate_property_offer", "property_id")
    total_area = fields.Integer(compute="_total_area")
    best_price = fields.Float(compute="_best_price")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'Only positive values.'),
        ('check_selling_price', 'CHECK(selling_price > 0)', 'Only positive values.')
    ]
    
    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            min = record.expected_price/100*90
            if float_compare(min, record.selling_price, precision_digits=2) == 1:
                raise ValidationError("Offer price must be at least 90 percent of the expected price")
            
    @api.depends("offer_ids.status")
    def _offers_state(self):
        for record in self:
            if record.offer_ids:
                if any(offer.status == 'accepted' for offer in record.offer_ids):
                    record.state = 'offer_accepted'
                else:
                    record.state = 'offer_recived'
                    

    @api.depends("living_area", "garden_area")
    def _total_area(self):
        self.total_area = self.living_area + self.garden_area
    
    @api.depends("offer_ids.price")
    def _best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = record.best_price

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
            sold = False
            for offer in self.offer_ids:
                if offer.status == 'accepted':
                    sold = True
            if sold:
                self.state = 'sold'
            else:
                raise UserError("Accept an offer before sold")
        return True
    
    def cancel_action(self):
        if self.state == 'sold':
            raise UserError("The property is sold")
        elif self.state == 'cancelled':
            raise UserError("The property is alredy cancelled")
        else:
            self.state = 'cancelled'
        return True
            
    

    