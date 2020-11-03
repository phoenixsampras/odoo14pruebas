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
    _name = 'l10n_cl_tichile_reports.reporte.lista.producto.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):     
        sheet = workbook.add_worksheet('reporte por lista de producto')
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
        sheet.set_column('L:L',10, letter1)
        sheet.set_column('M:M',10, letter1)
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
        sheet.merge_range('A1:V1', 'reporte por lista de producto', titulo1)
        sheet.merge_range('A2:V2', fecha_inicial +' - '+ fecha_final, titulo4)
        fecha = (datetime.now() - timedelta(hours=4)).strftime('%d/%m/%Y %H:%M:%S')
        sheet.merge_range('A3:D3', self.env.user.company_id.name, letter4)



        sheet.merge_range('C4:D4', 'Usuario:', letter4C)
        sheet.merge_range('E4:G4', self.env.user.partner_id.name, letter4)        
        sheet.merge_range('K4:L4', 'Sucuarsal:', letter4C)
        sheet.merge_range('M4:N4', 'Todos', letter4)
        sheet.merge_range('C5:D5', 'Cliente:', letter4C)
        sheet.merge_range('E5:G5', 'Todos', letter4)        
        sheet.merge_range('K5:L5', 'Ciudad:', letter4C)
        sheet.merge_range('M5:N5', 'Todos', letter4)
        sheet.freeze_panes(6, 0)
        filas=
        sheet.write(filas, 0, 'Cóodigo', letter4F)
        sheet.write(filas, 1, 'Nombre de Producto', letter4F)
        sheet.write(filas, 2, 'UdM', letter4F)
        sheet.write(filas, 3, 'Cantidad Pedida', letter4F)
        sheet.write(filas, 4, 'Cantidad Entregada', letter4F)
        sheet.write(filas, 5, 'Cantidad Facturado', letter4F)
        sheet.write(filas, 6, 'Base Imponible', letter4F)
        sheet.write(filas, 6, 'Total', letter4F)
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
            almacenes = self.env['stock.location'].sudo().search([('as_type_almacen', '=', False),('usage', '=', 'internal')])
            for almecen in almacenes:
                dict_almacen.append(almecen.id)
            filtro_almacen = "AND sl.id in "+str(dict_almacen).replace('[','(').replace(']',')')
        gran_total = 0.0
        # #consultas
        # consulta_clientes = ("""
        #     SELECT 
        #     rcs.name
        #     ,rp.vat
        #     ,rp.name
        #     ,rp.business_name
        #     ,rp.phone
        #     ,rp.mobile
        #     ,rp.id
        #     from res_partner rp
        #     left join res_country_state rcs on rp.state_id = rcs.id
        #     where customer=True
        #         """ + str(filtro_clientes) + """
        #     """)
        # self.env.cr.execute(consulta_clientes)
        # clientes = [k for k in self.env.cr.fetchall()]
        # for cliente in clientes:
        #     saldott = 0.00
        #     consultas_ventas = ("""
        #         SELECT
        #         ai.id
        #         ,to_char((ai.fecha_boliviana AT TIME ZONE 'UTC' AT TIME ZONE 'BOT')::date,'DD/MM/YYYY') AS fecha
        #         ,to_char((ai.date_due AT TIME ZONE 'UTC' AT TIME ZONE 'BOT')::date,'DD/MM/YYYY') AS fecha_vencimiento
        #         ,so.name as nro_nota
        #         ,so.as_numeracion_interna AS numero_interno	
        #         ,ai.invoice_number AS numero_interno_factura	
        #         ,ai.state
        #         ,ai.amount_total AS importe
        #         ,so.as_pagado AS pagado
        #         ,so.as_saldo as saldo			
        #         ,sl.name as almacen
        #         ,so.id
        #         ,ai.id
        #         FROM sale_order AS so
        #         left join account_invoice ai on ai.origin = so.name
        #         JOIN res_users AS usuarios ON usuarios.id = so.user_id
        #         JOIN res_partner AS asesor ON asesor.id = usuarios.partner_id
        #         LEFT JOIN res_partner AS cliente ON cliente.id = so.partner_id
        #         left join as_metodo_pago_ventas mp on mp.id = so.as_forma_pago_id
        #         join stock_picking sp on sp.origin=so.name
        #         join stock_location sl on sp.location_id=sl.id
        #         WHERE
        #         cliente.id = """+str(cliente[6])+"""
        #         AND so.date_order::date <= '"""+str(data['form']['end_date'])+"""'
        #         """ + str(filtro_vendedores_po) + """
        #         """ + str(filtro_almacen) + """
        #         and ai.state='open'
        #         and so.state NOT IN ('cancel','draft') group by 1,2,3,4,5,6,7,8,9,10,11,12,13
        #         """)
        #     self.env.cr.execute(consultas_ventas)
        #     ventas = [k for k in self.env.cr.fetchall()]
        #     #informacion que se va a escribir en excel
        #     if ventas:
        #         sheet.merge_range('A'+str(filas+1)+':B'+str(filas+1)+'', cliente[0], letter4G)
        #         sheet.merge_range('C'+str(filas+1)+':D'+str(filas+1)+'', cliente[1], letter4G)
        #         sheet.merge_range('E'+str(filas+1)+':J'+str(filas+1)+'', cliente[2], letter4G)
        #         sheet.merge_range('K'+str(filas+1)+':R'+str(filas+1)+'', cliente[3], letter4G)
        #         # sheet.write(filas, 14, cliente[3], letter4G)
        #         sheet.merge_range('P'+str(filas+1)+':R'+str(filas+1)+'',  cliente[4], letter4G)
        #         sheet.merge_range('S'+str(filas+1)+':U'+str(filas+1)+'',  cliente[5], letter4G)
        #         filav=filas
        #         filas+=1
        #         sheet.merge_range('B'+str(filas+1)+':D'+str(filas+1)+'', 'Doc. Origen', letter4S)
        #         sheet.merge_range('E'+str(filas+1)+':F'+str(filas+1)+'', 'Factura', letter4S)
        #         sheet.merge_range('G'+str(filas+1)+':I'+str(filas+1)+'', 'Fecha de Cred.', letter4S)
        #         sheet.merge_range('J'+str(filas+1)+':L'+str(filas+1)+'', 'Vencimiento.', letter4S)
        #         sheet.write(filas, 12, 'Est.', letter4S)
        #         sheet.write(filas, 13, 'Dia Ven', letter4S)
        #         sheet.merge_range('P'+str(filas+1)+':R'+str(filas+1)+'',  'Total', letter4S)
        #         sheet.merge_range('S'+str(filas+1)+':U'+str(filas+1)+'',  'Abonos', letter4S)
        #         sheet.write(filas, 21, 'Saldo', letter4S)
        #         filas+=1
        #         saldo_anterior = 0.0
        #         abono_anterior = 0.0
        #         movimientos_ventas = []
        #         movimientos_vencidos = []
        #         saldo_vencido = 0.0
        #         saldot = 0.0
        #         total_creditos = 0.0
        #         pagadot = 0.0
        #         for lines in ventas:
        #             if lines[6] == 'open':
        #                 movimientos_vencidos.append(lines)
                
        #         if movimientos_vencidos != []:
        #             for move in movimientos_vencidos:
        #                 saldot=0.0
        #                 if move[7] != None:
        #                     saldot += move[7]
        #                     pagadot += move[8]
        #                     saldo_vencido += move[7]
        #                     fecha_order = (datetime.now() - timedelta(hours = 4))
        #                     fecha_vence = datetime.strptime(str(move[2]), '%d/%m/%Y')
        #                     dias = fecha_order - fecha_vence
        #                     format = titulo5
        #                     format_right = titulo9
        #                     if dias.days > 30:
        #                         format = titulo6
        #                         format_right = titulo12
        #                     total_creditos= round(move[7],2)
        #                     sheet.merge_range('B'+str(filas+1)+':D'+str(filas+1)+'', move[3], letter41S)
        #                     sheet.merge_range('E'+str(filas+1)+':F'+str(filas+1)+'', move[5], letter41S)
        #                     sheet.merge_range('G'+str(filas+1)+':I'+str(filas+1)+'', move[1], letter41S)
        #                     sheet.merge_range('J'+str(filas+1)+':L'+str(filas+1)+'', move[2], letter41S)
        #                     state='PEN'
        #                     if move[2] != None and (datetime.now() - timedelta(hours = 4)).strftime('%d/%m/%Y') >= move[2] and move[6] == 'open':
        #                         state='VEN'

        #                     sheet.write(filas, 12, state, letter41S)
        #                     if dias.days < 0:
        #                         sheet.write(filas, 13, dias.days, letter41S)
        #                     else:
        #                         sheet.write(filas, 13, dias.days, letter41Sr)
        #                     sheet.merge_range('P'+str(filas+1)+':R'+str(filas+1)+'',  total_creditos, letter41S)
        #                     #extraemos el total de abonos
        #                     consultas_pagos = ("""
        #                     SELECT
        #                     as_venta,sum(as_pago) from as_account_payments_line
        #                     WHERE
        #                     as_venta = """+str(move[12])+""" and as_estado='Valido' group by 1
        #                     """)
        #                     self.env.cr.execute(consultas_pagos)
        #                     pagos = [k for k in self.env.cr.fetchall()]
        #                     abonos = 0.0
        #                     if pagos:
        #                         abonos = float(pagos[0][1])
        #                     sheet.merge_range('S'+str(filas+1)+':U'+str(filas+1)+'',  abonos, letter41S)
        #                     sheet.write(filas, 21, total_creditos-abonos, letter41S)
        #                     saldott += total_creditos-abonos
        #                     gran_total+=total_creditos-abonos
        #                     filas +=1
        #         sheet.write(filav, 21, saldott, letter4G)
        # sheet.merge_range('S'+str(filas+1)+':U'+str(filas+1)+'',  'Total', letter41S)
        # sheet.write(filas, 21, gran_total, letter4S)






