# -*- coding: utf-8 -*-
##############################################################################

from datetime import datetime, timedelta
import xlwt
from xlsxwriter.workbook import Workbook
from odoo.exceptions import UserError
from odoo.tools.translate import _
import base64
from odoo import netsvc
from odoo import tools
from time import mktime
import logging
from datetime import datetime
from odoo import api, fields, models

class as_ventas_productos(models.TransientModel):
    _name="as.ventas.productos"
    _description = "Reporte de ventas por producto	Excel"
    
    start_date  = fields.Date(string="Fecha Inicio", default=lambda *a: (datetime.now() - timedelta(hours = 4)).strftime('%Y-%m-%d'), required=True,ondelete='cascade')
    end_date    = fields.Date(string="Fecha Final",  default=lambda *a: (datetime.now() - timedelta(hours = 4)).strftime('%Y-%m-%d'), required=True,ondelete='cascade')
    user_ids = fields.Many2many('res.users', string="Usuario",ondelete='cascade')
    partner_ids  = fields.Many2many('res.partner', string="Clientes",ondelete='cascade')
    location_ids = fields.Many2many('stock.location', string='Almacenes', domain="[('usage', '=', 'internal')]",ondelete='cascade')
    city_ids = fields.Many2many('res.country.state', string='Ciudad',ondelete='cascade')


    def export_pdf(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'as.ventas.productos'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        return self.env.ref('l10n_cl_tichile_reports.as_ventas_por_producto_pdf').report_action(self, data=datas)

    def export_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'as.ventas.productos'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        if context.get('xls_export'):
            return self.env.ref('l10n_cl_tichile_reports.as_ventas_por_producto_report').report_action(self, data=datas)
 