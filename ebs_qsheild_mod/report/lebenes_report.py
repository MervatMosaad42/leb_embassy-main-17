from odoo import fields, models, api


class LebeneseReport(models.AbstractModel):
    _name = 'report.ebs_qsheild_mod.report_leabanesejel_custom2'
    _description = 'Lebenese Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        print("----------call-----------")
        model = 'res.partner'
        docs = self.env[model].browse(docids)
        print("---------docs-------------", docs)
        emp_dependent = False
        if docs.employee_dependants:
            emp_dependent = docs.employee_dependants.filtered(lambda x: x.dependent_type == 'child')
            # emp_dependent = docs.mapped('employee_dependants')
            print("---------------emp_dependent--------", emp_dependent)
        lbn_address = False
        qtr_address = False
        if docs.address_ids:
            lbn_address = docs.address_ids.filtered(lambda add: add.type == 'Lebanon')
            lbn_address = lbn_address and lbn_address[-1] or False
            qtr_address = docs.address_ids.filtered(lambda add: add.type == 'Qatar')
            qtr_address = qtr_address and qtr_address[-1] or False
        contactikama = False
        if docs.contact_ikama:
            contactikama = docs.mapped('contact_ikama')[-1]
            print("-------------------contact------", contactikama)
        contactpassport = False
        if docs.contact_passports:
            contactpassport = docs.mapped('contact_passports')[-1]
            # print("------------lead---------",contactikama.ikama_no)
        # for i in contactikama:
        #     print("ikama.ikama_no",i.ikama_no,"ikama.partner_id._get_arabic_date_employee(ikama.ikama_enddate)",i.partner_id._get_arabic_date_employee(i.ikama_enddate))

        return {
            'doc_ids': docids,
            'doc_model': model,
            'data': data,
            'docs': docs,
            'emp_dependent': emp_dependent,
            'lbn_address': lbn_address,
            'qtr_address': qtr_address,
            'contactikama': contactikama,
            'contactpassport': contactpassport,
        }

