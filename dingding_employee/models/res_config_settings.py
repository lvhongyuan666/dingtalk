# -*- coding: utf-8 -*-
from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    dingtalk_app_key = fields.Char(string='钉钉appkey')
    dingtalk_app_Secret = fields.Char(string='钉钉appSecret')

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        params = self.env['ir.config_parameter'].sudo()
        params.set_param('dingtalk.appkey', self[0].dingtalk_app_key)
        params.set_param('dingtalk.appsecret', self[0].dingtalk_app_Secret)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            dingtalk_app_key=params.get_param('dingtalk.appkey', default=''),
            dingtalk_app_Secret=params.get_param('dingtalk.appsecret', default=''),
        )
        return res
