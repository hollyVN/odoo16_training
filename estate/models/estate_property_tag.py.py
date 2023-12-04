from odoo import models, fields, api

class Tag(models.Model):
    _name='estate_property_tag'
    _description='this is tag for estate feature '
    _order='name'

    name=fields.Char('Feature Tags')
    color=fields.Integer('Color')

    _sql_constraints = [
            ('tag_name_constraints', 'UNIQUE(name)', 'you can not have 2 tag in same name')
            ]
