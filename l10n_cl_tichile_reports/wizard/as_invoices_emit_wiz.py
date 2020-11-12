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

class as_facturas_emitidas(models.TransientModel):
    _name="as.invoices.emit.wiz"
    _description = "Warehouse Reports by AhoraSoft"
    
    fecha_inicial = fields.Date('Desde la Fecha', required=True, default=lambda *a: (datetime.now() - timedelta(hours = 4)).strftime('%Y-%m-%d'))
    fecha_final = fields.Date('Hasta la Fecha', required=True, default=lambda *a: (datetime.now() - timedelta(hours = 4)).strftime('%Y-%m-%d'))
    nombre_cliente = fields.Many2one('res.partner', 'Cliente')
    as_razon_social = fields.Char('Razon Social')
    asesor = fields.Many2one('res.users', 'Comercial')
    as_tipo = fields.Selection([('ventas','Ventas'),('pos','POS'),('ambos','Ambos')] ,'Origen', required=True, default='ventas')


    def export_xls(self):
        context = self._context
        datas = {'ids': context.get('active_ids', [])}
        datas['model'] = 'as.invoices.emit.wiz'
        datas['form'] = self.read()[0]
        for field in datas['form'].keys():
            if isinstance(datas['form'][field], tuple):
                datas['form'][field] = datas['form'][field][0]
        if context.get('xls_export'):
            return self.env.ref('l10n_cl_tichile_reports.as_invoices_emit').report_action(self, data=datas)