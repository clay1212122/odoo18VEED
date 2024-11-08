# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    insz_or_bis_number = fields.Char("INSZ or BIS number", groups="hr.group_hr_user")
    clocked_session_ids = fields.Many2many(
        "pos.session",
        "employees_session_clocking_info",
        string="Users Clocked In",
        groups="hr.group_hr_user",
        help="This is a technical field used for tracking the status of the session for each employees.",
    )

    @api.constrains("insz_or_bis_number")
    def _check_insz_or_bis_number(self):
        for emp in self:
            insz_number = emp.insz_or_bis_number
            if insz_number and not self.is_valid_insz_or_bis_number(insz_number):
                raise ValidationError(_("The INSZ or BIS number is not valid."))

    def is_valid_insz_or_bis_number(self, number):
        if not number:
            return False
        if len(number) != 11 or not number.isdigit():
            return False

        partial_number = number[:-2]
        modulo = int(partial_number) % 97

        return modulo == 97 - int(number[-2:])

    @api.model
    def _load_pos_data_fields(self, config_id):
        result = super()._load_pos_data_fields(config_id)
        config_id = self.env["pos.config"].browse(config_id)
        if config_id.iface_fiscal_data_module:
            result += ['insz_or_bis_number']
        return result
