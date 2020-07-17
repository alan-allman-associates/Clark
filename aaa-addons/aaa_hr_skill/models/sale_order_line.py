from odoo import api,fields, models
from odoo.addons import decimal_precision as dp


import logging

_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    #marge_unitaire_k2 = fields.Float(compute='_compute_marge_k2', string='Marge unitaire k2')
    percent_marge_unitaire_k2 = fields.Float(compute='_product_margin', string='% Marge unitaire K2')
    order_name = fields.Char(related="order_id.name")
    opportunity_id = fields.Many2one(related='order_id.opportunity_id')
    employee_id = fields.Many2one('hr.employee', string="Consultant")
    expenses = fields.Float(string="Expenses")

    @api.onchange('employee_id')
    def _compute_cost_k2(self):
        for line in self:
            line.purchase_price = line.employee_id.cost_k2 or 0
 
    @api.depends('product_id', 'expenses', 'purchase_price', 'product_uom_qty', 'price_unit', 'price_subtotal')
    def _product_margin(self):
        """ 
            % marge unitaire k2 = ((Marge unitaire K2) / quantité )/HJM [prix de vente] *100
        """
        for line in self:
            currency = line.order_id.pricelist_id.currency_id
            price = line.purchase_price or 0
            price += line.expenses or 0
            qty = line.product_uom_qty
            margin = currency.round(line.price_subtotal - (price * qty))
            line.margin = margin
            price = line.price_unit
            if price > 0 and qty > 0:
                line.percent_marge_unitaire_k2 = (margin / qty) / price * 100
    
    
    @api.onchange('margin')
    def _alert_margin(self):
        for order_line in self :
            # on recalcule la marge de la commande
            order_margin = 0
            for line in order_line.order_id.order_line : 
                
                # on ne prend pas les lignes dont le produit est le même que la ligne en cours (Odoo génère des lignes en brouillon quand on change une valeur)
                # cette condition permet d'éviter de prendre les doublons de ligne en compte et de fausser la marge
                if line.state != 'cancel' and (line.product_id.id != order_line.product_id.id or line.id == order_line.id) :
                    order_margin += line.margin
            
            # on calcule la marge cible
            order_line.order_id._compute_order_margin_cible()
            
            
            if order_margin < order_line.order_id.marge_k2_cible :
                if order_line.product_id :
                    message = "Attention, la marge sur le devis est inférieure à l'objectif de l'équipe de vente."
                    mess= {
                            'title': 'Marge trop faible !',
                            'message' : message
                        }
                    return {'warning': mess}
        return {}
    
    # fonction permettant de générer les tâches sur un projet défini (ou non)
    # on modifie seulement la génération de la tâche sur un projet existant 
    # si un projet est rattaché à la commande, on génère les tâches sur ce projet, peu importe le projet sélectionné sur l'article
    @api.multi
    def _timesheet_service_generation(self):
        """ For service lines, create the task or the project. If already exists, it simply links
            the existing one to the line.
            Note: If the SO was confirmed, cancelled, set to draft then confirmed, avoid creating a
            new project/task. This explains the searches on 'sale_line_id' on project/task. This also
            implied if so line of generated task has been modified, we may regenerate it.
        """
        so_line_task_global_project = self.filtered(lambda sol: sol.is_service and sol.product_id.service_tracking == 'task_global_project')
        so_line_new_project = self.filtered(lambda sol: sol.is_service and sol.product_id.service_tracking in ['project_only', 'task_new_project'])

        # search so lines from SO of current so lines having their project generated, in order to check if the current one can
        # create its own project, or reuse the one of its order.
        map_so_project = {}
        if so_line_new_project:
            order_ids = self.mapped('order_id').ids
            so_lines_with_project = self.search([('order_id', 'in', order_ids), ('project_id', '!=', False), ('product_id.service_tracking', 'in', ['project_only', 'task_new_project']), ('product_id.project_template_id', '=', False)])
            map_so_project = {sol.order_id.id: sol.project_id for sol in so_lines_with_project}
            so_lines_with_project_templates = self.search([('order_id', 'in', order_ids), ('project_id', '!=', False), ('product_id.service_tracking', 'in', ['project_only', 'task_new_project']), ('product_id.project_template_id', '!=', False)])
            map_so_project_templates = {(sol.order_id.id, sol.product_id.project_template_id.id): sol.project_id for sol in so_lines_with_project_templates}

        # search the global project of current SO lines, in which create their task
        # Si un projet est rattaché au bon de commande, on ne s'occupe pas de celui indiqué sur l'article (pour toutes les lignes)
        # si aucun projet n'est rattaché, on garde le fonctionnement normal
        map_sol_project = {}
        if so_line_task_global_project:
            # dans les lignes qui crééent une tâche, on cherche celles dont la commande a un projet rattaché
            sol_with_projet_rattache = self.search([('order_id.projet_rattache', '!=', False), ('id', 'in', so_line_task_global_project.ids)])
            
            # si un projet est déjà rattaché à la ligne sur l'article, on ne s'en occupe pas et on prend celui de la commande
            if len(sol_with_projet_rattache) > 0 :
                map_sol_project = {sol.id: sol.order_id.projet_rattache for sol in sol_with_projet_rattache}
            # sinon, fonctionnement normal
            else : 
                map_sol_project = {sol.id: sol.product_id.with_context(force_company=sol.company_id.id).project_id for sol in so_line_task_global_project}
            
        def _can_create_project(sol):
            if not sol.project_id:
                if sol.product_id.project_template_id:
                    return (sol.order_id.id, sol.product_id.project_template_id.id) not in map_so_project_templates
                elif sol.order_id.id not in map_so_project:
                    return True
            return False

        # task_global_project: create task in global project
        for so_line in so_line_task_global_project:
            if not so_line.task_id:
                if map_sol_project.get(so_line.id):
                    so_line._timesheet_create_task(project=map_sol_project[so_line.id])

        # project_only, task_new_project: create a new project, based or not on a template (1 per SO). May be create a task too.
        for so_line in so_line_new_project:
            project = so_line.project_id
            if not project and _can_create_project(so_line):
                project = so_line._timesheet_create_project()
                if so_line.product_id.project_template_id:
                    map_so_project_templates[(so_line.order_id.id, so_line.product_id.project_template_id.id)] = project
                else:
                    map_so_project[so_line.order_id.id] = project
            elif not project:
                # Attach subsequent SO lines to the created project
                so_line.project_id = (
                    map_so_project_templates.get((so_line.order_id.id, so_line.product_id.project_template_id.id))
                    or map_so_project.get(so_line.order_id.id)
                )
            if so_line.product_id.service_tracking == 'task_new_project':
                if not project:
                    if so_line.product_id.project_template_id:
                        project = map_so_project_templates[(so_line.order_id.id, so_line.product_id.project_template_id.id)]
                    else:
                        project = map_so_project[so_line.order_id.id]
                if not so_line.task_id:
                    so_line._timesheet_create_task(project=project)

class SaleOrder(models.Model):
    _inherit = 'sale.order'    
    
    @api.depends('margin')
    def _compute_order_margin_cible(self):
        for order in self :
            
            marge_k2_cible = (order.amount_untaxed * order.team_id.percent_marge_cible_team) / 100
            order.marge_k2_cible = marge_k2_cible
            
    marge_k2_cible = fields.Monetary(compute='_compute_order_margin_cible', digits=dp.get_precision('Product Price'), store=True, currency_field='currency_id')
    projet_rattache = fields.Many2one(
                        string='Projet rattaché',
                        comodel_name='project.project',
                    )
    
    def _send_mail_alerte_margin(self):
        """
            Fonction d'envoi de mail au responsable si la marge de la commande est trop faible par rapport 
            à l'objectif prévu sur l'équipe de vente
            
            user_id = vendeur
        """
        # on cherche l'employé lié au vendeur, puis on récupère le gestionnaire :
        gestionnaire = self.env['hr.employee'].search([('user_id', '=', self.user_id.id)]).parent_id
        
        # on cherche l'adresse mail du gestionnaire (employé -> utilisateur -> partenaire)
        mail_gestionnaire = False
        if gestionnaire :
            mail_gestionnaire = gestionnaire.user_id.partner_id.email
            
        if mail_gestionnaire : 
            # envoi du mail d'alerte
            template = self.env.ref('aaa_hr_skill.mail_alerte_margin_devis')

            emailValues = self.env['mail.template'].browse(template.id).generate_email(self.id)
            emailValues['email_to'] = mail_gestionnaire
            msg_id = self.env['mail.mail'].create(emailValues)
            msg_id.send()
    
    @api.multi
    def write(self, values):
        
        result = super(SaleOrder, self).write(values)
        
        # si la marge de la commande est inférieure à la marge cible de l'équipe, on prévient le responsable du vendeur
        if self.margin < self.marge_k2_cible : 
            self._send_mail_alerte_margin()

        return result
    
    @api.model
    def create(self, values):
        
        result = super(SaleOrder, self).create(values)
        
        # si la marge de la commande est inférieure à la marge cible de l'équipe, on prévient le responsable du vendeur
        if result.margin < result.marge_k2_cible : 
            result._send_mail_alerte_margin()

        return result
    
           