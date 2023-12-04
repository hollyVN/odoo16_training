from odoo import models, fields, api

class Estate_property_type(models.Model):
    _name='estate_property_type'
    _description='Estate Property Type'
    _order='name'

    name=fields.Char(string='Property Type', required=True)

    _sql_constraints = [
            ('type_name_constraints','UNIQUE(name)','pls use another name')
            ]

    property_ids = fields.One2many('estate_property', 'property_type_id')
