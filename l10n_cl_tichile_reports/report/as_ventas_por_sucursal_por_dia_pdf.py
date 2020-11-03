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
    _name = 'report.l10n_cl_tichile_reports.as_pdf_sucursal_dia'

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
            'result_clientes': self.result_clientes_line(data['form']),

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
            rcs.name
            ,rp.vat
            ,rp.name
            ,rp.business_name
            ,rp.phone
            ,rp.mobile
            ,rp.id
            from res_partner rp
            left join res_country_state rcs on rp.state_id = rcs.id
            where customer=True
                """ + str(filtro_clientes) + """
            """)
        self.env.cr.execute(consulta_clientes)
        clientes = [k for k in self.env.cr.fetchall()]
        nuevo_clientes = []
        for client in clientes:
            client = client+tuple([{'invoices':self.result_clientes_line(client[6],data)}])
            nuevo_clientes.append(client)
        return nuevo_clientes
        
    def result_clientes_line(self,data):
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
        consultas_ventas = (""" SELECT 
            to_char((so.date_order AT TIME ZONE 'UTC' AT TIME ZONE 'BOT')::date,'DD/MM/YYYY') AS fecha
            ,sl.name as almacen
            ,sol.product_uom_qty
            ,uu.name
            ,sol.price_unit
            FROM sale_order AS so
            join sale_order_line sol on sol.order_id = so.id
            join uom_uom uu on uu.id = sol.product_uom
            left join account_move ai on ai.invoice_origin = so.name and ai.state='open'
            JOIN res_users AS usuarios ON usuarios.id = so.user_id
            JOIN res_partner AS asesor ON asesor.id = usuarios.partner_id
            LEFT JOIN res_partner AS cliente ON cliente.id = so.partner_id
            left join stock_picking sp on sp.origin=so.name
            left join stock_location sl on sp.location_id=sl.id """ + str(filtro_almacen) + """ 
            WHERE
            so.date_order::date <= '"""+str(data['end_date'])+"""' """ + str(filtro_vendedores_po) + """  and so.state NOT IN ('cancel','draft') """)
        self.env.cr.execute(consultas_ventas)
        ventas = [k for k in self.env.cr.fetchall()]
        nuevo = []
        array_fechas=[]
        arrays=[]
        if ventas != []:
            for transation in ventas:
                fecha = str(transation[0])
                if not fecha in array_fechas:
                    array_fechas.append(fecha)
            array_fechas.sort()
            for lines in array_fechas:
                moves = []
                total = 0.0
                for transation in ventas:
                    if str(transation[0]) == lines:
                        total += transation[2]*transation[4]
                        moves.append(transation)
                if moves:
                    arrays.append((lines,tuple([{'invoices':moves}]),total))
        return arrays
