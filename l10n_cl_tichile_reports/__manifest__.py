# -*- coding: utf-8 -*-
{
    'name': 'AhoraSoft Modulo de Reportes Varios',
    'version': '1.0.1',
    'category': 'sale',
    'author': 'Ahorasoft',
    'summary': 'Customized sale Management',
    'website': 'http://www.ahorasoft.com',
    'depends': [
        'sale',
        'base','product', 'stock', 'resource','purchase','report_xlsx'
    ],
    'data': [
        # 'security/as_group_view.xml',
        'security/ir.model.access.csv',
        'views/as_menu_report.xml',
        'wizard/as_ventas_por_producto.xml',
        'wizard/as_cuentas_pagar_detalle.xml',
        'wizard/as_cuentas_cobrar_detalle.xml',
        'wizard/as_ventas_por_clientes_por_producto.xml',
        'wizard/as_resumen_por_ventas.xml',
        'wizard/as_ventas_por_vendedor.xml',
        'wizard/as_kardex_productos_wiz.xml',
        'wizard/as_ventas_sucursal_dia.xml',
        'wizard/as_reporte_por_ventas_por_utilidad.xml',
        'wizard/as_reporte_por_lista_de_productos.xml',
        'wizard/as_reporte_ingresos_inventario.xml',
        'wizard/as_reporte_salidas_inventario.xml',
        'report/as_cuentas_por_pagar_pdf.xml',
        'report/as_ventas_por_producto_pdf.xml',
        'report/as_ventas_por_cliente_por_producto_pdf.xml',
        'report/as_cuentas_por_cobrar_pdf.xml',
        'report/as_resumen_por_ventas_pdf.xml',
        'report/as_ventas_por_sucursal_por_dia_pdf.xml',
        'views/as_report_format.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}