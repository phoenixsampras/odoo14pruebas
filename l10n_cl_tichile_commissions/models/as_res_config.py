# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    as_type_comissions = fields.Selection([
        ('Porcentaje (%)', 'Porcentaje (%)'),
        ('Monto Fijo', 'Monto Fijo')
    ], default="Porcentaje (%)",string="Tipo de Comisión a Aplicar")
    group_comissions_porcentaje = fields.Boolean("Comsion por porcentaje",
        implied_group="l10n_cl_tichile_commissions.group_comissions_porcentaje")
    group_comissions_monto = fields.Boolean("Comisión por precio fijo",
        implied_group="l10n_cl_tichile_commissions.group_comissions_monto")    
    group_comissions_clientes = fields.Boolean("Comisión por cliente", implied_group="l10n_cl_tichile_commissions.group_comissions_clientes")
    group_comissions_productos = fields.Boolean("Comisión por productos", implied_group="l10n_cl_tichile_commissions.group_comissions_productos")
    as_type_modality = fields.Selection([
        ('Clientes', 'Clientes'),
        ('Productos', 'Productos')
    ], default="Productos",string="Modalidad de Comisión a Aplicar")
    

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res['as_type_comissions'] = (self.env['ir.config_parameter'].sudo().get_param('res_config_settings.as_type_comissions'))
        res['as_type_modality'] = (self.env['ir.config_parameter'].sudo().get_param('res_config_settings.as_type_modality'))
        return res

    @api.model
    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param('res_config_settings.as_type_comissions', self.as_type_comissions)
        self.env['ir.config_parameter'].sudo().set_param('res_config_settings.as_type_modality', self.as_type_modality)
        super(ResConfigSettings, self).set_values()

    @api.onchange('as_type_comissions')
    def _onchange_as_type_comissions(self):
        if self.as_type_comissions == 'Porcentaje (%)':
            self.update({
                'group_comissions_porcentaje': True,
                'group_comissions_monto': False,
            })
        elif self.as_type_comissions == 'Monto Fijo':
            self.update({
                'group_comissions_porcentaje': False,
                'group_comissions_monto': True,
            })

    @api.onchange('as_type_modality')
    def _onchange_as_type_modality(self):
        if self.as_type_modality == 'Clientes':
            self.update({
                'group_comissions_clientes': True,
                'group_comissions_productos': False,
            })
        elif self.as_type_modality == 'Productos':
            self.update({
                'group_comissions_clientes': False,
                'group_comissions_productos': True,
            })
        