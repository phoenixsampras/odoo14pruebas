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
    _name = 'report.l10n_cl_tichile_reports.as_pdf_report_ventas_producto'
    
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
                 AND so.date_order::date <= '"""+str(data['end_date'])+"""'
                """ + str(filtro_vendedores_po) + """
           
            and so.state in ('sale','done','sent')
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
        consultas_ventas = (""" SELECT
            ai.id
            ,to_char((ai.fecha_boliviana AT TIME ZONE 'UTC' AT TIME ZONE 'BOT')::date,'DD/MM/YYYY') AS fecha
            ,to_char((ai.date_due AT TIME ZONE 'UTC' AT TIME ZONE 'BOT')::date,'DD/MM/YYYY') AS fecha_vencimiento
            ,so.name as nro_nota
            ,so.as_numeracion_interna AS numero_interno	
            ,ai.invoice_number AS numero_interno_factura	
            ,ai.state
            ,ai.amount_total AS importe
            ,so.as_pagado AS pagado
            ,so.as_saldo as saldo			
            ,sl.name as almacen
            ,so.id
            ,ai.id
            FROM sale_order AS so
            left join account_invoice ai on ai.origin = so.name
            JOIN res_users AS usuarios ON usuarios.id = so.user_id
            JOIN res_partner AS asesor ON asesor.id = usuarios.partner_id
            LEFT JOIN res_partner AS cliente ON cliente.id = so.partner_id
            left join as_metodo_pago_ventas mp on mp.id = so.as_forma_pago_id
            left join stock_picking sp on sp.origin=so.name
            join stock_location sl on sp.location_id=sl.id 
            WHERE
            cliente.id = """+str(ciente_id)+""" AND so.date_order::date <= '"""+str(data['end_date'])+"""' """ + str(filtro_vendedores_po) + """ """ + str(filtro_almacen) + """ and ai.state='open' and so.state NOT IN ('cancel','draft') group by 1,2,3,4,5,6,7,8,9,10,11,12,13""")
        self.env.cr.execute(consultas_ventas)
        ventas = [k for k in self.env.cr.fetchall()]
        nuevo = []
        for lines in ventas:
            if lines[2] != None and lines[6] == 'open':
                state='PEN'
                if lines[2] != None and (datetime.now() - timedelta(hours = 4)).strftime('%d/%m/%Y') >= lines[2] and lines[6] == 'open':
                    state='VEN'
                fecha_order = (datetime.now() - timedelta(hours = 4))
                fecha_vence = datetime.strptime(str(lines[2]), '%d/%m/%Y')
                dias = fecha_order - fecha_vence
                consultas_pagos = ("""
                    SELECT
                    as_venta,sum(as_pago) from as_account_payments_line
                    WHERE
                    as_venta = """+str(lines[12])+""" and as_estado='Valido' group by 1
                    """)
                self.env.cr.execute(consultas_pagos)
                pagos = [k for k in self.env.cr.fetchall()]
                abonos = 0.0
                if pagos:
                    abonos = float(pagos[0][1])
                movimientos_vencidos.append(lines+tuple([state])+tuple([dias.days])+tuple([abonos]))
        return movimientos_vencidos
