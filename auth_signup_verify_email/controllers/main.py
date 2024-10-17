# Copyright 2015 Antiun Ingeniería, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from email_validator import EmailSyntaxError, EmailUndeliverableError, validate_email
from odoo.exceptions import ValidationError, AccessError, MissingError, UserError

from odoo import _
from odoo.http import request, route

from odoo.addons.auth_signup.controllers.main import AuthSignupHome

_logger = logging.getLogger(__name__)


class SignupVerifyEmail(AuthSignupHome):
    @route()
    def web_auth_signup(self, *args, **kw):
        if request.params.get("login") and not request.params.get("password"):
            return self.passwordless_signup()
        return super().web_auth_signup(*args, **kw)

    def passwordless_signup(self):
        print("........passwordless_signup......")
        values = request.params
        qcontext = self.get_auth_signup_qcontext()
        print("......qcontext.....===========.....", qcontext)
        # Check good format of e-mail
        exist = False
        ikama = request.env['ebs_mod.contact.ikama'].sudo().search([('ikama_no', '=', values['id_no'])])
        if len(ikama) > 0:
            for i in ikama:
                if i.family_member == 'me':
                    exist = True
        if exist:
            qcontext["error"] = _(
                "QID Number Already Exists"
            )
            return request.render("auth_signup.signup", qcontext)

        try:
            validate_email(values.get("login", ""))
        except EmailSyntaxError as error:
            qcontext["error"] = getattr(
                error, "message", _("That does not seem to be an email address."),
            )
            return request.render("auth_signup.signup", qcontext)
        except EmailUndeliverableError as error:
            qcontext["error"] = str(error)
            return request.render("auth_signup.signup", qcontext)
        except Exception as error:
            qcontext["error"] = str(error)
            return request.render("auth_signup.signup", qcontext)
        if not values.get("email"):
            values["email"] = values.get("login")
        if not values.get("id_no"):
            values["id_no"] = values.get("id_no")

        # preserve user lang
        values["lang"] = request.context.get("lang", "")
        # remove values that could raise "Invalid field '*' on model 'res.users'"
        values.pop("redirect", "")
        values.pop("token", "")

        # Remove password
        values["password"] = ""
        sudo_users = request.env["res.users"].with_context(create_user=True).sudo()

        try:
            with request.cr.savepoint():
                existing_user = request.env["res.users"].sudo().search(
                    [('password', '=', False), ('state', '=', 'new'), ('login', '=', values.get("login"))])
                password_set_user = request.env["res.users"].sudo().search([('login', '=', values.get("login"))])
                if existing_user:
                    # existing_user.write({'active': True})
                    existing_user.with_context(create_user=True).reset_password(values.get("login"))
                elif password_set_user:
                    qcontext["message"] = _("Mail is already sended")
                    return request.render("auth_signup.reset_password", qcontext)
                else:
                    sudo_users.signup(values, qcontext.get("token"))
                    sudo_users.reset_password(values.get("login"))

        except Exception as error:
            # Duplicate key or wrong SMTP settings, probably
            _logger.exception(error)
            if (
                    request.env["res.users"]
                            .sudo()
                            .search([("login", "=", qcontext.get("login"))])
            ):
                qcontext["error"] = _(
                    "Another user is already registered using this email" " address."
                )
            else:
                # Agnostic message for security
                qcontext["error"] = _(
                    "Something went wrong, please try again later or" " contact us."
                )
            return request.render("auth_signup.signup", qcontext)

        qcontext["message"] = _("Check your email to activate your account!")
        return request.render("auth_signup.reset_password", qcontext)

    def do_signup(self, qcontext):
        print("./././././...............", qcontext)
        values = {key: qcontext.get(key) for key in
                  ('login', 'name', 'password', 'id_no', 'user_access', 'sign_up_access')}
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.context.get('lang', '').split('_')[0]
        if lang in supported_lang_codes:
            values['lang'] = lang

        self._signup_with_values(qcontext.get('token'), values)
        request.env.cr.commit()
