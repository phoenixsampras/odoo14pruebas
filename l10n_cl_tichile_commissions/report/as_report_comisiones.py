# # -*- coding: utf-8 -*-

import datetime
from datetime import datetime
import pytz
from odoo import models,fields
from datetime import datetime, timedelta
from time import mktime

class CalculoComisiones(models.AbstractModel):
    _name = 'report.l10n_cl_tichile_commissions.comision_report_xls.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):        
        dict_almacen = []
        dict_aux = []
        filtro = ''
        if data['form']['user_id']:
            filtro+= ' and ru.id in '+ str(data['form']['user_id']).replace('[','(').replace(']',')')
        # if data['form']['partner_id']:
        #     filtro+= ' and rp.id in '+ str(data['form']['partner_id']).replace('[','(').replace(']',')')
        # if data['form']['as_empresa']:
        #     filtro+= ' and ae.id in '+ str(data['form']['as_empresa']).replace('[','(').replace(']',')')

        sheet = workbook.add_worksheet('Detalle de Movimientos')
        titulo1 = workbook.add_format({'font_size': 16, 'align': 'center', 'text_wrap': True, 'bold':True })
        titulo2 = workbook.add_format({'font_size': 14, 'align': 'center', 'text_wrap': True, 'bottom': True, 'top': True, 'bold':True })
        titulo3 = workbook.add_format({'font_size': 12, 'align': 'left', 'text_wrap': True, 'bottom': True, 'top': True, 'bold':True })
        titulo3_number = workbook.add_format({'font_size': 14, 'align': 'right', 'text_wrap': True, 'bottom': True, 'top': True, 'bold':True, 'num_format': '#,##0.00' })
        titulo4 = workbook.add_format({'font_size': 12, 'align': 'center', 'text_wrap': True, 'bottom': True, 'top': True, 'left': True, 'right': True, 'bold':True })

        number_left = workbook.add_format({'font_size': 12, 'align': 'left', 'num_format': '#,##0.00'})
        number_right = workbook.add_format({'font_size': 12, 'align': 'right', 'num_format': '#,##0.00'})
        number_right_bold = workbook.add_format({'font_size': 12, 'align': 'right', 'num_format': '#,##0.00', 'bold':True})
        number_right_col = workbook.add_format({'font_size': 12, 'align': 'right', 'num_format': '#,##0.00','bg_color': 'silver'})
        number_right_col1 = workbook.add_format({'font_size': 12, 'align': 'right', 'num_format': '#,##0.00'})
        number_center = workbook.add_format({'font_size': 12, 'align': 'center', 'num_format': '#,##0.00'})
        number_right_col.set_locked(False)

        letter12 = workbook.add_format({'font_size': 12, 'align': 'center', 'text_wrap': True, 'bold':True})
        letter11 = workbook.add_format({'font_size': 12, 'align': 'center', 'text_wrap': True})
        letter1 = workbook.add_format({'font_size': 12, 'align': 'left', 'text_wrap': True})
        letter2 = workbook.add_format({'font_size': 12, 'align': 'left', 'bold':False})
        letter3 = workbook.add_format({'font_size': 12, 'align': 'right', 'text_wrap': True})
        letter4 = workbook.add_format({'font_size': 12, 'align': 'left', 'text_wrap': True, 'bold': True})
        letter5 = workbook.add_format({'font_size': 12, 'align': 'right', 'text_wrap': True, 'bold': True})
        letter4C = workbook.add_format({'font_size': 9, 'align': 'left', 'text_wrap': True, 'bold': True,'color': '#507AAA','font_name': 'Lucida Sans', })
        letter4F = workbook.add_format({'font_size': 9, 'align': 'left', 'text_wrap': True, 'bold': True,'color': '#FFFFFF','bg_color': '#507AAA','font_name': 'Lucida Sans',})
        letter4G = workbook.add_format({'font_size': 9, 'align': 'left', 'text_wrap': True, 'bold': True,'color': '#000000','bg_color': '#f0f0f0','font_name': 'Lucida Sans',})
        letter4S = workbook.add_format({'font_size': 9, 'align': 'left', 'text_wrap': True, 'bold': True})
        letter41S = workbook.add_format({'font_size': 9, 'align': 'left', 'text_wrap': True})
        letter41Sr = workbook.add_format({'font_size': 9, 'align': 'left', 'text_wrap': True,'color': 'red'})
        letter_locked = letter3
        letter_locked.set_locked(False)

        # Aqui definimos en los anchos de columna
        sheet.set_column('A:A',15, letter1)
        sheet.set_column('B:B',15, letter1)
        sheet.set_column('C:C',15, letter1)
        sheet.set_column('D:D',15, letter1)
        sheet.set_column('E:E',15, letter1)
        sheet.set_column('F:F',15, letter1)
        sheet.set_column('G:G',15, letter1)
        sheet.set_column('H:H',20, letter1)
        sheet.set_column('I:I',25, letter1)
        sheet.set_column('J:J',15, letter1)
        sheet.set_column('K:K',15, letter1)
        type_report = self.env['ir.config_parameter'].sudo().get_param('res_config_settings.as_type_comissions')
        modality = self.env['ir.config_parameter'].sudo().get_param('res_config_settings.as_type_modality')
        fecha_inicial = datetime.strptime(data['form']['start_date'], '%Y-%m-%d').strftime('%d/%m/%Y')
        fecha_final = datetime.strptime(data['form']['end_date'], '%Y-%m-%d').strftime('%d/%m/%Y')
        # Titulos, subtitulos, filtros y campos del reporte
        fecha = (datetime.now() - timedelta(hours=4)).strftime('%d/%m/%Y %H:%M:%S')
        sheet.merge_range('A1:G1', 'Liquidacion de Comisiones', titulo1)
        
        sheet.write(3, 1, 'Usuario:', letter4C)
        sheet.write(3, 2, self.env.user.partner_id.name, letter4C)
        sheet.write(3, 3, 'Sucuarsal:', letter4C)
        sheet.write(3, 4, 'Todos', letter4C)
        sheet.write(4, 1, 'Cliente:', letter4C)
        sheet.write(4, 2, 'Todos', letter4C)
        sheet.write(4, 3, 'Ciudad:', letter4C)
        sheet.write(4, 4, 'Todos', letter4C)
        sheet.set_row(6, 40)
        sheet.merge_range('A2:G2', 'DEL '+fecha_inicial+' AL '+fecha_final, letter11)
        filas = 6
        if type_report == 'Porcentaje (%)':

            sheet.write(filas, 0, 'Fecha Pedido',letter4G) #cliente/proveedor
            sheet.write(filas, 1, 'Pedido de Venta',letter4G) #cliente/proveedor
            sheet.write(filas, 2, 'Nro interno',letter4G) #cliente/proveedor
            sheet.write(filas, 3, 'Cliente',letter4G) #cliente/proveedor
            sheet.write(filas, 4, 'Total Ventas',letter4G) #cliente/proveedor
            sheet.write(filas, 5, '(%) Comisión',letter4G) #cliente/proveedor
            sheet.write(filas, 6, 'Liquidación',letter4G) #cliente/proveedor
            sheet.write(filas, 7, 'Tipo Liquidación',letter4G) #cliente/proveedor
            sheet.write(filas, 8, 'Usuario',letter4G) #cliente/proveedor
            total_margen = 0.0 
            total_pagar = 0.0 
            sheet.set_row(filas,30,letter4G)
            filas += 1
            cantidad = 0
            query_movements = ("""
                select 
                pt.name
                ,thp.as_comissions
                ,sum(sol.as_total_puntos)
                ,rp.name
                ,so.state
                ,so.date_order
                ,so.name
                ,so.id
                ,cliente.name
                ,so.amount_total
                ,so.as_comissions
                from product_pricelist_item thp
                inner join product_product pp on pp.product_tmpl_id = thp.product_tmpl_id
                inner join product_template pt on pt.id = thp.product_tmpl_id
                inner join sale_order_line sol on sol.product_id = pp.id
                inner join sale_order so on so.id = sol.order_id
                inner join res_partner cliente on so.partner_id = cliente.id
                inner join res_users ru on ru.id = so.user_id
                inner join res_partner rp on ru.partner_id = rp.id
                where 
                so.state not in ('draft') and
                so.date_order::date BETWEEN '"""+str(data['form']['start_date'])+"""' AND  '"""+str(data['form']['end_date'])+"""' """+filtro+""" 
                group by 1,2,4,5,6,7,8,9,10
                """)
            #_logger.debug(query_movements)
            self.env.cr.execute(query_movements)
            total_margin = 0.0
            total_comision = 0.0
            historico_prom = [k for k in self.env.cr.fetchall()]
            for history in historico_prom:
                comision=0.0
                margin=0.0
                if modality != 'Clientes':
                    if history[1]:
                        comision = history[1] 
                else:
                    if history[10]:
                        comision = history[10]               
                if history[2]:
                    margin = history[2]
                cantidad+=1
                sheet.write(filas, 0, str(history[5])) 
                sheet.write(filas, 1, history[6]) 
                sheet.write(filas, 2, history[7]) 
                sheet.write(filas, 3, history[8]) 
                sheet.write(filas, 4, history[9]) 
                sheet.write(filas, 5, comision,number_right_col1) 
                if history[4] == 'cancel':
                    total_margin-=float(margin)
                    total_comision-= (float(margin)*float(comision))/100
                    # sheet.write(filas, 2, -margin,number_right_col1) 
                    # sheet.write(filas, 3, fecha_inicial) 
                    # sheet.write(filas, 4, fecha_final) 
                    sheet.write(filas, 6, -(float(margin)*float(comision))/100,number_right_col1) 
                    sheet.write(filas, 7, type_report)  
                    sheet.write(filas, 8, history[3])  
                else:
                    total_margin+=float(margin)
                    total_comision+= (float(margin)*float(comision))/100
                    # sheet.write(filas, 2, margin,number_right_col1) 
                    # sheet.write(filas, 3, fecha_inicial) 
                    # sheet.write(filas, 4, fecha_final) 
                    sheet.write(filas, 6, (float(margin)*float(comision))/100,number_right_col1) 
                    sheet.write(filas, 7, type_report)  
                    sheet.write(filas, 8, history[3])  

                filas += 1

            sheet.merge_range('A'+str(filas+1)+':D'+str(filas+1),'TOTAL ', number_right_col)
            sheet.write(filas, 4, total_margin, number_right_col) 
            sheet.write(filas, 5, total_comision, number_right_col) 
        else:
            sheet.write(filas, 0, 'VENDEDOR',titulo4) #cliente/proveedor
            sheet.write(filas, 1, 'FECHA INICIO',titulo4) #cliente/proveedor
            sheet.write(filas, 2, 'FECHA FINAL',titulo4) #cliente/proveedor
            sheet.write(filas, 3, 'TOTAL MARGEN VENTAS',titulo4) #cliente/proveedor
            sheet.write(filas, 4, '% DE COMISION <= LIMITE 1',titulo4) #cliente/proveedor
            sheet.write(filas, 5, 'A PAGAR',titulo4) #cliente/proveedor
            total_margen = 0.0 
            total_pagar = 0.0 
            total_porcentaje = 0.0 
            sheet.set_row(filas,30,titulo4)
            filas += 1
            cantidad = 0
            query_ids = ("""
                select ru.id from res_users ru
                inner join res_partner rp on ru.partner_id = rp.id
                where 
                ru.active=True
                """+filtro+"""
            """)

            self.env.cr.execute(query_ids)
            users = [j for j in self.env.cr.fetchall()]
            for partner in users:
                query_movements = ("""
                    select 
                    rp.name
                    ,sum(sol.as_total_puntos)
                    ,so.state
                    from product_template thp
                    inner join product_product pp on pp.product_tmpl_id = thp.id
                    inner join sale_order_line sol on sol.product_id = pp.id
                    inner join sale_order so on so.id = sol.order_id
                    inner join res_users ru on ru.id = so.user_id
                    inner join res_partner rp on ru.partner_id = rp.id
                    where 
                    so.state not in ('draft')
                    and ru.id="""+str(partner[0])+""" and
                    so.date_order::date BETWEEN '"""+str(data['form']['start_date'])+"""' AND  '"""+str(data['form']['end_date'])+"""' """+filtro+""" 
                    group by 1,3
                    """)
                #_logger.debug(query_movements)
                self.env.cr.execute(query_movements)
                historico_prom = [k for k in self.env.cr.fetchall()]
                for history in historico_prom:
                    cantidad+=1
                    sheet.write(filas, 0, history[0]) 
                    sheet.write(filas, 1, fecha_inicial) 
                    sheet.write(filas, 2, fecha_final) 
                    if history[2] == 'cancel':
                        sheet.write(filas, 3, -history[1],number_right_col1) 
                    else:
                        sheet.write(filas, 3, history[1],number_right_col1) 
                    query_ids = ("""
                    select as_desde,as_hasta,as_comision,as_division from as_tabla_comisiones 
                    where 
                    as_desde <= """+str(history[1])+""" and """+str(history[1])+""" <= as_hasta limit 1
                    """)

                    self.env.cr.execute(query_ids)
                    history_table = [j for j in self.env.cr.fetchall()]
                    porcentaje = 0.0
                    pagar = 0.0
                    if history_table:
                        porcentaje = float(history[1])/float(history_table[0][1])
                        if history_table[0][3]==True:
                            pagar = history_table[0][2] * porcentaje
                        else:
                            pagar = history_table[0][2]
                        if history[2] == 'cancel':
                            total_margen -= float(history[1])
                            total_pagar -= pagar
                            total_porcentaje -= porcentaje
                        else:
                            total_margen += float(history[1])
                            total_pagar += pagar
                            total_porcentaje += porcentaje
                    if history[2] == 'cancel':
                        sheet.write(filas, 4,  str(round(-porcentaje*100,2))+str('%'),number_right_col1)
                        sheet.write(filas, 5,  -pagar,number_right_col1)
                    else:
                        sheet.write(filas, 4,  str(round(porcentaje*100,2))+str('%'),number_right_col1)
                        sheet.write(filas, 5,  pagar,number_right_col1)
                    filas += 1

            sheet.merge_range('A'+str(filas+1)+':C'+str(filas+1),'TOTAL ', number_right_col)
            sheet.write(filas, 4, str(round(total_porcentaje*100,2))+str('%'),number_right_col)
            sheet.write(filas, 3, total_margen, number_right_col) 
            sheet.write(filas, 5, total_pagar, number_right_col) 
