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
    _name = 'report.l10n_cl_tichile_reports.ingreso_inventario.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):     
        sheet = workbook.add_worksheet('reporte por lista de producto')
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
        letter4F = workbook.add_format({'font_size': 9, 'align': 'left', 'bold': True,'color': '#000000','bg_color': '#ffffff','font_name': 'Lucida Sans',})
        letter4G = workbook.add_format({'font_size': 9, 'align': 'left', 'bold': True,'color': '#000000','bg_color': '#f0f0f0','font_name': 'Lucida Sans',})
        letter4G2 = workbook.add_format({'font_size': 9, 'align': 'left', 'bold': True,'color': '#000000','bg_color': '#FFFAF0','font_name': 'Lucida Sans',})
        letter4S = workbook.add_format({'font_size': 9, 'align': 'left', 'bold': True,'bg_color': '#ffffff'})
        letter4S_right = workbook.add_format({'font_size': 9, 'align': 'right', 'bold': True,'bg_color': '#ffffff','num_format': '#,##0.00',})
        letter41S = workbook.add_format({'font_size': 9, 'align': 'left','bg_color': '#ffffff'})
        letter41Si = workbook.add_format({'font_size': 9, 'align': 'right','bg_color': '#ffffff'})
        letter41Sr = workbook.add_format({'font_size': 9, 'align': 'left','color': 'red','bg_color': '#ffffff'})
        letter_locked = letter3
        letter_locked.set_locked(False)

        # Aqui definimos en los anchos de columna
        sheet.set_column('A:A',10, letter1)
        sheet.set_column('B:B',10, letter1)
        sheet.set_column('C:C',10, letter1)
        sheet.set_column('D:D',10, letter1)
        sheet.set_column('E:E',10, letter1)
        sheet.set_column('F:F',10, letter1)
        sheet.set_column('G:G',10, letter1)
        sheet.set_column('H:H',10, letter1)
        sheet.set_column('I:I',10, letter1)
        sheet.set_column('J:J',10, letter1)
        sheet.set_column('K:K',10, letter1)
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
        sheet.merge_range('A1:M1', 'Ingresos de Inventario', titulo1)
        sheet.merge_range('A2:M2', fecha_inicial +' - '+ fecha_final, titulo4)
        fecha = (datetime.now() - timedelta(hours=4)).strftime('%d/%m/%Y %H:%M:%S')
        sheet.merge_range('A3:D3', self.env.user.company_id.name, letter4)



        # sheet.merge_range('C4:D4', 'Usuario:', letter4C)
        # sheet.merge_range('E4:G4', self.env.user.partner_id.name, letter4)        
        sheet.merge_range('B4:C4', 'Sucuarsal:', letter4C)
        sheet.merge_range('D4:F4', 'Todos', letter4)
        # sheet.merge_range('C5:D5', 'Cliente:', letter4C)
        # sheet.merge_range('E5:G5', 'Todos', letter4)        
        # sheet.merge_range('B5:C5', 'Producto:', letter4C)
        # sheet.merge_range('D5:F5', 'Todos', letter4)
        sheet.freeze_panes(6, 0)
        filas=5
        sheet.write(filas, 0, 'Fecha', letter4G)
        sheet.write(filas, 1, 'Nota Compra', letter4G)
        sheet.write(filas, 2, 'Nota Compra', letter4G)
        sheet.write(filas, 3, 'Cliente', letter4G)
        sheet.write(filas, 4, 'Cóodigo', letter4G)
        sheet.write(filas, 5, 'Nombre de Producto', letter4G)
        sheet.write(filas, 6, 'Cantidad', letter4G)
        sheet.write(filas, 7, 'Costo', letter4G)
        sheet.write(filas, 8, 'Total', letter4G)
        sheet.write(filas, 9, 'Categoria Producto', letter4G)
        sheet.write(filas, 10, 'Estado', letter4G)
        sheet.write(filas, 11, 'Ubicación Origen', letter4G)
        sheet.write(filas, 12, 'Ubicación Destino', letter4G)
        filas+=1
        # Preparando variables para cada casod e consulta
        dict_city_ids=[]
        filtro_fechas_po = " AND (po.date_order AT TIME ZONE 'UTC' AT TIME ZONE 'BOT')::date BETWEEN '" + str(data['form']['start_date']) + "' AND '" + str(data['form']['end_date']) + "'"
        dict_vendedores = []
        if data['form']['user_ids']:
            for ids in data['form']['user_ids']:
                dict_vendedores.append(ids)
        if dict_vendedores:
            filtro_vendedores_po = "AND usuarios.id in "+str(dict_vendedores).replace('[','(').replace(']',')')
        else:
            filtro_vendedores_po = ''

        if data['form']['city_ids']:
            for ids in data['form']['city_ids']:
                dict_city_ids.append(ids)
        if dict_city_ids:
            filtro_vendedores_po += " AND cliente.state_id in "+str(dict_city_ids).replace('[','(').replace(']',')')
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
        dict_product = []
        filtro_product = ''
        if data['form']['product_id']:
            for ids in data['form']['product_id']:
                dict_product.append(ids)
        if dict_product:
            filtro_product = "AND pp.id in "+str(dict_product).replace('[','(').replace(']',')')
      
        gran_total = 0.0
        gran_total2 = 0.0
        consulta_productos = ("""
            SELECT 
            sm.id
            ,to_char((sm.date AT TIME ZONE 'UTC' AT TIME ZONE 'BOT')::date,'DD/MM/YYYY') AS fecha
            ,sp.name
            ,sp.origin
            ,rp.name
            ,pp.default_code
            ,pt.name
            ,sm.product_qty
            ,sm.price_unit
            ,pc.name
            ,sp.state
            ,sl1.name
            ,sl2.name
            FROM stock_move sm
            join stock_picking sp on sp.id = sm.picking_id
            join product_product pp on pp.id= sm.product_id
            join purchase_order po on po.name =sp.origin and po.state not in ('draft','cancel')
            join res_partner rp on rp.id= sp.partner_id
            join product_template pt on pt.id=pp.product_tmpl_id
            left join product_category pc on pc.id = pt.categ_id
            left join stock_location sl1 on sm.location_id=sl1.id
            left join stock_location sl2 on sm.location_dest_id=sl2.id
                """ + str(filtro_clientes) + """
                 AND po.date_order::date <= '"""+str(data['form']['end_date'])+"""'
                """ + str(filtro_product) + """
           
            
            """)
        self.env.cr.execute(consulta_productos)
        productos = [k for k in self.env.cr.fetchall()]
        for producto in productos:
            precio = 0.0
            sheet.write(filas, 0, producto[1], letter41S)
            sheet.write(filas, 1, producto[2], letter41S)
            sheet.write(filas, 2, producto[3], letter41S)
            sheet.write(filas, 3, producto[4], number_right)
            sheet.write(filas, 4, producto[5], number_right)
            sheet.write(filas, 5, producto[6], number_right)
            sheet.write(filas, 6, producto[7], number_right)
            sheet.write(filas, 7, producto[8] or 0.0, number_right)
            if producto[8]:
                precio = producto[8]
            else:
                precio = 0.0
            sheet.write(filas, 8, precio* producto[7], number_right)
            sheet.write(filas, 9, producto[9], number_right)
            sheet.write(filas, 10, producto[10], number_right)
            sheet.write(filas, 11, producto[11], number_right)
            sheet.write(filas, 12, producto[12], number_right)
            gran_total+= precio* producto[7]
            gran_total2+= 0.0
            filas+=1
        sheet.merge_range('A'+str(filas+1)+':C'+str(filas+1)+'',  'Total', letter4)
        # sheet.write(filas, 3, gran_total, letter4S_right)
        sheet.write(filas, 8, gran_total, letter4S_right)





