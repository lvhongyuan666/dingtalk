# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class DingUser(models.Model):
    _inherit = "hr.employee"
    _description = '钉钉用户和员工同步'

    work_id = fields.Char(string='工号')
    ding_userid = fields.Char(string='钉钉用户id')

    _sql_constraints = [
        ('work_id_unique',
         'UNIQUE(work_id)',
         "The work_id must be unique"),
    ]


class DingDepartment(models.Model):
    _inherit = "hr.department"
    _description = '钉钉部门和odoo部门同步'

    ding_id = fields.Char(string='部门id')
    ding_active = fields.Char(string='同步钉钉', default='钉钉同步')

    _sql_constraints = [
        ('work_id_unique',
         'UNIQUE(ding_id)',
         "The ding_id must be unique"),
    ]


