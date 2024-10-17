# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, AccessError, MissingError, UserError
from odoo.http import request, route

class ResUsers(models.Model):
    _inherit = 'res.users'
    id_no = fields.Char(
        string='ID',
        required=False)
    user_access = fields.Selection([('seekers','Seekers'),('company','Company')])
    sign_up_access = fields.Selection([('electronic_service','electronic_service'),('recruitment','recruitment')])

    @api.model
    def create(self, vals):
        res = super(ResUsers, self).create(vals)

        if 'id_no' in vals:
            user_partner = res.partner_id
            ikama = self.env['ebs_mod.contact.ikama'].sudo().search([('ikama_no', '=', vals['id_no'])])
            if len(ikama) > 0:
                par = None
                exist = False
                for i in ikama:
                    if i.family_member == 'me':
                        exist = True
                if exist:
                    raise UserError(_("There is another user with same QID."))
                else:
                    par = i.dependent

                if par is not None and not exist:
                    parent = par.parent_id
                    par.sudo().write({
                        'parent_id': None
                    })
                    user_partner.id_no = vals['id_no']
                    user_partner.parent_id = parent.id
                    user_partner.name = par.name
                    user_partner.firstName = par.firstName
                    user_partner.middleName = par.middleName
                    user_partner.lastName = par.lastName
                    user_partner.first_name_en = par.first_name_en
                    user_partner.middle_name_en = par.middle_name_en
                    user_partner.last_name_en = par.last_name_en
                    user_partner.dependent_type = par.dependent_type
                    user_partner.nationality = par.nationality
                    user_partner.country_id = par.country_id
                    user_partner.sejelNo = par.sejelNo
                    user_partner.function = par.function
                    user_partner.marriage_place = par.marriage_place
                    user_partner.marriage_date = par.marriage_date
                    user_partner.schoolName = par.schoolName
                    user_partner.motherFullName = par.motherFullName
                    user_partner.placeOfBirth = par.placeOfBirth
                    user_partner.phone = par.phone
                    user_partner.date = par.date
                    user_partner.father_fullname = par.father_fullname
                    user_partner.kazaBirth = par.kazaBirth
                    user_partner.company_name = par.company_name
                    user_partner.street = par.street
                    user_partner.first_Nationality = par.first_Nationality
                    user_partner.person_type = 'emp'
            self.env['ebs_mod.contact.ikama'].sudo().create({
                'ikama_no':  vals['id_no'],
                'is_active': True,
                'partner_id': user_partner.id,
                'family_member': 'me'
            })

        return res

    @api.model
    def signup(self, values, token=None):
        """ signup a user, to either:
            - create a new user (no token), or
            - create a user for a partner (with token, but no user for partner), or
            - change the password of a user (with token, and existing user).
            :param values: a dictionary with field values that are written on user
            :param token: signup token (optional)
            :return: (dbname, login, password) for the signed up user
        """
        print(".//......values.........", values)

        print("...................\n\n\n\.=====token=======",token)



        if token:
            # signup with a token: find the corresponding partner id
            partner = self.env['res.partner']._signup_retrieve_partner(token, check_validity=True, raise_exception=True)
            # invalidate signup token

            partner.write({'signup_token': False, 'signup_type': False, 'signup_expiration': False})
            partner_user = partner.user_ids and partner.user_ids[0] or False
            print("......partner_user..........",partner_user)

            # avoid overwriting existing (presumably correct) values with geolocation data
            if partner.country_id or partner.zip or partner.city:
                values.pop('city', None)
                values.pop('country_id', None)
            if partner.lang:
                values.pop('lang', None)

            if partner_user:
                # user exists, modify it according to values
                values.pop('login', None)
                values.pop('name', None)
                partner_user.write(values)
                if not partner_user.login_date:
                    partner_user._notify_inviter()
                return (self.env.cr.dbname, partner_user.login, values.get('password'))
            else:
                # user does not exist: sign up invited user
                values.update({
                    'name': partner.name,
                    'partner_id': partner.id,
                    'email': values.get('email') or values.get('login'),
                })
                if partner.company_id:
                    values['company_id'] = partner.company_id.id
                    values['company_ids'] = [(6, 0, [partner.company_id.id])]
                partner_user = self._signup_create_user(values)
                partner_user._notify_inviter()
        else:
            # no token, sign up an external user
            values['email'] = values.get('email') or values.get('login')
            partner_user = self._signup_create_user(values)
        if values.get("sign_up_access") == 'recruitment':
            if values.get("user_access", False) and values.get("user_access") == 'company' and partner_user:
                company_group = request.env.ref('ebs_qsheild_mod.company_profile_grp')
                company_group.sudo().write({
                    'users': [(4, partner_user.id)]
                })
                partner_user.sudo().write({
                    'person_type': 'child',
                    'applicant_user_boolean': True
                })
            if values.get("user_access", False) and values.get("user_access") == 'seekers' and partner_user:
                partner_user.sudo().write({
                    'applicant_user_boolean': True
                })
        return (self.env.cr.dbname, values.get('login'), values.get('password'))
