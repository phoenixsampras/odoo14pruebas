# -*- coding: utf-8 -*-

from odoo import tools
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class PricelistItemC(models.Model):
    _inherit = "product.pricelist.item"
    
    as_comissions = fields.Float(string="Comisión (%)")
