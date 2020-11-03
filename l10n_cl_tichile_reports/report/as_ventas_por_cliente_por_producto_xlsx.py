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
    _name ='report.l10n_cl_tichile_reports.cliente_producto.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):     
        sheet = workbook.add_worksheet('ventas por vendedor')
        #estilos
        titulo1 = workbook.add_format({'font_size': 11,'font_name': 'Lucida Sans', 'align': 'center', 'text_wrap': True, 'bold':True,'color': '#507AAA' })
        titulo2 = workbook.add_format({'font_size': 10, 'align': 'center', 'text_wrap': True, 'bottom': True, 'top': True, 'bold':True })
        titulo3 = workbook.add_format({'font_size': 9, 'align': 'left', 'text_wrap': True, 'bottom': True, 'top': True, 'bold':True })
        titulo3_number = workbook.add_format({'font_size': 10, 'align': 'right', 'text_wrap': True, 'bottom': True, 'top': True, 'bold':True, 'num_format': '#,##0.00' })
        titulo4 = workbook.add_format({'font_size': 11, 'font_name': 'Lucida Sans','align': 'center', 'text_wrap': True, 'bottom': True, 'top': True, 'left': True, 'right': True, 'bold':True })
        titulo10 = workbook.add_format({'font_size': 10, 'align': 'right', 'text_wrap': True, 'bottom': True, 'top': True, 'left': True, 'right': True, 'bold':True })
        titulo5 = workbook.add_format({'font_size': 10, 'align': 'center', 'text_wrap': True, 'bottom': False, 'top': False, 'left': False, 'right': False, 'bold':False })
        titulo9 = workbook.add_format({'font_size': 10, 'align': 'right', 'text_wrap': True, 'bottom': False, 'top': False, 'left': False, 'right': False, 'bold':False })
        titulo6 = workbook.add_format({'font_size': 10, 'align': 'center', 'text_wrap': True, 'bottom': False, 'top': False, 'left': False, 'right': False, 'bold':False, 'color': 'red'})
        titulo12 = workbook.add_format({'font_size': 10, 'align': 'right', 'text_wrap': True, 'bottom': False, 'top': False, 'left': False, 'right': False, 'bold':False, 'color': 'red'})
        titulo7 = workbook.add_format({'font_size': 10, 'align': 'left', 'text_wrap': True, 'bottom': False, 'top': False, 'left': False, 'right': False, 'bold':False})
        titulo8 = workbook.add_format({'font_size': 10, 'align': 'right', 'text_wrap': True, 'bottom': False, 'top': False, 'left': False, 'right': False, 'bold':False})

        number_left = workbook.add_format({'font_size': 9, 'align': 'left', 'num_format': '#,##0.00'})
        number_right = workbook.add_format({'font_size': 9, 'align': 'right', 'num_format': '#,##0.00'})
        number_right_bold = workbook.add_format({'font_size': 9, 'align': 'right', 'num_format': '#,##0.00', 'bold':True})
        number_right_col = workbook.add_format({'font_size': 9, 'align': 'right', 'num_format': '#,##0.00','bg_color': 'silver'})
        number_center = workbook.add_format({'font_size': 9, 'align': 'center', 'num_format': '#,##0.00'})
        number_right_col.set_locked(False)

        letter1 = workbook.add_format({'font_size': 9, 'align': 'left', 'text_wrap': True})
        letter2 = workbook.add_format({'font_size': 9, 'align': 'left', 'bold':True})
        letter3 = workbook.add_format({'font_size': 9, 'align': 'right', 'text_wrap': True,'font_size': 11,'font_name': 'Lucida Sans',})
        letter4 = workbook.add_format({'font_size': 9, 'align': 'left', 'text_wrap': True, 'bold': True})
        letter4C = workbook.add_format({'font_size': 9, 'align': 'left', 'text_wrap': True, 'bold': True,'color': '#507AAA','font_name': 'Lucida Sans', })
        letter4F = workbook.add_format({'font_size': 9, 'align': 'left', 'text_wrap': True, 'bold': True,'color': '#FFFFFF','bg_color': '#507AAA','font_name': 'Lucida Sans',})
        letter4G = workbook.add_format({'font_size': 9, 'align': 'left', 'text_wrap': True, 'bold': True,'color': '#000000','bg_color': '#f0f0f0','font_name': 'Lucida Sans',})
        letter4S = workbook.add_format({'font_size': 9, 'align': 'left', 'text_wrap': True, 'bold': True})
        letter41S = workbook.add_format({'font_size': 9, 'align': 'left', 'text_wrap': True})
        letter41Sr = workbook.add_format({'font_size': 9, 'align': 'left', 'text_wrap': True,'color': 'red'})
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
        sheet.merge_range('A1:G1', 'Ventas por Clientes y Porducto', titulo1)
        sheet.merge_range('A2:G2', fecha_inicial +' - '+ fecha_final, titulo4)
        fecha = (datetime.now() - timedelta(hours=4)).strftime('%d/%m/%Y %H:%M:%S')
        sheet.merge_range('A3:D3', self.env.user.company_id.name, letter4)


        sheet.write(3, 1, 'Usuario:', letter4C)
        sheet.write(3, 2, self.env.user.partner_id.name, letter4C)
        sheet.write(3, 3, 'Sucuarsal:', letter4C)
        sheet.write(3, 4, 'Todos', letter4C)
        sheet.write(4, 1, 'Cliente:', letter4C)
        sheet.write(4, 2, 'Todos', letter4C)
        sheet.write(4, 3, 'Ciudad:', letter4C)
        sheet.write(4, 4, 'Todos', letter4C)
        sheet.freeze_panes(6, 0)
        filas=7
        sheet.write(filas, 0, 'Cóodigo', letter4G)
        sheet.write(filas, 1, 'Nombre de Producto', letter4G)
        sheet.write(filas, 2, 'UdM', letter4G)
        sheet.write(filas, 3, 'Cantidad', letter4G)
        sheet.write(filas, 4, 'Base Imponible', letter4G)
        sheet.write(filas, 5, 'Impuestos', letter4G)
        sheet.write(filas, 6, 'Total', letter4G)
        filas+=1
        # Preparando variables para cada casod e consulta
        dict_city_ids=[]
        filtro_fechas_po = " AND (so.date_order AT TIME ZONE 'UTC' AT TIME ZONE 'BOT')::date BETWEEN '" + str(data['form']['start_date']) + "' AND '" + str(data['form']['end_date']) + "'"
        dict_vendedores = []
        if data['form']['user_ids']:
            for ids in data['form']['user_ids']:
                dict_vendedores.append(ids)
        if dict_vendedores:
            filtro_vendedores_po = "AND user_id.id in "+str(dict_vendedores).replace('[','(').replace(']',')')
        else:
            filtro_vendedores_po = ''

        if data['form']['city_ids']:
            for ids in data['form']['city_ids']:
                dict_city_ids.append(ids)
        if dict_city_ids:
            filtro_vendedores_po += " AND rp.state_id in "+str(dict_city_ids).replace('[','(').replace(']',')')
        else:
            filtro_vendedores_po += ''
        dict_clientes = []
        if data['form']['partner_ids']:
            for ids in data['form']['partner_ids']:
                dict_clientes.append(ids)
        if dict_clientes:
            filtro_clientes = "AND rp.id in "+str(dict_clientes).replace('[','(').replace(']',')')
        else:
            filtro_clientes = ''
        
        dict_almacen = []
        if data['form']['location_ids']:
            for ids in data['form']['location_ids']:
                dict_almacen.append(ids)
        if dict_almacen:
            filtro_almacen = "AND sl.id in "+str(dict_almacen).replace('[','(').replace(']',')')
        else:
            almacenes = self.env['stock.location'].sudo().search([('usage', '=', 'internal')])
            for almecen in almacenes:
                dict_almacen.append(almecen.id)
            filtro_almacen = "AND sl.id in "+str(dict_almacen).replace('[','(').replace(']',')')
        gran_total = 0.0
        #consultas
        consulta_productos = ("""
            SELECT 
            sol.id
            ,pp.default_code
            ,pt.name
            ,um.name
            ,sol.product_uom_qty
            ,sol.qty_delivered
            ,sol.qty_invoiced
            ,sol.price_total
            ,sol.price_tax
            ,sol.price_subtotal
            FROM product_product pp
            join sale_order_line sol on sol.product_id = pp.id
            join uom_uom um on um.id= sol.product_uom
            join sale_order so on so.id =sol.order_id
            join res_partner rp on rp.id= so.partner_id
            join product_template pt on pt.id=pp.product_tmpl_id
                """ + str(filtro_clientes) + """
                 AND so.date_order::date <= '"""+str(data['form']['end_date'])+"""'
                """ + str(filtro_vendedores_po) + """
           
            and so.state in ('sale','done','sent')
            """)
        self.env.cr.execute(consulta_productos)
        productos = [k for k in self.env.cr.fetchall()]
        for producto in productos:
            sheet.write(filas, 0, producto[1], letter41S)
            sheet.write(filas, 1, producto[2], letter41S)
            sheet.write(filas, 2, producto[3], letter41S)
            sheet.write(filas, 3, producto[4], letter41S)
            sheet.write(filas, 4, producto[7], number_right)
            sheet.write(filas, 5, producto[8], number_right)
            sheet.write(filas, 6, producto[9], number_right)
            gran_total+= producto[9]
            filas+=1
        sheet.merge_range('E'+str(filas+1)+':F'+str(filas+1)+'',  'Total', letter41S)
        sheet.write(filas, 6, gran_total, letter4S)