from odoo import models, fields, api, _


def count():
    return 5


class ServiceTypes(models.Model):
    _name = 'ebs_mod.service.types'
    _description = "Service Types"
    _parent_name = 'parent_service_id'

    _sql_constraints = [
        ('service_type_code_unique', 'unique (code)',
         'Code must be unique !'),
        ('service_type_name_unique', 'unique (name)',
         'Name must be unique !')
    ]

    contract_id = fields.Many2one('ebs_mod.contracts')

    service_image = fields.Binary("Image")

    parent_service_id = fields.Many2one(
        comodel_name='ebs_mod.service.types',
        string='Parent Service',
        required=False)

    code = fields.Char(
        string='Code',
        required=True)

    path = fields.Char(
        string='Path',
        required=False)

    name = fields.Char(
        string='Name (Arabic)',
        required=True)
    name_en = fields.Char(
        string='Name (English)',
        required=False)

    inactive = fields.Boolean(string="Inactive")
    active = fields.Boolean(string="Active")

    def _get_name(self):
        locale = self._context.get('lang') or 'en_US'
        # ar_001 for arabic

        if locale == 'en_US':
            name = self.name_en or self.name
        else:
            name = self.name or ''
        return name

    def name_get(self):
        res = []
        for service in self:
            name = service._get_name()
            res.append((service.id, name))
        return res

    sla = fields.Char(
        string='SLA - Working Days',
        required=False)

    sla_min = fields.Integer(
        string='SLA - Minimum Days',
        required=False)

    sla_max = fields.Integer(
        string='SLA - Maximum Days',
        required=False)

    parent = fields.Boolean(
        string='Parent',
        required=False,
        default=False)

    for_lebanese = fields.Boolean(
        string='For Lebanese',
        required=False,
        default=False)

    for_palestinian = fields.Boolean(
        string='For Palestinian',
        required=False,
        default=False)

    for_others = fields.Boolean(
        string='For Others',
        required=False,
        default=False)

    for_company = fields.Boolean(
        string='For Company',
        required=False,
        default=False)

    for_employee = fields.Boolean(
        string='For Employee',
        required=False,
        default=False)

    for_visitor = fields.Boolean(
        string='For Visitor',
        required=False,
        default=False)

    for_dependant = fields.Boolean(
        string='For Dependant',
        required=False,
        default=False)

    for_miscellaneous = fields.Boolean(
        string='For Miscellaneous',
        required=False,
        default=False)
    for_not_miscellaneous = fields.Boolean(
        string='For Not Miscellaneous',
        required=False,
        default=False)

    workflow_online_ids = fields.One2many(
        comodel_name='ebs_mod.service.type.workflow',
        inverse_name='service_type_id',
        string='Workflow Online',
        required=False,
        domain=[('flow_type', '=', 'o')])

    workflow_manual_ids = fields.One2many(
        comodel_name='ebs_mod.service.type.workflow',
        inverse_name='service_type_id',
        string='Workflow Manual',
        required=False,
        domain=[('flow_type', '=', 'm')])

    document_types = fields.Many2many(
        comodel_name='ebs_mod.document.types',
        string='Document Types'
    )
    
    terms_conditions = fields.Html(
        string='Terms and Conditions',
        required=False)

    logout_terms_conditions = fields.Html(
        string='Logout Terms and Conditions',
        required=False
    )


    read_group_ids = fields.Many2many(
        comodel_name='res.groups',
        string='Read Groups')


    # document_types_ids = fields.One2many(
    #     comodel_name='ebs_mod.document.types',
    #     inverse_name='service_type_id',
    #     string='Document Types',
    #     required=False)

    def count(self):
        cnt = self.env['ebs_mod.service.types'].search_count(
            [('parent_service_id', '=', self.id)])
        return cnt

    @api.model
    def create(self, vals):
        res = super(ServiceTypes, self).create(vals)
        for rec in self.env['ebs_mod.service.workflow.config'].search([]):
            self.env['ebs_mod.service.type.workflow'].create({
                'name': rec.name,
                'sequence': rec.sequence,
                'flow_type': rec.flow_type,
                'start_count_flow': rec.start_count_flow,
                'service_type_id': res.id,
            })
        return res


class ServiceTypeWorkflow(models.Model):
    _name = "ebs_mod.service.type.workflow"
    _description = "Service Type Workflow"
    _order = "sequence"
    name = fields.Char(
        string='Name',
        required=True)
    sequence = fields.Integer(
        string='Sequence',
        required=True, default=0)
    flow_type = fields.Selection(
        string='Type',
        selection=[('o', 'Online'),
                   ('m', 'Manual'), ],
        required=True)

    start_count_flow = fields.Boolean(
        string='Start Count Flow',
        required=False,
        default=False)

    service_type_id = fields.Many2one(
        comodel_name='ebs_mod.service.types',
        string='Service_type',
        required=False)

    _sql_constraints = [
        ('service_type_flow_name_type_unique', 'unique (service_type_id,name,flow_type)',
         'Name and type combination must be unique !')
    ]
