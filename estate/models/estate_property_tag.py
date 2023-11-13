from odoo import models, fields, api

class Tag(models.Model):
    _name='estate_property_tag'
    _description='this is tag for estate feature '

    name=fields.Char('Feature Tags')
