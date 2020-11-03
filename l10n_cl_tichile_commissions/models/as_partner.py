# -*- coding: utf-8 -*-

from odoo import models,fields,api
    
class as_res_partner(models.Model):
    _inherit="res.partner"
    
    as_comissions = fields.Float(string="Comisión (%)")
    as_comissions_monto = fields.Float(string="Comisión Monto Fijo")