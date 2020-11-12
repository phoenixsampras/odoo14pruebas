# # -*- coding: utf-8 -*-

import datetime
from datetime import datetime
import pytz
from odoo import models,fields
from datetime import datetime, timedelta
from time import mktime

class as_invoices_emit_excel(models.AbstractModel):
    _name = 'report.l10n_cl_tichile_reports.invoices_emit_report_xls.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):     

        consulta = ("""
            SELECT
            to_char(((ai.fecha_boliviana AT TIME ZONE 'UTC' AT TIME ZONE 'BOT')::timestamp),'DD/MM/YYYY') AS fecha_nota,
                    """)
        moduleObj = self.env['ir.module.module'].sudo().search([("name","=","as_sales"),("state","=","installed")])
        if data['form']['as_tipo']=='ventas':
            if moduleObj:
                consulta += "so.as_numeracion_interna AS numero_nota,"
            else:
                consulta += "so.name AS numero_nota,"
        else:
            consulta += "ai.name AS numero_nota,"
        if data['form']['as_tipo']=='ventas':
            consulta += ("""
                ai.id,
                ai.as_nit AS nit_cliente,
                ai.as_razon_social AS nombre_cliente,
                ewqc.numero_autorizacion AS numero_autorizacion,
                ai.control_code AS codigo_control,
            CASE
                WHEN rc.NAME = 'BOB' 
                OR rc.symbol = 'Bs.' THEN
                ROUND( ai.amount_total, 4 ) ELSE ai.amount_total
                END AS importe_neto_venta,
                ROUND( ai.amount_total, 4 ) AS importe_neto_factura,
                ai.invoice_number AS numero_factura,
                to_char((( ai.fecha_boliviana AT TIME ZONE'UTC' AT TIME ZONE'BOT' ) :: TIMESTAMP ), 'DD/MM/YYYY' ) AS fecha_factura,
                asesor.NAME AS nombre_asesor,
                ROUND( ai.amount_total, 4 ) AS impote_bruto_fact,
                ROUND( ai.amount_total, 4 ) AS total_descuento_fact,
                ai.fecha_boliviana AS fecha_factura2,
                fp.name AS tipo_venta 
            FROM
                account_invoice ai
                JOIN sale_order so ON so.NAME = ai.origin
                JOIN res_partner AS cliente ON cliente.ID = so.partner_id
                JOIN res_users AS usuario ON usuario.ID = so.user_id
                JOIN res_partner AS asesor ON asesor.ID = usuario.partner_id
                JOIN qr_code AS ewqc ON ewqc.ID = ai.qr_code_id
                JOIN product_pricelist pp ON pp.ID = so.pricelist_id
                JOIN res_currency rc ON rc.ID = pp.currency_id 
                JOIN as_metodo_pago_ventas fp ON fp.id = so.as_forma_pago_id 
            WHERE
                ai.TYPE = 'out_invoice' 
                AND ai.STATE NOT IN ( 'draft', 'cancel' )
                AND ai.order_status = 'valida'
                AND ai.invoice_number != 0 
                AND ai.type = 'out_invoice' 
            """)
        elif data['form']['as_tipo']=='pos':
            consulta += ("""
                ai.id,
                ai.as_nit AS nit_cliente,
                ai.as_razon_social AS nombre_cliente,
                ewqc.numero_autorizacion AS numero_autorizacion,
                ai.control_code AS codigo_control,
            CASE
                WHEN rc.NAME = 'BOB' 
                OR rc.symbol = 'Bs.' THEN
                ROUND( ai.amount_total, 4 ) ELSE ai.amount_total
                END AS importe_neto_venta,
                ROUND( ai.amount_total, 4 ) AS importe_neto_factura,
                ai.invoice_number AS numero_factura,
                to_char((( ai.fecha_boliviana AT TIME ZONE'UTC' AT TIME ZONE'BOT' ) :: TIMESTAMP ), 'DD/MM/YYYY' ) AS fecha_factura,
                asesor.NAME AS nombre_asesor,
                ROUND( ai.amount_total, 4 ) AS impote_bruto_fact,
                ROUND( ai.amount_total, 4 ) AS total_descuento_fact,
                ai.fecha_boliviana AS fecha_factura2,
                'N/A'
            FROM
                account_invoice ai
                JOIN pos_order so ON so.NAME = ai.origin
                JOIN res_partner AS cliente ON cliente.ID = so.partner_id
                JOIN res_users AS usuario ON usuario.ID = so.user_id
                JOIN res_partner AS asesor ON asesor.ID = usuario.partner_id
                JOIN qr_code AS ewqc ON ewqc.ID = ai.qr_code_id
                JOIN product_pricelist pp ON pp.ID = so.pricelist_id
                JOIN res_currency rc ON rc.ID = pp.currency_id 
            WHERE
                ai.TYPE = 'out_invoice' 
                AND ai.STATE NOT IN ( 'draft', 'cancel' )
                AND ai.order_status = 'valida'
                AND ai.invoice_number != 0 
                AND ai.type = 'out_invoice' 
            """)
        else:
            consulta += ("""
                ai.id,
                ai.as_nit AS nit_cliente,
                ai.as_razon_social AS nombre_cliente,
                ewqc.numero_autorizacion AS numero_autorizacion,
                ai.control_code AS codigo_control,
            CASE
                WHEN rc.NAME = 'BOB' 
                OR rc.symbol = 'Bs.' THEN
                ROUND( ai.amount_total, 4 ) ELSE ai.amount_total
                END AS importe_neto_venta,
                ROUND( ai.amount_total, 4 ) AS importe_neto_factura,
                ai.invoice_number AS numero_factura,
                to_char((( ai.fecha_boliviana AT TIME ZONE'UTC' AT TIME ZONE'BOT' ) :: TIMESTAMP ), 'DD/MM/YYYY' ) AS fecha_factura,
                asesor.NAME AS nombre_asesor,
                ROUND( ai.amount_total, 4 ) AS impote_bruto_fact,
                ROUND( ai.amount_total, 4 ) AS total_descuento_fact,
                ai.fecha_boliviana AS fecha_factura2,
                'N/A'
            FROM
                account_invoice ai
                JOIN res_partner AS cliente ON cliente.ID = ai.partner_id
                JOIN res_users AS usuario ON usuario.ID = ai.user_id
                JOIN res_partner AS asesor ON asesor.ID = usuario.partner_id
                JOIN qr_code AS ewqc ON ewqc.ID = ai.qr_code_id
                JOIN res_currency rc ON rc.ID = ai.currency_id 
            WHERE
                ai.TYPE = 'out_invoice' 
                AND ai.STATE NOT IN ( 'draft', 'cancel' )
                AND ai.order_status = 'valida'
                AND ai.invoice_number != 0 
                AND ai.type = 'out_invoice' 
            """)

        if data['form']['asesor']:
            consulta += " AND usuario.id = " + str(data['form']['asesor'])
        if data['form']['nombre_cliente']:
            consulta += " AND cliente.id = " + str(data['form']['nombre_cliente'])
        if data['form']['fecha_final']:
            consulta +=  " AND ai.fecha_boliviana BETWEEN '" + str(data['form']['fecha_inicial']) + "' AND '" + str(data['form']['fecha_final'])+ "'"
        

        #Definiciones generales del archivo, formatos, titulos, hojas de trabajo
        sheet = workbook.add_worksheet('Detalle de Movimientos')
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
        sheet.set_column('A:A',15, letter1)
        sheet.set_column('B:B',15, letter1)
        sheet.set_column('C:C',15, letter1)
        sheet.set_column('D:D',18, letter1)
        sheet.set_column('E:E',15, letter1)
        sheet.set_column('F:F',15, letter1)
        sheet.set_column('G:G',15, letter3)
        sheet.set_column('H:H',15, letter3)
        sheet.set_column('I:I',15, letter3)
        sheet.set_column('J:J',15, number_center)
        sheet.set_column('K:K',18, letter1)
        sheet.set_column('L:L',18, letter1)
        sheet.set_column('M:M',18, letter1)

        # Titulos, subtitulos, filtros y campos del reporte
        sheet.merge_range('A1:M1', 'FACTURAS EMITIDAS', titulo1)
        sheet.set_row(0, 40)
        fecha = (datetime.now() - timedelta(hours=4)).strftime('%d/%m/%Y %H:%M:%S')
        fecha_inicial = datetime.strptime(data['form']['fecha_inicial'], '%Y-%m-%d').strftime('%d/%m/%Y')
        fecha_final = datetime.strptime(data['form']['fecha_final'], '%Y-%m-%d').strftime('%d/%m/%Y')
        sheet.write(1, 0, 'Rango de Fechas: ', letter4)
        sheet.merge_range('B2:D2', fecha_inicial +' - '+ fecha_final)
        sheet.merge_range('H3:I3', 'Fecha impresion: ', letter5)
        sheet.merge_range('J3:M3', fecha)
        sheet.merge_range('H4:I4', 'Usuario: ', letter5)
        sheet.merge_range('J4:M4', self.env.user.name)

        sheet.write(4, 0,'FECHA', letter4)
        sheet.write(4, 1,'NUMERACION INTERNA', letter4)
        sheet.write(4, 2,'NIT CLIENTE', letter4)
        sheet.write(4, 3,'RAZON SOCIAL', letter4)
        sheet.write(4, 4,'No AUTORIZACION', letter4)
        sheet.write(4, 5, 'CODIGO DE CONTROL', letter4)
        sheet.write(4, 6, 'IMPORTE BRUTO DE FACTURA AL CREDITO BS.', letter4)
        sheet.write(4, 7, 'DESCUENTO CREDITO BS.', letter4)
        sheet.write(4, 8, 'IMPORTE NETO DE FACTURA CREDITO BS.', letter4)
        sheet.write(4, 9, 'No FACTURA', letter4)
        sheet.write(4, 10, 'FECHA FACTURA', letter4)
        sheet.write(4, 11, 'COMERCIAL', letter4)
        sheet.write(4, 12, 'FORMA DE PAGO', letter4)
        sheet.freeze_panes(5, 0)
        sheet.set_row(4, 40)
        self.env.cr.execute(consulta)
        invoices = [j for j in self.env.cr.fetchall()]
        filas=5
        cols=0
        total_bruto=0
        total_descuento=0
        total_neto=0
        cols=0
        for invoice in invoices:
            sheet.write(filas, 0, invoice[0]) #fecha
            sheet.write(filas, 1, invoice[1]) #numeracion interna
            sheet.write(filas, 2, invoice[3]) #nit cliente
            sheet.write(filas, 3, invoice[4]) #razon social
            sheet.write(filas, 4, invoice[5]) #numero autorizacion
            sheet.write(filas, 5, invoice[6]) #codigo control
            sheet.write(filas, 6, round(self.amount_bruto(invoice[2],),6)) #importe bruto
            total_bruto+= self.amount_bruto(invoice[2])
            sheet.write(filas, 7, round(self.amount_discount(invoice[2],),6)) #descuento
            total_descuento += self.amount_discount(invoice[2])
            sheet.write(filas, 8, invoice[8],) #importe neto
            total_neto +=invoice[8]
            sheet.write(filas, 9, invoice[9]) #numero de factura
            sheet.write(filas, 10, invoice[10]) #fecha factura
            sheet.write(filas, 11, invoice[11]) #comercial
            sheet.write(filas, 12, invoice[15]) #forma de pago
            filas+=1
        coltotal= 'A'+str(filas+1)+':'+'F'+str(filas+1)
        sheet.merge_range(coltotal, 'TOTALES',letter5) #fecha
        sheet.write(filas, 6, total_bruto,letter5) #importe neto
        sheet.write(filas, 7, total_descuento,letter5) #importe neto
        sheet.write(filas, 8, total_neto,letter5) #importe neto



    def amount_bruto(self,invoice_id):
        invoices_line = self.env['account.invoice.line'].sudo().search([('invoice_id', '=', invoice_id)])
        monto=0.00
        for line in invoices_line:
            monto += (line.price_unit * line.quantity)
        return monto

    def amount_discount(self,invoice_id):
        invoices_line = self.env['account.invoice.line'].sudo().search([('invoice_id', '=', invoice_id)])
        monto=0.00
        monto_discount=0.00
        for line in invoices_line:
            if line.discount > 0.00:
                monto = (line.price_unit * line.quantity)
                monto_discount += (monto*line.discount)/100
        return monto_discount