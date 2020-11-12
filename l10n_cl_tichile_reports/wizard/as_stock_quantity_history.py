# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class StockQuantityHistory(models.TransientModel):
    _inherit = 'stock.quantity.history'
    _description = 'Stock Quantity History inherit'

    bajo_stock = fields.Boolean(string="Bajo Stock", help="Choose to analyze the current inventory or from a specific date in the past.")

    def open_at_date(self):
        tree_view_id = self.env.ref('stock.view_stock_product_tree').id
        form_view_id = self.env.ref('stock.product_form_view_procurement_button').id
        domain = [('type', '=', 'product')]
        product_id = self.env.context.get('product_id', False)
        product_tmpl_id = self.env.context.get('product_tmpl_id', False)
        if not self.bajo_stock:
            if product_id:
                domain = expression.AND([domain, [('id', '=', product_id)]])
            elif product_tmpl_id:
                domain = expression.AND([domain, [('product_tmpl_id', '=', product_tmpl_id)]])
            # We pass `to_date` in the context so that `qty_available` will be computed across
            # moves until date.
            action = {
                'type': 'ir.actions.act_window',
                'views': [(tree_view_id, 'tree'), (form_view_id, 'form')],
                'view_mode': 'tree,form',
                'name': _('Products'),
                'res_model': 'product.product',
                'domain': domain,
                'context': dict(self.env.context, to_date=self.inventory_datetime),
            }
        else:
            tree_view_id = self.env.ref('stock.view_stock_quant_tree').id
            #form_view_id = self.env.ref('stock.product_form_view_procurement_button').id, (form_view_id, 'form')
            # We pass `to_date` in the context so that `qty_available` will be computed across
            # moves until date.

            action = {
                'type': 'ir.actions.act_window',
                'views': [(tree_view_id, 'tree')],
                'view_mode': 'tree',
                'name': _('Products'),
                'res_model': 'stock.quant',
                'domain': self.compute_low_stock(),
                'context': dict(self.env.context),
            }
        return action


    def compute_low_stock(self):
        product_quant = self.env['stock.quant'].sudo().search([])
        bajo_stock=[]
        for quant in product_quant:
            if quant.location_id.usage =='internal':
                stock_min = quant.product_id.product_tmpl_id.as_qty_min + quant.product_id.product_tmpl_id.as_qty_security
                if quant.quantity <= stock_min:
                    bajo_stock.append(quant.id)
        return "[('id','in',"+str(tuple(bajo_stock))+")]"