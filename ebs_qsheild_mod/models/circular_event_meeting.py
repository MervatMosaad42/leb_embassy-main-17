from odoo import models, fields, api, _
from odoo.tools.translate import html_translate


class CircularPage(models.Model):
    _name = 'circulars.page'
    _description = "circulars page"

    name = fields.Char(string='Title',required=True)
    date = fields.Date(string='Date')
    description = fields.Html("Descriptions" , translate=html_translate)
    image = fields.Binary('Image')
    active = fields.Boolean('Active',default=True)
    page_active = fields.Boolean('Active')
    attachment_id = fields.Many2one('ir.attachment', string="Attachment", attachment=True)


class CircularPage(models.Model):
    _name = 'meetings.meetings'
    _description = "meetings"

    name = fields.Char(string='Title',required=True)
    date = fields.Date(string='Date')
    description = fields.Html("Descriptions", translate=html_translate)
    image = fields.Binary('Image')
    active = fields.Boolean('Active',default=True)
    page_active = fields.Boolean('Active')
    image_ids = fields.One2many('multi.image','meeting_image_id',string="Extra image",copy=True)


class CircularPage(models.Model):
    _name = 'events_activities.events_activities'
    _description = "events and activities"

    name = fields.Char(string='Title',required=True)
    date = fields.Date(string='Date')
    description = fields.Html("Descriptions", translate=html_translate)
    image = fields.Binary('Image')
    page_active = fields.Boolean('Active')
    active = fields.Boolean('Active',default=True)
    image_ids = fields.One2many('multi.image','activity_image_id',string="Extra image",copy=True)


class MultiImage(models.Model):
    _name = 'multi.image'
    _order = 'sequence, id'

    activity_image_id = fields.Many2one('events_activities.events_activities')
    meeting_image_id = fields.Many2one('meetings.meetings')
    image = fields.Many2one('ir.attachment',"File",required=True)
    name = fields.Char("Name", required=True)
    sequence = fields.Integer(default=10, index=True)
    type = fields.Selection([
        ('image', 'Image'),
        ('video', 'Video'),
    ],required=True)


class IrAttachmentInherit(models.Model):
    _inherit = 'ir.attachment'

    @api.model_create_multi
    def create(self, vals_list):
        res = super(IrAttachmentInherit, self).create(vals_list)
        if res:
            res.public = True
        return res

