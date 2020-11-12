# -*- coding: utf-8 -*-
from odoo import api, models, fields,_
from odoo.exceptions import UserError
from datetime import datetime
import time
import calendar
from datetime import datetime, timedelta
from time import mktime
import time
from time import mktime
from dateutil.relativedelta import relativedelta

class ReportTax(models.AbstractModel):
    _name = 'report.l10n_cl_tichile_reports.as_pdf_salida_inventario'
    
    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise UserError(_("Form content is missing, this report cannot be printed."))
        fechaf = datetime.strptime(str(data['form']['end_date']), '%Y-%m-%d').strftime('%d/%m/%Y')
        fechai = datetime.strptime(str(data['form']['start_date']), '%Y-%m-%d').strftime('%d/%m/%Y')
        return {
            'data': data['form'],
            'fechai': fechai,
            'fechaf': fechaf,
            'usuario': self.get_user(data['form']),
            'cliente': self.get_cliente(data['form']),
            'sucursal': self.get_sucursal(data['form']),
            'ciudad': self.get_ciudad(data['form']),
            'result_clientes': self.result_clientes(data['form']),

        }
    
    def get_user(self,data):
        usuarios = ''
        if data['user_ids']:
            usuario = self.env['res.users'].sudo().search([('id', '=',data['user_ids'][0])])
            for user in usuario:
                usuarios=str(user.partner_id.name)
        else:
            usuarios='Todos'
        return usuarios    
    
    def get_sucursal(self,data):
        registro = ''
        if data['location_ids']:
            modelo = self.env['stock.location'].sudo().search([('id', '=',data['location_ids'][0])])
            for user in modelo:
                registro=str(user.name)
        else:
            registro='Todos'
        return registro

    def get_cliente(self,data):
        registro = ''
        if data['partner_ids']:
            modelo = self.env['res.partner'].sudo().search([('id', '=',data['partner_ids'][0])])
            for user in modelo:
                registro=str(user.name)
        else:
            registro='Todos'
        return registro    
    
    def get_ciudad(self,data):
        registro = ''
        if data['city_ids']:
            modelo = self.env['res.country.state'].sudo().search([('id', '=',data['city_ids'][0])])
            for user in modelo:
                registro=str(user.name)
        else:
            registro='Todos'
        return registro

    def result_clientes(self,data):
        dict_vendedores = []
        filtro_almacen = ''
        if data['user_ids']:
            for ids in data['user_ids']:
                dict_vendedores.append(ids)
        if dict_vendedores:
            filtro_vendedores_po = "AND usuarios.id in "+str(dict_vendedores).replace('[','(').replace(']',')')
        else:
            filtro_vendedores_po = ''

        dict_clientes = []
        if data['partner_ids']:
            for ids in data['partner_ids']:
                dict_clientes.append(ids)
        if dict_clientes:
            filtro_clientes = "AND rp.id in "+str(dict_clientes).replace('[','(').replace(']',')')
        else:
            filtro_clientes = ''
        
        dict_almacen = []
        if data['location_ids']:
            for ids in data['location_ids']:
                dict_almacen.append(ids)
        if dict_almacen:
            filtro_almacen = "AND sl.id in "+str(dict_almacen).replace('[','(').replace(']',')')
        else:
            almacenes = self.env['stock.location'].sudo().search([('usage', '=', 'internal')])
            for almecen in almacenes:
                dict_almacen.append(almecen.id)
            filtro_almacen = "AND sl.id in "+str(dict_almacen).replace('[','(').replace(']',')')

        consulta_clientes = ("""
            SELECT 
            sm.id
            ,to_char((sm.date AT TIME ZONE 'UTC' AT TIME ZONE 'BOT')::date,'DD/MM/YYYY') AS fecha
            ,sp.name
            ,sp.origin
            ,rp.name
            ,pp.default_code
            ,pt.name
            ,sm.product_qty
            ,COALESCE(sm.price_unit,0.0) 
            ,pc.name
            ,sp.state
            ,sl1.name
            ,sl2.name
            FROM stock_move sm
            join stock_picking sp on sp.id = sm.picking_id
            join product_product pp on pp.id= sm.product_id
            join sale_order so on so.name =sp.origin and so.state in ('sale','done','sent')
            join res_partner rp on rp.id= sp.partner_id
            join product_template pt on pt.id=pp.product_tmpl_id
            left join product_category pc on pc.id = pt.categ_id
            left join stock_location sl1 on sm.location_id=sl1.id
            left join stock_location sl2 on sm.location_dest_id=sl2.id
                """ + str(filtro_clientes) + """
                 AND so.date_order::date <= '"""+str(data['end_date'])+"""'
            """)
        self.env.cr.execute(consulta_clientes)
        clientes = [k for k in self.env.cr.fetchall()]
        nuevo_clientes = []
        for client in clientes:
            nuevo_clientes.append(client)
        return nuevo_clientes
        
    def result_clientes_line(self,ciente_id,data):
        dict_city_ids = []
        dict_almacen = []
        dict_vendedores = []
        filtro_almacen=''
        movimientos_vencidos = []
        if data['user_ids']:
            for ids in data['user_ids']:
                dict_vendedores.append(ids)
        if dict_vendedores:
            filtro_vendedores_po = "AND usuarios.id in "+str(dict_vendedores).replace('[','(').replace(']',')')
        else:
            filtro_vendedores_po = ''
        if data['city_ids']:
            for ids in data['city_ids']:
                dict_city_ids.append(ids)
        if dict_city_ids:
            filtro_vendedores_po += " AND cliente.state_id in "+str(dict_city_ids).replace('[','(').replace(']',')')
        else:
            filtro_vendedores_po += ''
        if data['location_ids']:
            for ids in data['location_ids']:
                dict_almacen.append(ids)
        if dict_almacen:
            filtro_almacen = "AND sl.id in "+str(dict_almacen).replace('[','(').replace(']',')')
        else:
            almacenes = self.env['stock.location'].sudo().search([('usage', '=', 'internal')])
            for almecen in almacenes:
                dict_almacen.append(almecen.id)
            filtro_almacen = "AND sl.id in "+str(dict_almacen).replace('[','(').replace(']',')')
        consultas_ventas = ("""    SELECT 
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
            join sale_order so on so.name =sp.origin and so.state in ('sale','done','sent')
            join res_partner rp on rp.id= sp.partner_id
            join product_template pt on pt.id=pp.product_tmpl_id
            left join product_category pc on pc.id = pt.categ_id
            left join stock_location sl1 on sm.location_id=sl1.id
            left join stock_location sl2 on sm.location_dest_id=sl2.id
                """ + str(filtro_clientes) + """
                 AND so.date_order::date <= '"""+str(data['form']['end_date'])+"""'
                """ + str(filtro_product) + """
                """)
        self.env.cr.execute(consultas_ventas)
        ventas = [k for k in self.env.cr.fetchall()]
        nuevo = []
        for lines in ventas:
            movimientos_vencidos.append(lines)
        return movimientos_vencidos
