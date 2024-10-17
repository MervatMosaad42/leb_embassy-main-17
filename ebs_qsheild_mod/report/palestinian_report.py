from odoo import fields, models, api


class Plaestinianreport(models.AbstractModel):
    _name = 'report.ebs_qsheild_mod.report_palestiniansejel'
    _description = 'Palestinian Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        print("----------call--palestinian---------")
        model = 'res.partner'
        docs = self.env[model].browse(docids)
        emp_dependent = False
        if docs.employee_dependants:
            emp_dependent = docs.mapped('employee_dependants')[-1]
        address = False
        if docs.address_ids:
            address = docs.mapped('address_ids')[-1]
        contactikama = False
        if docs.contact_ikama:
            contactikama = docs.mapped('contact_ikama')[-1]
        contactpassport = False
        if docs.contact_passports:
            contactpassport = docs.mapped('contact_passports')[-1]
        contactemergency = False
        if docs.contact_emergency:
            contactemergency = docs.mapped('contact_emergency')[-1]
        return {
            'doc_ids': docids,
            'doc_model': model,
            'data': data,
            'docs': docs,
            'emp_dependent':emp_dependent,
            'address':address,
            'contactikama':contactikama,
            'contactpassport':contactpassport,
            'contactemergency':contactemergency,
        }
