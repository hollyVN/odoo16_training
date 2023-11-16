from odoo import models, fields, api
from datetime import datetime, timedelta

class Offer(models.Model):
    _name='estate_property_offer'
    _description='this is offer for deal'

    name=fields.Char('Offer:')
    price=fields.Float('Price:')
    partner_id=fields.Many2one('res.partner',required=True,string='Partner')
    status=fields.Selection([('accepted','Accepted'),('refuse','Refuse')],copy=False,string='Status')

    date_deadline=fields.Date(string='Deadline',compute='_compute_deadline',inverse='_inverse_deadline',store=True)
    validity=fields.Integer("Validity(days)", default=8)
    create_date=fields.Date(default=fields.Date.context_today, string='Created Day')

    # many2one fields that is inverse field with one2many at other model
    property_id=fields.Many2one('estate_property',required=True,readonly=True)

    def action_refuse(self):
        # self.write({'status':'refuse'})
        self.status='refuse'
        self.property_id.selling_price = 0
        self.property_id.buyer_id =  ""

    def action_accepted(self):
        # this is how to make "only one offer can be accepted for a given property"
        all_offer = self.env['estate_property_offer'].search([])
        for offer in all_offer:
            offer.status = 'refuse'

        self.status='accepted'
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id.id

    @api.depends("validity","create_date")
    def _compute_deadline(self):
        for each in self:
            each.date_deadline = fields.Date.from_string(each.create_date) + timedelta(days=each.validity)

    def _inverse_deadline(self):
        for each in self:
            FORMAT='%Y-%m-%d'
            each.validity = (each.date_deadline - each.create_date).days
            # each.validity = (each.date_deadline - each.create_date).days
            each.create_date = fields.Date.from_string(each.date_deadline) - timedelta(days=each.validity)

