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
from odoo import fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    """
    This class extends the 'sale.order' model to Update Functionalities
    """
    _inherit = 'sale.order'

    manager_reference = fields.Text(string='Manager Reference', help="Manager Reference value here")

    is_manager_ref_editable = fields.Boolean(compute="_compute_manager_ref_editable")

    def _compute_manager_ref_editable(self):
        """Method checking the user contains the group"""
        is_sale_admin = self.env.user.has_group('sale_order_enhancement.sale_admin_user')
        for rec in self:
            rec.is_manager_ref_editable = is_sale_admin


    def action_confirm(self):
        """Validate amount based on sale order limit and user group and automation workflow
        ***For the first DELIVERY we have to Enable or disable SMS option manually to
        AUTOMATE the Validation function***"""
        res = super().action_confirm()
        # sale order limit-------------------------------------------------------------------------------------
        sale_order_limit = self.env['ir.config_parameter'].sudo().get_param('sale_order_enhancement.sale_order_limit')
        if (sale_order_limit and self.amount_total > float(sale_order_limit)
                and not self.env.user.has_group('sale_order_enhancement.sale_admin_user')):
            raise ValidationError("The amount exceeds the allowed limit for this user.")

        # multiple deliveries against each product Auto Workflow is enabled------------------------------------
        auto_workflow = self.env['ir.config_parameter'].sudo().get_param('sale_order_enhancement.auto_workflow')
        if auto_workflow:
            line_list = [{"product": rec.product_id, "qty": rec.product_uom_qty, "line_id": rec.id} for rec in self.order_line]

            for line in line_list:
                picking = self.env['stock.picking'].create({
                    'partner_id': self.partner_id.id,
                    'sale_id': self.id,
                    'origin': self.name,
                    'location_id': self.env.ref('stock.stock_location_stock').id,
                    'location_dest_id': self.env.ref('stock.stock_location_customers').id,
                    'picking_type_id': self.env.ref('stock.picking_type_out').id,
                    'move_ids': [(0, 0, {
                        'name': line.get('product').name,
                        'product_id': line.get('product').id,
                        'product_uom_qty': line.get('qty'),
                        'quantity': line.get('qty'),
                        'sale_line_id': line.get('line_id'),
                        'location_id': self.env.ref('stock.stock_location_stock').id,
                        'location_dest_id': self.env.ref('stock.stock_location_customers').id,
                    })]
                })
                picking.write({
                    'sale_id': self.id,
                })

        # Auto Workflow [Sale -> Delivery -> Invoice -> Payment]-----------------------------------------------
        if auto_workflow:
            for rec in self.picking_ids:
                if rec.state != 'cancel' and rec.state != 'done':
                    rec.action_confirm()
                    rec.action_assign()
                    rec.button_validate()

            invoice = self._create_invoices()
            if invoice:
                invoice.action_post()
                # Register payment
                payment_wizard = self.env[
                    'account.payment.register'].with_context(
                    active_model='account.move',
                    active_ids=invoice.ids
                ).create({
                    'amount': invoice.amount_residual,
                    'payment_date': fields.Date.today(),
                    'journal_id': self.env['account.journal'].search([('type', '=', 'bank')], limit=1).id,
                    'payment_method_line_id': self.env.ref('account.account_payment_method_manual_in').id,
                    'partner_id': self.partner_id.id,
                    'communication': invoice.name,
                })
                payment_wizard.action_create_payments()
        return res
