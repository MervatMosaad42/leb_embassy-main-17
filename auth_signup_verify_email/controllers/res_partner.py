# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import random
import werkzeug.urls

from collections import defaultdict
from datetime import datetime, timedelta

from odoo import api, exceptions, fields, models, _

class SignupError(Exception):
    pass

def random_token():
    # the token has an entropy of about 120 bits (6 bits/char * 20 chars)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.SystemRandom().choice(chars) for _ in range(20))

def now(**kwargs):
    return datetime.now() + timedelta(**kwargs)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def signup_retrieve_info(self, token):
        partner = self._signup_retrieve_partner(token, raise_exception=True)
        res = {'db': self.env.cr.dbname}
        if partner.signup_valid:
            res['token'] = token
            res['name'] = partner.name
        if partner.user_ids:
            res['login'] = partner.user_ids[0].login
            res['id_no'] = partner.user_ids[0].id_no
            print(res['id_no'])
        else:
            res['email'] = res['login'] = partner.email or ''

        return res
