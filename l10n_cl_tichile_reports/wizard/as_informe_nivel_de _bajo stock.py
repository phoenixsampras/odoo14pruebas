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

class as_kardex_nivel_wiz(models.TransientModel):
    _name="as.informe.nivel.bajo stock"
    _description = "Warehouse Reports by AhoraSoft"
    
    start_date  = fields.Date(string="Fecha Inicio", default=lambda *a: (datetime.now() - timedelta(hours = 4)).strftime('%Y-%m-%d'), required=True)
    end_date    = fields.Date(string="Fecha Final",  default=lambda *a: (datetime.now() - timedelta(hours = 4)).strftime('%Y-%m-%d'), required=True)
    user_ids = fields.Many2many('res.users', string="Usuario")
    partner_ids  = fields.Many2many('res.partner', string="Clientes")
    location_ids = fields.Many2many('stock.location', string='Almacenes', domain="[('usage', '=', 'internal'),('as_type_almacen', '=', False)]")
    city_ids = fields.Many2many('res.country.state', string='Ciudad')


    @api.multi
    def export_pdf(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'as.informe.nivel.bajo stock'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        return self.env.ref('l10n_cl_tichile_reports.as_informe_nivel_bajo stock_pdf').report_action(self, data=datas)

    @api.multi
    def export_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'as.informe.nivel.bajo stock'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        if context.get('xls_export'):
            return self.env.ref('l10n_cl_tichile_reports.as_informe_nivel_bajo stock').report_action(self, data=datas)
 