from odoo import models, fields, api,SUPERUSER_ID
from odoo.exceptions import UserError
# from odoo.exceptions import UserError
from datetime import date, timedelta

class Estate_Property(models.Model):
    _name='estate_property'
    _description='Estate Property'

    name=fields.Char('Title',required=True)
    description=fields.Text(string='Description')
    postcode=fields.Char(string='Postcode')
    date_availability=fields.Selection(selection='date_selection',string='Available From',copy=False)
    expected_price=fields.Float(string='Expected Price',required=True)
    selling_price=fields.Float(string='Selling Price',readonly=True,copy=False)

    bedrooms=fields.Integer(string='Bedroom',default=2)
    living_area=fields.Integer(string='Living Area(sqm)')
    facades=fields.Integer(string='Facades')
    garden=fields.Boolean(string='Garden')
    garage=fields.Boolean(string='Garage')
    garden_area=fields.Integer(string='Garden Area(sqm)')
    garden_orientation=fields.Selection([('north','North'),('south','South'),('east','East'),('west','West')],string='Garden Orientation')
    state=fields.Selection([('new','New'),('offer received','Offer Received'),('offer accepted','Offer Accepted'),('sold','Sold'),('canceled','Canceled')],string='State',required=True,copy=False,default='new')

    # to hide a record, we use Model.active(boolean type)
    active=fields.Boolean(string='Active')

    # many2one fields
    property_type_id=fields.Many2one('estate_property_type', string='Property Type')
    saleman_id=fields.Many2one('res.users',string='Saleman', default=lambda self: self.env.user)
    buyer_id=fields.Many2one('res.partner',string='Buyer',copy=False)

    # many2many fields
    tags_ids=fields.Many2many('estate_property_tag')

    # one2many fields
    offer_ids=fields.One2many('estate_property_offer','property_id',string='Offers')

    # def user_err(self,message):
    #     return odoo.exceptions.UserError(message)

    # action button for estate status use odoo.exceptions to raise exceptions
    def action_change_status_sold(self):
        for each in self:
            if each.state != 'sold' and each.state != 'canceled':
                each.state = 'sold'
            else:
                if each.state == 'canceled':
                    raise UserError('canceled property can not be sold')
    
    def action_change_status_canceled(self):
        for each in self:
            if each.state != 'sold' and each.state != 'canceled':
                each.state = 'canceled'
            else:
                if each.state == 'sold':
                    raise UserError('sold property can not be canceled')

    # compute field
    @api.model
    def date_selection(self):
        day1=date.today()
        numofdays=100
        list=[day1 - timedelta(days=x) for x in range(numofdays)]
        listday=[]
        for i in range(len(list)):
            listday.append((str(list[i]),str(list[i])))
            i=+1
        return listday

    best_offer=fields.Float(compute='_compute_best_offer')
    @api.depends('offer_ids')
    def _compute_best_offer(self):

        for record in self:
            # best_list=[]
            # for offer in record.offer_ids:
            #     best_list.append(offer.price)
            best_list=record.offer_ids.mapped('price')
            if len(best_list)>0:
                record.best_offer=max(best_list)
            else:
                record.best_offer=0

    @api.onchange("garden","garden_area","garden_orientation")
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""
