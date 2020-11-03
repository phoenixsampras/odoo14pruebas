# -*- coding: utf-8 -*-

from odoo import tools
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class PricelistItemC(models.Model):
    _name = "as.history.commissions"
    _description = "modulo para llevar historico de comisiones"

    @api.depends('sale_id','aty_invoice')
    def _get_invoiced_ver(self):
        for history in self:
            if history.sale_id:
                for order in history.sale_id:
                    invoices = order.order_line.invoice_lines.move_id.filtered(lambda r: r.type in ('out_invoice', 'out_refund'))
                    history.invoice_ids = invoices
                    history.fecha_venta = order.date_order
                    history.aty_invoice = len(history.invoice_ids)
                    if history.aty_invoice > 0:
                        history.invoice_name = history.invoice_ids[0].name
                        history.fecha_factura = history.invoice_ids[0].invoice_date

            else:
                history.invoice_ids = []
                history.fecha_venta = datetime.now()
                history.aty_invoice = len(history.invoice_ids)

    as_comissions = fields.Float(string="Comisión (%)")
    amount_payment = fields.Float(string="Monto a Pagar")
    sale_line_id = fields.Many2one('sale.order.line', string='Linea de venta')
    sale_id = fields.Many2one('sale.order', string='Venta')
    partner_id = fields.Many2one('res.partner', string='Cliente')
    vendor_id = fields.Many2one('res.users', string='Vendedor')
    product_id = fields.Many2one('product.product', string='Producto')
    margin_puntos = fields.Float('Margin Puntos')
    aty_invoice = fields.Integer('cantidad factura',compute='_get_invoiced_ver')
    fecha_venta = fields.Datetime(string='Fecha Venta', compute="_get_invoiced_ver",store=True)
    as_pricelist_id = fields.Many2one('product.pricelist', string='Tarifa')
    state_sale = fields.Selection([('draft', 'Quotation'),('sent', 'Quotation Sent'),('sale', 'Sales Order'),('done', 'Locked'),('cancel', 'Cancelled'),], string='Estado venta', related="sale_id.state")
    as_type_modality = fields.Selection([('Clientes', 'Clientes'),('Productos', 'Productos')], default="Productos",string="Modalidad de Comisión a Aplicar")
    as_type_comissions = fields.Selection([
        ('Porcentaje (%)', 'Porcentaje (%)'),
        ('Monto Fijo', 'Monto Fijo')
    ], default="Porcentaje (%)",string="Tipo de Comisión a Aplicar")

    @api.depends('sale_id')
    def _get_invoiced_ver_default(self):
        ids = []
        for history in self:
            if history.sale_id:
                for order in history.sale_id:
                    invoices = order.order_line.invoice_lines.move_id.filtered(lambda r: r.type in ('out_invoice', 'out_refund'))
                    ids.append(invoices.id)
        return ids

    invoice_ids = fields.Many2many("account.move", string='Facturas de Cliente', compute="_get_invoiced_ver",default=_get_invoiced_ver_default)
    invoice_name = fields.Char(string='Facturas de Cliente', related='invoice_ids.name',store=True)
