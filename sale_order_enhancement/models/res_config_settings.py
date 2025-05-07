# -*- coding: utf-8 -*-
###############################################################################
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """inherited the 'res.config.settings' to add custom fields"""
    _inherit = 'res.config.settings'

    sale_order_limit = fields.Float(
        string='Sale Order Limit',
        config_parameter='sale_order_enhancement.sale_order_limit',
        help='Sale Order Total Amount Limit')

    auto_workflow = fields.Boolean(
        string="Auto Workflow",
        config_parameter='sale_order_enhancement.auto_workflow',
        help='Sale-Delivery-Invoice-Payment Automation')
