# # -*- coding: utf-8 -*-

import datetime
from datetime import datetime
import pytz
from odoo import models,fields
from datetime import datetime, timedelta
from time import mktime
import time
import operator
import itertools
from datetime import datetime, timedelta
from dateutil import relativedelta
import xlwt
from xlsxwriter.workbook import Workbook
from odoo.tools.translate import _
import base64
import locale
from odoo import netsvc
from odoo import tools
from time import mktime
import logging
from odoo import api, models, _
from odoo.exceptions import UserError

class as_sales_libro_ventas_tax(models.AbstractModel):
    _name = 'report.l10n_cl_tichile_report.ventas_producto.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):     
        sheet = workbook.add_worksheet('ventas por vendedor')
        #estilos
        titulo1 = workbook.add_format({'font_size': 16,'font_name': 'Lucida Sans', 'align': 'center', 'bold':True,'bg_color': '#ffffff'})
        titulo2 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold':True })
        titulo3 = workbook.add_format({'font_size': 9, 'align': 'left', 'bold':True })
        titulo3_number = workbook.add_format({'font_size': 10, 'align': 'right', 'bold':True, 'num_format': '#,##0.00' })
        titulo4 = workbook.add_format({'font_size': 11, 'font_name': 'Lucida Sans','align': 'center','bg_color': '#ffffff', 'bold':True })
        titulo10 = workbook.add_format({'font_size': 10, 'align': 'right','bg_color': '#ffffff', 'bold':True })
        titulo5 = workbook.add_format({'font_size': 10, 'align': 'center', 'right': False, 'bold':False })
        titulo9 = workbook.add_format({'font_size': 10, 'align': 'right', 'right': False, 'bold':False })
        titulo6 = workbook.add_format({'font_size': 10, 'align': 'center', 'right': False, 'bold':False, 'color': 'red'})
        titulo12 = workbook.add_format({'font_size': 10, 'align': 'right', 'right': False, 'bold':False, 'color': 'red'})
        titulo7 = workbook.add_format({'font_size': 10, 'align': 'left', 'right': False, 'bold':False})
        titulo8 = workbook.add_format({'font_size': 10, 'align': 'right', 'right': False, 'bold':False})

        number_left = workbook.add_format({'font_size': 9, 'align': 'left', 'num_format': '#,##0.00','bg_color': '#ffffff'})
        number_right = workbook.add_format({'font_size': 9, 'align': 'right', 'num_format': '#,##0.00','bg_color': '#ffffff'})
        number_right_bold = workbook.add_format({'font_size': 9, 'align': 'right', 'num_format': '#,##0.00', 'bold':True,'bg_color': '#ffffff'})
        number_right_col = workbook.add_format({'font_size': 9, 'align': 'right', 'num_format': '#,##0.00','bg_color': 'silver'})
        number_center = workbook.add_format({'font_size': 9, 'align': 'center', 'num_format': '#,##0.00','bg_color': '#ffffff'})
        number_right_col.set_locked(False)

        letter1 = workbook.add_format({'font_size': 9, 'align': 'left','bg_color': '#ffffff'})
        letter2 = workbook.add_format({'font_size': 9, 'align': 'left', 'bold':True,'bg_color': '#ffffff'})
        letter3 = workbook.add_format({'font_size': 9, 'align': 'right','font_size': 11,'font_name': 'Lucida Sans','bg_color': '#ffffff'})
        letter4 = workbook.add_format({'font_size': 9, 'align': 'left', 'bold': True,'bg_color': '#ffffff'})
        letter4C = workbook.add_format({'font_size': 9, 'align': 'left', 'bold': True,'color':'#000000','font_name': 'Lucida Sans','bg_color': '#ffffff' })
        letter4F = workbook.add_format({'font_size': 9, 'align': 'left', 'bold': True,'color': '#FFFFFF','bg_color': '#ffffff','font_name': 'Lucida Sans',})
        letter4G = workbook.add_format({'font_size': 9, 'align': 'left', 'bold': True,'color': '#000000','bg_color': '#f0f0f0','font_name': 'Lucida Sans',})
        letter4S = workbook.add_format({'font_size': 9, 'align': 'left', 'bold': True,'bg_color': '#ffffff'})
        letter41S = workbook.add_format({'font_size': 9, 'align': 'left','bg_color': '#ffffff'})
        letter41Si = workbook.add_format({'font_size': 9, 'align': 'right','bg_color': '#ffffff'})
        letter41Sr = workbook.add_format({'font_size': 9, 'align': 'left','color': 'red','bg_color': '#ffffff'})
        letter_locked = letter3
        letter_locked.set_locked(False)

        # Aqui definimos en los anchos de columna
        sheet.set_column('A:A',20, letter1)
        sheet.set_column('B:B',20, letter1)
        sheet.set_column('C:C',20, letter1)
        sheet.set_column('D:D',20, letter1)
        sheet.set_column('E:E',20, letter1)
        sheet.set_column('F:F',20, letter1)
        sheet.set_column('G:G',20, letter1)
        sheet.set_column('H:H',20, letter1)
        sheet.set_column('I:I',20, letter1)
        sheet.set_column('J:J',20, letter1)
        sheet.set_column('K:K',20, letter1)
        sheet.set_column('L:L',20, letter1)
        sheet.set_column('M:M',20, letter1)
        # sheet.set_column('N:N',12, letter1)
        # sheet.set_column('O:O',12, letter1)
        # sheet.set_column('P:P',5, letter1)
        # sheet.set_column('Q:Q',5, letter1)
        # sheet.set_column('R:R',5, letter1)
        # sheet.set_column('S:S',5, letter1)
        # sheet.set_column('T:T',5, letter1)
        # sheet.set_column('U:U',5, letter1)
        # sheet.set_column('V:V',10, letter1)

        # Titulos, subtitulos, filtros y campos del reporte
        fecha_inicial = datetime.strptime(str(data['form']['start_date']), '%Y-%m-%d').strftime('%d/%m/%Y')
        fecha_final = datetime.strptime(str(data['form']['end_date']), '%Y-%m-%d').strftime('%d/%m/%Y')
        sheet.merge_range('A1:I1', 'Detalle de Transferencias Ingresos', titulo1)
        sheet.merge_range('A2:I2', fecha_inicial +' - '+ fecha_final, titulo4)
        fecha = (datetime.now() - timedelta(hours=4)).strftime('%d/%m/%Y %H:%M:%S')
        sheet.merge_range('A3:D3', self.env.user.company_id.name, letter4)



        filas=7
        worksheet.write(filas,0,'Nro Importacion',titulo2)
        worksheet.write(filas,1,'Ref Proveedor',titulo2)
        worksheet.write(filas,2,'Fecha',titulo2)
        worksheet.write(filas,3,'Almacen Origen',titulo2)
        worksheet.write(filas,4,'Almacen Destino',titulo2)
        worksheet.write(filas,5,'Importe $us.',titulo2)
        sheet.freeze_panes(6, 0)
        filas+=1
       
        # Preparando variables para cada casod e consulta
        consulta_clientes = ('''
            SELECT
            sp.id AS id_picking
            FROM stock_picking AS sp
            JOIN stock_picking_type AS spt ON spt.id = sp.picking_type_id
            WHERE spt.code = 'internal' and sp.state in ('done')
            AND ((sp.min_date AT TIME ZONE 'UTC' AT TIME ZONE 'BOT')::timestamp::date) BETWEEN %s AND %s
            AND sp.location_dest_id = %s
        ''',([self_browse.start_date,self_browse.end_date,self_browse.location.id]))
        self.env.cr.execute(consulta_clientes)
        # AND (sp.location_id = %s OR sp.location_dest_id = %s) # Colocar si es para cualquier posicion
        lista_id_picking = [i for i in cr.fetchall()]
        lista_ids  = []
        for lista in lista_id_picking:
            lista_ids.append(lista[0])
        picking = self.env['stock.picking'].sudo().search([('id', '=',lista_ids)])
        for producto in picking:
            struct_time_convert = time.strptime(picking.min_date, '%Y-%m-%d %H:%M:%S')
            date_time_convert = datetime.fromtimestamp(mktime(struct_time_convert))
            date_time_convert = date_time_convert - timedelta(hours = 4)
            fecha_picking = date_time_convert.strftime('%d/%m/%Y')
            fila += 1
            valor_importe = obtener_total_importe_picking(cr,uid,picking.id)
            worksheet.write(fila,0,picking.origin,datos1)
            worksheet.write(fila,1,picking.name,datos1)
            worksheet.write(fila,2,fecha_picking,datos2)
            worksheet.write(fila,3,picking.location_id.name,datos1)
            worksheet.write(fila,4,picking.location_dest_id.name,datos1)
            worksheet.write(fila,5,valor_importe,datos3)
            total_importe_dolares += valor_importe

        fila += 1
        worksheet.write_merge(fila,fila,0,4,'Total General',totales2)
        worksheet.write(fila,5,total_importe_dolares,totales3)
