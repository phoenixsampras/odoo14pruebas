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
    _name = 'report.l10n_cl_tichile_reports.resumen_ventas_utilidad.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):     
        sheet = workbook.add_worksheet('Informe de Ventas y Utilidad')
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
        sheet.set_column('A:A',25, letter1)
        sheet.set_column('B:B',15, letter1)
        sheet.set_column('C:C',15, letter1)
        sheet.set_column('D:D',15, letter1)
        sheet.set_column('E:E',15, letter1)
        sheet.set_column('F:F',15, letter1)
        sheet.set_column('G:G',15, letter1)
        sheet.set_column('H:H',15, letter1)
        sheet.set_column('I:I',15, letter1)
        sheet.set_column('J:J',10, letter1)
        sheet.set_column('K:K',10, letter1)
        sheet.set_column('L:L',10, letter1)
        sheet.set_column('M:M',10, letter1)
        sheet.set_column('N:N',12, letter1)
        sheet.set_column('O:O',12, letter1)
        sheet.set_column('P:P',5, letter1)
        # sheet.set_column('Q:Q',5, letter1)
        # sheet.set_column('R:R',5, letter1)
        # sheet.set_column('S:S',5, letter1)
        # sheet.set_column('T:T',5, letter1)
        # sheet.set_column('U:U',5, letter1)
        # sheet.set_column('V:V',10, letter1)

        # Titulos, subtitulos, filtros y campos del reporte
        fecha_inicial = datetime.strptime(str(data['form']['start_date']), '%Y-%m-%d').strftime('%d/%m/%Y')
        fecha_final = datetime.strptime(str(data['form']['end_date']), '%Y-%m-%d').strftime('%d/%m/%Y')
        sheet.merge_range('A1:J1', 'Informe de Ventas y Utilidad', titulo1)
        sheet.merge_range('A2:J2', fecha_inicial +' - '+ fecha_final, titulo4)
        fecha = (datetime.now() - timedelta(hours=4)).strftime('%d/%m/%Y %H:%M:%S')
        sheet.merge_range('A3:D3', self.env.user.company_id.name, letter4)



        sheet.merge_range('C4:D4', 'Sucuarsal:', letter4C)
        sheet.merge_range('H4:I4', 'Todos', letter4)        
        # sheet.merge_range('H4:I4', 'Sucuarsal:', letter4C)
        # sheet.merge_range('I4:J4', 'Todos', letter4)
        # sheet.merge_range('C5:D5', 'Cliente:', letter4C)
        # sheet.merge_range('H5:I5', 'Todos', letter4)        
        # sheet.merge_range('H5:I5', 'Ciudad:', letter4C)
        # sheet.merge_range('I5:J5', 'Todos', letter4)
        sheet.freeze_panes(7, 0)
        filas= 7
        sheet.write(filas, 0, 'Detalle', letter4G)
        sheet.write(filas, 1, 'Unidad de Medida', letter4G)
        sheet.write(filas, 2, 'Cantidad', letter4G)
        sheet.write(filas, 3, 'Precio de Costo', letter4G)
        sheet.write(filas, 4, 'Precio U. Venta', letter4G)
        sheet.write(filas, 5, 'Venta Bruta', letter4G)
        sheet.write(filas, 6, 'IVA DEB.', letter4G)
        sheet.write(filas, 7, 'Venta Neta', letter4G)
        sheet.write(filas, 8, 'Costo Compra', letter4G)
        sheet.write(filas, 9, 'Margen de Ganancia', letter4G)
        sheet.write(filas, 10, '(%)', letter4G)
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
        gran_total = 0.0
        #consultas
        ttotal_venta =0.0
        ttotal_iva =0.0
        ttotal_neto =0.0
        ttotal_costo =0.0
        ttotal_margen =0.0
        ttotal_porcentaje =0.0
        consulta_clientes = ("""
            SELECT 
            pc.id
            ,pc.complete_name
            from product_category pc
            """)
        self.env.cr.execute(consulta_clientes)
        categories = [k for k in self.env.cr.fetchall()]
        for categ_id in categories:
            saldott = 0.00
            total_venta =0.0
            total_iva =0.0
            total_neto =0.0
            total_costo =0.0
            total_margen =0.0
            total_porcentaje =0.0
            consultas_ventas = ("""
                SELECT
                to_char((so.date_order AT TIME ZONE 'UTC' AT TIME ZONE 'BOT')::date,'DD/MM/YYYY') AS fecha
                ,sol.name
                ,um.name
                ,sol.product_uom_qty
                ,pt.list_price
                ,sol.price_subtotal
                ,sol.price_tax
                ,sol.price_total
                ,pp.id
                FROM sale_order AS so
                join sale_order_line sol on sol.order_id = so.id
                join uom_uom um on um.id=sol.product_uom
                join product_product pp on pp.id=sol.product_id
                left join stock_picking sp on sp.origin=so.name
                join product_template pt on pt.id=pp.product_tmpl_id
                left join account_move ai on ai.invoice_origin = so.name and ai.state='open'
                left join account_payment_term apt on apt.id=so.payment_term_id
                JOIN res_users AS usuarios ON usuarios.id = so.user_id
                JOIN res_partner AS asesor ON asesor.id = usuarios.partner_id
                LEFT JOIN res_partner AS cliente ON cliente.id = so.partner_id
                left join stock_location sl on sp.location_id=sl.id  """ + str(filtro_almacen) + """
                WHERE
                pt.categ_id = """+str(categ_id[0])+"""
                AND so.date_order::date <= '"""+str(data['form']['end_date'])+"""'
                """ + str(filtro_vendedores_po) + """
                
                and so.state NOT IN ('cancel','draft') 
                """)
            self.env.cr.execute(consultas_ventas)
            ventas = [k for k in self.env.cr.fetchall()]
            #informacion que se va a escribir en excel
            if ventas:
                sheet.merge_range('A'+str(filas+1)+':E'+str(filas+1)+'', categ_id[1], letter4S)
                filasv= filas
                filas+=1
                for lines in ventas:
                    product = self.env['product.product'].search([('id','=',lines[8])])
                    total_venta +=lines[5]
                    total_iva += lines[6]
                    total_neto +=lines[7]
                    total_costo +=product.standard_price*lines[3]
                    total_margen +=lines[7]-total_costo
                    if lines[7] > 0:
                        total_porcentaje += (lines[7]-total_costo/lines[7])*100
                    else:
                        total_porcentaje += 0.0
                    sheet.write(filas, 0, lines[1], letter41S)
                    sheet.write(filas, 1, lines[2], letter41S)
                    sheet.write(filas, 2, lines[3], letter41S)
                    sheet.write(filas, 3, product.standard_price, number_right)
                    sheet.write(filas, 4, product.list_price, number_right)
                    sheet.write(filas, 5, lines[5], number_right)
                    sheet.write(filas, 6, lines[6], number_right)
                    sheet.write(filas, 7, lines[7], number_right)
                    sheet.write(filas, 8, total_costo, number_right)
                    sheet.write(filas, 9, lines[7]-total_costo, number_right)
                    sheet.write(filas, 10, total_porcentaje, number_right)
                    filav=filas
                    filas+=1
                sheet.write(filasv, 5, total_venta, letter4S_right)
                sheet.write(filasv, 6, total_iva, letter4S_right)
                sheet.write(filasv, 7, total_neto, letter4S_right)
                sheet.write(filasv, 8, total_costo, letter4S_right)
                sheet.write(filasv, 8, total_costo, letter4S_right)
                sheet.write(filasv, 9, total_margen, letter4S_right)
                sheet.write(filasv, 10, total_porcentaje, letter4S_right)
                filas+=1
                ttotal_venta += total_venta
                ttotal_iva = total_iva
                ttotal_neto = total_neto
                ttotal_costo = total_costo
                ttotal_margen = total_margen
                ttotal_porcentaje = total_porcentaje
        sheet.merge_range('A'+str(filas+1)+':E'+str(filas+1)+'',  'Total', letter4S)
        sheet.write(filas, 5, ttotal_venta, letter4S_right)
        sheet.write(filas, 6, ttotal_iva, letter4S_right)
        sheet.write(filas, 7, ttotal_neto, letter4S_right)
        sheet.write(filas, 8, ttotal_costo, letter4S_right)
        sheet.write(filas, 9, ttotal_porcentaje, letter4S_right)
            
        #         saldo_anterior = 0.0
        #         abono_anterior = 0.0
        #         movimientos_ventas = []
        #         movimientos_vencidos = []
        #         saldo_vencido = 0.0
        #         saldot = 0.0
        #         total_creditos = 0.0
        #         pagadot = 0.0
        #         for lines in ventas:
        #             movimientos_vencidos.append(lines)
                
        #         if movimientos_vencidos != []:
        #             for move in movimientos_vencidos:
        #                 abonos = 0.0
        #                 saldot=0.0
        #                 # if move[7] != None:
        #                 saldot += move[7]
        #                 pagadot += move[8]
        #                 saldo_vencido += move[7]
        #                 fecha_order = (datetime.now() - timedelta(hours = 4))
        #                 fecha_vence = datetime.strptime(str(move[2]), '%d/%m/%Y')
        #                 dias = fecha_order - fecha_vence
        #                 format = titulo5
        #                 format_right = titulo9
        #                 if dias.days > 30:
        #                     format = titulo6
        #                     format_right = titulo12
        #                 total_creditos= round(move[7],2)
        #                 sheet.write(filas, 0, move[1], letter41S)
        #                 sheet.write(filas, 1, move[3], letter41S)
        #                 sheet.write(filas, 2, move[11], letter41S)
        #                 sheet.write(filas, 3, move[13], letter41S)
        #                 sheet.write(filas, 4, move[14], letter41S)
        #                 sheet.write(filas, 5, move[15], letter41S)
        #                 sheet.write(filas, 6, move[14], letter41S)
        #                 sheet.write(filas, 7, move[7], number_right)
        #                 sale = self.env['sale.order'].sudo().search([('id', '=',move[11])])
        #                 for inv in sale.invoice_ids:
        #                     pagos = inv._get_reconciled_info_JSON_values()
        #                     for pay in pagos:
        #                         abonos = pay['amount']
        #                 sheet.write(filas, 8, abonos, number_right)
        #                 sheet.write(filas, 9, move[7]-abonos, number_right)
        #                 gran_total+=move[7]-abonos

        #                 # sheet.merge_range('B'+str(filas+1)+':D'+str(filas+1)+'', move[3], letter41S)
        #                 # sheet.merge_range('E'+str(filas+1)+':F'+str(filas+1)+'', move[5], letter41S)
        #                 # sheet.merge_range('G'+str(filas+1)+':I'+str(filas+1)+'', move[1], letter41S)
        #                 # sheet.merge_range('J'+str(filas+1)+':L'+str(filas+1)+'', move[2], letter41S)
        #                 # state='PEN'
        #                 # if move[2] != None and (datetime.now() - timedelta(hours = 4)).strftime('%d/%m/%Y') >= move[2] and move[6] == 'open':
        #                 #     state='VEN'

        #                 # sheet.write(filas, 12, state, letter41S)
        #                 # if dias.days < 0:
        #                 #     sheet.write(filas, 13, dias.days, letter41S)
        #                 # else:
        #                 #     sheet.write(filas, 13, dias.days, letter41Sr)
        #                 # sheet.merge_range('P'+str(filas+1)+':R'+str(filas+1)+'',  total_creditos, letter41S)
        #                 # #extraemos el total de abonos
        #                 # consultas_pagos = ("""
        #                 # SELECT
        #                 # as_venta,sum(as_pago) from as_account_payments_line
        #                 # WHERE
        #                 # as_venta = """+str(move[12])+""" and as_estado='Valido' group by 1
        #                 # """)
        #                 # self.env.cr.execute(consultas_pagos)
        #                 # pagos = [k for k in self.env.cr.fetchall()]
        #                 # abonos = 0.0
        #                 # if pagos:
        #                 #     abonos = float(pagos[0][1])
        #                 # sheet.merge_range('S'+str(filas+1)+':U'+str(filas+1)+'',  abonos, letter41S)
        #                 # sheet.write(filas, 21, total_creditos-abonos, letter41S)
        #                 # saldott += total_creditos-abonos
        #                 # gran_total+=total_creditos-abonos
        #                 filas +=1
        #         # sheet.write(filav, 21, saldott, letter4G)






