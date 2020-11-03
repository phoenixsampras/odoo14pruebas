# -*- coding: utf-8 -*-
{
    'name': 'AhoraSoft Modulo de Comisiones en Venta',
    'version': '1.0.1',
    'category': 'sale',
    'author': 'Ahorasoft',
    'summary': 'Customized comisiones Management',
    'website': 'http://www.ahorasoft.com',
    'depends': [
        'base',
        'sale','product', 'report_xlsx'
    ],
    'data': [
        'security/as_group_view.xml',
        'security/ir.model.access.csv',
        'wizard/as_report_comisiones.xml',
        'views/as_history_commissions.xml',
        'views/as_tabla_comisiones.xml',
        'views/as_res_config.xml',
        'views/as_product_pricelist.xml',
        'views/sale_order_inherit_view.xml',
        'views/as_product_template.xml',
        'views/as_partner.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}