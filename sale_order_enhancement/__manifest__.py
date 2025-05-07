# -*- coding: utf-8 -*-
#############################################################################
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
#############################################################################
{
    'name': 'Sale Order Enhancement',
    'version': '17.0.1.0.0',
    'category': 'Sale',
    'summary': 'Automates the full sales workflow from quotation to payment with'
               ' configurable amount limits.',
    'description': 'Adds a configurable sale order amount limit and an '
                   '"Auto Workflow" option that automates the full sales '
                   'flow: confirmation, delivery creation (split per product), '
                   'validation, invoice posting, and payment registration.',
    'maintainer': '',
    'company': '',
    'website': '',
    'depends': ['base', 'sale_management', 'stock', 'account'],
    'data': [
        'security/sale_order_enhancement_groups.xml',
        'views/sale_order_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
