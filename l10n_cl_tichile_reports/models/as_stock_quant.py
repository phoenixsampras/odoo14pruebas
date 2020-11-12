# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.tools.float_utils import float_is_zero


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    as_low_stock = fields.Boolean(string='Bajo Stock',default=False)

    @api.depends('quantity')
    def compute_low_stock(self):
        if self.quantity <= self.product_id.product_tmpl_id.as_qty_min_total:
            self.as_low_stock = True
        else:
            self.as_low_stock = False