import base64
import hashlib
import mimetypes
from odoo import models, fields, api, http
from odoo.tools.mimetypes import get_extension, guess_mimetype
from odoo.tools import consteq, pycompat
from odoo.http import request, content_disposition


class InheritIrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def _binary_record_content(
            self, record, field='datas', filename=None,
            filename_field='name', default_mimetype='application/octet-stream'):

        model = record._name
        mimetype = 'mimetype' in record and record.mimetype or False
        content = None
        filehash = 'checksum' in record and record['checksum'] or False

        field_def = record._fields[field]
        if field_def.type == 'binary' and field_def.attachment:
            field_attachment = self.env['ir.attachment'].sudo().search_read(domain=[('res_model', '=', model), ('res_id', '=', record.id), ('res_field', '=', field)], fields=['datas', 'mimetype', 'checksum'], limit=1)
            if field_attachment:
                mimetype = field_attachment[0]['mimetype']
                content = field_attachment[0]['datas']
                filehash = field_attachment[0]['checksum']

        if not content:
            content = record[field] or ''

        # filename
        if not filename:
            if filename_field in record:
                filename = record[filename_field]
            if not filename:
                filename = "%s-%s-%s" % (record._name, record.id, field)

        if not mimetype:
            try:
                decoded_content = base64.b64decode(content)
            except base64.binascii.Error:  # if we could not decode it, no need to pass it down: it would crash elsewhere...
                return (404, [], None)
            mimetype = guess_mimetype(decoded_content, default=default_mimetype)

        # extension
        has_extension = get_extension(filename) or mimetypes.guess_type(filename)[0]
        if not has_extension:
            extension = mimetypes.guess_extension(mimetype)
            if extension:
                filename = "%s%s" % (filename, extension)

        if not filehash:
            filehash = '"%s"' % hashlib.md5(pycompat.to_text(content).encode('utf-8')).hexdigest()

        status = 200 if content else 404
        return status, content, filename, mimetype, filehash


    def _binary_set_headers(self, status, content, filename, mimetype, unique, filehash=None, download=False):
        headers = [('Content-Type', mimetype), ('X-Content-Type-Options', 'nosniff'), ('Content-Security-Policy', "default-src 'none'")]
        # cache
        etag = bool(request) and request.httprequest.headers.get('If-None-Match')
        status = status or 200
        if filehash:
            headers.append(('ETag', filehash))
            if etag == filehash and status == 200:
                status = 304
        headers.append(('Cache-Control', 'max-age=%s' % (http.STATIC_CACHE_LONG if unique else 0)))
        # content-disposition default name
        if download:
            headers.append(('Content-Disposition', content_disposition(filename)))

        return (status, headers, content)