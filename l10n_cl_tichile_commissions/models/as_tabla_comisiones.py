# -*- coding: utf-8 -*-

from odoo import tools
from odoo import models, fields, api, _
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)

class tfResPartner(models.Model):
    _name = "as.tabla.comisiones"
    _description = "Tabla de Comisiones a Vendedores"

    as_desde = fields.Float('Desde')
    as_hasta = fields.Float('Hasta')
    as_comision = fields.Float('Comision')
    as_division = fields.Boolean('Calculo por division',default=False)