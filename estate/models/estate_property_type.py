from odoo import models, fields, api

class Estate_property_type(models.Model):
    _name='estate_property_type'
    _description='Estate Property Type'

    name=fields.Char(string='Property Type', required=True)
