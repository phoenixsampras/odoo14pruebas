from odoo import api, models, fields
from odoo import tools


class product_template(models.Model):
    _inherit = "product.template"

    as_qty_min = fields.Float(string='Stock minimo', help='stock minimo de producto.')
    as_qty_security = fields.Float(string='Stock de seguridad', help='cantidad de seguridad de producto.')

    @api.depends('as_qty_min','as_qty_security')
    def compute_qty_security(self):
        for sale in self:
            valor = float(sale.as_qty_min)
            product_product= self.env['product.product'].sudo().search([('product_tmpl_id', '=', sale.id)],limit=1)
            product_quant = self.env['stock.quant'].sudo().search([('product_id', '=', product_product.id)])
            for quant in product_quant:
                if quant.quantity <= valor:
                    quant.write({
                        'as_low_stock': True
                    })
                else:
                    quant.write({
                        'as_low_stock': False
                    })

            sale.as_qty_min_total=sale.as_qty_min+sale.as_qty_security

    as_qty_min_total = fields.Float(string='Stock suma', help='stock minimo de producto.',compute='compute_qty_security',store=True)