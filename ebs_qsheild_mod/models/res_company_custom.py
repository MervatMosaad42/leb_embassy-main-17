from odoo import fields, models, api, _


class ResConfigSettingCustom(models.Model):
    _inherit = "res.company"

    disable_future_date_service = fields.Boolean(
        string='Disable Future Date in Service Request',
        Default=True,readonly=False
    )
    name = fields.Char(string="Name", translate=True)

    shift_description = fields.Text(string="Shift Description" , translate=True)
    
    map_location = fields.Char(default="Map Location", translate=True)

    ambassador_name = fields.Char('Ambassador Name',required=True, translate=True)

    description = fields.Html(string='Description', required=True, translate=True)

    image = fields.Binary("Image")



