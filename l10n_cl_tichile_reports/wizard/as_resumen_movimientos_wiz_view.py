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

class ew_movimientos_ubicacion_wiz(models.TransientModel):
    _name = "as.movimientos.ubicacion.wiz"
    _description = "Movimientos de ubicacion"

    start_date = fields.Date('Desde la Fecha', default=lambda *a: (datetime.now() - timedelta(hours = 4)).strftime('%Y-%m-%d'))
    end_date = fields.Date('Hasta la Fecha', default=lambda *a: (datetime.now() - timedelta(hours = 4)).strftime('%Y-%m-%d'))
    location = fields.Many2one('stock.location', 'Ubicacion', domain="[('usage','!=','view')])")

    def imprimir_excel(self,cr,uid,filtros,context=None):
        self_browse = self.browse(cr, uid, filtros[0])
        picking_obj = self.pool.get('stock.picking')

        cr.execute('''
            SELECT
            sp.id AS id_picking
            FROM stock_picking AS sp
            JOIN stock_picking_type AS spt ON spt.id = sp.picking_type_id
            WHERE spt.code = 'internal' and sp.state in ('done')
            AND ((sp.min_date AT TIME ZONE 'UTC' AT TIME ZONE 'BOT')::timestamp::date) BETWEEN %s AND %s
            AND sp.location_dest_id = %s
        ''',([self_browse.start_date,self_browse.end_date,self_browse.location.id]))
        # AND (sp.location_id = %s OR sp.location_dest_id = %s) # Colocar si es para cualquier posicion
        lista_id_picking = [i for i in cr.fetchall()]
        lista_ids  = []
        for lista in lista_id_picking:
            lista_ids.append(lista[0])

        import base64
        filename= 'transferencias_internas.xls'
        workbook= xlwt.Workbook(encoding="UTF-8")
        worksheet= workbook.add_sheet('Transferencias Internas')

        worksheet.col(0).width = 260 * 11
        worksheet.col(1).width = 260 * 11
        worksheet.col(2).width = 260 * 9
        worksheet.col(3).width = 260 * 15
        worksheet.col(4).width = 260 * 15
        worksheet.col(5).width = 260 * 12

        titulo = xlwt.easyxf('font:height 400, bold True, name Arial; align: horiz center, vert center;')
        titulo2 = xlwt.easyxf('font:height 160, bold True, name Arial; align: horiz center, vert center,wrap on;borders: top medium,bottom medium')
        titulo3 = xlwt.easyxf('font:height 200, bold True, name Arial; align: horiz center, vert center')
        titulo4 = xlwt.easyxf('font:height 200, bold True, name Arial; align: horiz left, vert center')
        info = xlwt.easyxf('font:height 160, bold True, name Arial; align: horiz left, vert center;')
        info_center = xlwt.easyxf('font:height 160, bold True, name Arial; align: horiz center, vert center;')
        info2 = xlwt.easyxf('font:height 160, bold False, name Arial; align: horiz left, vert center;')
        cuentas_y_analticas = xlwt.easyxf('font:height 140, bold True, name Arial; align: horiz left, vert center; borders: top thin, bottom thin;')

        datos1 = xlwt.easyxf('font:height 140, bold False, name Arial; align: horiz left, vert center, wrap on;')
        datos2 = xlwt.easyxf('font:height 140, bold False, name Arial; align: horiz center, vert center, wrap on;')
        datos3 = xlwt.easyxf('font:height 140, bold False, name Arial; align: horiz right, vert center, wrap on;',num_format_str='#,##0.00')
        datos3_enteros = xlwt.easyxf('font:height 140, bold False, name Arial; align: horiz right, vert center, wrap on;',num_format_str='#,##0')
        datos3_negrita = xlwt.easyxf('font:height 140, bold True, name Arial; align: horiz right, vert center, wrap on;',num_format_str='#,##0.00')

        totales1 = xlwt.easyxf('font:height 140, bold True; align: horiz left, vert center; borders: top medium')
        totales2 = xlwt.easyxf('font:height 140, bold True; align: horiz center, vert center; borders: top medium')
        totales3 = xlwt.easyxf('font:height 140, bold True; align: horiz right, vert center; borders: top medium',num_format_str='#,##0.00')
        totales3_enteros = xlwt.easyxf('font:height 140, bold True; align: horiz right, vert center; borders: top medium',num_format_str='#,##0')

        fecha_inicial = 'Fecha Inicial: ' + str(self_browse.start_date)
        fecha_final = 'Fecha Final: ' + str(self_browse.end_date)
        ubicacion = 'Ubicacion ' + self_browse.location.name
        
        worksheet.write_merge(0,0,0,5, self_browse.location.company_id.name, info_center)
        worksheet.write_merge(1,1,0,5, 'Detalle de Transferencias Ingresos', info_center)
        worksheet.write_merge(2,2,0,2,fecha_inicial, info)
        worksheet.write_merge(2,2,4,5,fecha_final, info)
        worksheet.write_merge(3,3,0,5, ubicacion, info_center)

        worksheet.write(4,0,'Nro Importacion',titulo2)
        worksheet.write(4,1,'Ref Proveedor',titulo2)
        worksheet.write(4,2,'Fecha',titulo2)
        worksheet.write(4,3,'Almacen Origen',titulo2)
        worksheet.write(4,4,'Almacen Destino',titulo2)
        worksheet.write(4,5,'Importe $us.',titulo2)

        fila = 4

        def obtener_total_importe_picking(cr,uid,id_picking):
            sum_importes = 0
            move_obj = self.pool.get('stock.move')
            move_search = move_obj.search(cr,uid,[('picking_id','=',id_picking)])
            for move in move_obj.browse(cr,uid,move_search):
                sum_importes += (move.price_unit or -1) * move.product_qty
                # sum_importes += move.product_id.standard_price * move.product_uom_qty
            return sum_importes

        total_importe_dolares = 0

        for picking in picking_obj.browse(cr,uid,lista_ids):
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

        fp = StringIO()
        workbook.save(fp)
        export_id = self.pool.get('excel.extended').create(cr, uid, {'excel_file': base64.encodestring(fp.getvalue()), 'file_name': filename}, context=context)
        fp.close()
        return{
            'view_mode': 'form',
            'res_id': export_id,
            'res_model': 'excel.extended',
            'view_type': 'form',
            'type': 'ir.actions.act_window',
            'context': context,
            'target': 'new',
        }