# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from functools import partial
from itertools import groupby

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import formatLang
from odoo.osv import expression
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare
from odoo.tools.float_utils import float_round, float_is_zero
from datetime import datetime
from odoo.exceptions import UserError
from dateutil import relativedelta
from odoo.addons import decimal_precision as dp
from werkzeug.urls import url_encode

import logging
_logger = logging.getLogger(__name__)

class SaleOrderline(models.Model):
    _inherit = "sale.order.line"

    as_total_puntos = fields.Float(string="Total Puntos")
    as_discount_amount =  fields.Float(string="Monto Descuento")
    as_costo =  fields.Float(string="Costo")
    as_type =  fields.Boolean(string="%")
    as_permitido =  fields.Boolean(string="Permitido",default=True)
    as_margen_unit = fields.Float(string="Margen Unitario")
    as_total_porcentaje = fields.Float(string="Margen Unitario (%)")
    as_total_costo = fields.Float(string="Costo")
    as_total_price = fields.Float(string="Margen Unitario (%)")
    as_total_comisiones = fields.Float(string="Comisión")

    @api.onchange('as_discount_amount','discount','price_unit')
    def onchange_discount_mount(self):
        type_report = self.env['ir.config_parameter'].sudo().get_param('res_config_settings.as_type_comissions')
        modality = self.env['ir.config_parameter'].sudo().get_param('res_config_settings.as_type_modality')
        for line in self:
            line.as_costo = line.product_id.product_tmpl_id.standard_price
            line.as_costo = line.order_id.company_id.currency_id._convert(line.as_costo,line.order_id.currency_id, line.order_id.company_id, line.order_id.date_order)
            if line.as_type == True:
                #se calcula el monto de descuento
                line.as_discount_amount = (line.discount*line.price_unit)/100
            else:
                #se calcula el porcentaje de descuento
                if line.price_unit > 0.0:
                    line.discount = (line.as_discount_amount*100)/line.price_unit
            #margen Unitario
            line.as_margen_unit = (line.price_unit-line.as_discount_amount)-line.as_costo
            line.as_total_costo = line.as_costo*line.product_uom_qty
            line.as_total_price = (line.price_unit-line.as_discount_amount)*line.product_uom_qty
            line.as_total_puntos = (line.price_unit-line.as_discount_amount-line.as_costo)*line.product_uom_qty
            if line.as_total_price > 0:
                line.as_total_porcentaje = ((line.as_total_price-line.as_total_costo)/line.as_total_price)*100

          

class SaleOrder(models.Model):
    _inherit = "sale.order"

    as_debito = fields.Boolean(string="Venta inside en comisiones")
    as_comissions = fields.Float(string="Comisión (%)")

    @api.onchange('partner_id')
    def onchange_partner(self):  
        self.as_comissions = self.partner_id.as_comissions
    
    def action_cancel(self):
        if self.state == 'sale':
            self.update({'as_debito':True})
        result = super(SaleOrder, self).action_cancel()
        return result

    def action_confirm(self):
        type_report = self.env['ir.config_parameter'].sudo().get_param('res_config_settings.as_type_comissions')
        modality = self.env['ir.config_parameter'].sudo().get_param('res_config_settings.as_type_modality')
        comision = 0.0
        amount_payment = 0.0
        #creamos historial de comisiones

        for sale_line in self.order_line:
            if type_report == 'Porcentaje (%)':
                if modality == 'Clientes':
                    comision = self.as_comissions
                    amount_payment = (comision*sale_line.as_total_puntos)/100
                else:
                    comision = self.pricelist_id.item_ids.filtered(lambda r: r.product_id == sale_line.product_id).as_comissions
                    amount_payment = (comision*sale_line.as_total_puntos)/100
            else:
                query_ids = ("""
                select as_desde,as_hasta,as_comision,as_division from as_tabla_comisiones 
                where 
                as_desde <= """+str(sale_line.as_total_puntos)+""" and """+str(sale_line.as_total_puntos)+""" <= as_hasta limit 1
                """)
                self.env.cr.execute(query_ids)
                history_table = [j for j in self.env.cr.fetchall()]
                if history_table:
                    comision = float(sale_line.as_total_puntos)/float(history_table[0][1])
                    if history_table[0][3]==True:
                        amount_payment = history_table[0][2] * comision
                    else:
                        amount_payment = history_table[0][2]
            comision_history = self.env['as.history.commissions'].create(dict(
                as_comissions = comision,
                amount_payment = amount_payment,
                sale_line_id = sale_line.id,
                sale_id = self.id,
                partner_id = self.partner_id.id,
                vendor_id = self.user_id.id,
                product_id = sale_line.product_id.id,
                margin_puntos = sale_line.as_total_puntos,
                fecha_venta = self.date_order,
                as_pricelist_id = self.pricelist_id.id,
                as_type_modality = modality,
                as_type_comissions = type_report,
            )) 
        res = super(SaleOrder, self).action_confirm()
        return res
