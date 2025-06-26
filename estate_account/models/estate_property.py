from odoo import fields, models, Command

class estate_property(models.Model):
    _inherit = "estate_property"

    def sold_action(self):
        selling_price = self.selling_price
        self.env['account.move'].create({
            'partner_id': self.salesperson.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                Command.create({
                    'name': 'Comisión del 6%',
                    'quantity': 1,
                    'price_unit': selling_price * 0.06
                }),
                Command.create({
                    'name': 'Gastos administrativos',
                    'quantity': 1,
                    'price_unit': 100.00
                }),
            ]
        })
        return super().sold_action()
