# -*- coding: utf-8 -*-
import requests
import json
import werkzeug
from werkzeug.exceptions import BadRequest
from odoo import api, fields, models, _


class GenerateDingdingDepartment(models.TransientModel):
    _name = 'generate_dingd_department'
    _description = '根据主部门1，生成多个部门'
    department_id = fields.Char(string='部门id', default='1')

    def get_access_token(self):
        obj = self.env['ir.config_parameter'].sudo()
        appkey = obj.get_param('dingtalk.appkey', default='')
        appsecret = obj.get_param('dingtalk.appsecret', default='')
        if not appkey or not appsecret:
            raise werkzeug.exceptions.NotFound()
        url = "https://oapi.dingtalk.com/gettoken?appkey=%s&appsecret=%s" % (appkey, appsecret)
        result = requests.get(url).text
        # {
        #     "errcode": 0,
        #     "errmsg": "ok",
        #     "access_token": "fw8ef8we8f76e6f7s8df8s"
        # }
        result = json.loads(result)
        if result['errcode'] == 0:
            return result['access_token']
        else:
            raise werkzeug.exceptions.BadRequest(result['errmsg'])

    @api.multi
    def generate_ding_department(self):
        access_token = self.get_access_token()
        department_id = self.department_id
        url = 'https://oapi.dingtalk.com/department/list?access_token=%s&id=%s' % (access_token, department_id)

        resp = requests.get(url).text
        result = json.loads(resp)

        if result['errcode'] == 0:
            # 获取所有的部门信息列表
            ret_li = result["department"]
            # 遍历每一个部门
            for data in ret_li:

                    ding_department_id_li = self.env['hr.department'].search_read(domain=[], fields=['ding_id'])
                    ding_department_lis = [data['ding_id'] for data in ding_department_id_li]
                    # 判断部门id是否已存在，不存在，则进行新建部门
                    if str(data['id']) not in ding_department_lis:
                        self.env['hr.department'].create(
                            {'name': data['name'],
                             'ding_id': data['id'],
                             # 'parent_id': data['parentid']
                             }
                        )
                    # 通过部门id，获取该部门的用户id列表，创建用户
                    dep_id = data['id']
                    # 获取当前的部门对象
                    hr_department_id = self.env['hr.department'].search([('ding_id', '=', dep_id)])

                    url = 'https://oapi.dingtalk.com/user/getDeptMember?access_token=%s&deptId=%s' % (
                        access_token, dep_id)
                    response = requests.get(url).text
                    response = json.loads(response)

                    if response['errcode'] == 0:
                        # 获取用户的userid列表
                        user_li = response['userIds']

                        # 获取部门员工的钉钉userid
                        for user_id in user_li:
                            # 先循环，再获取userid列表
                            ding_user_id_li = self.env['hr.employee'].search_read(domain=[], fields=['ding_userid'])
                            ding_user_lis = [data['ding_userid'] for data in ding_user_id_li]
                            if user_id not in ding_user_lis:
                                url = 'https://oapi.dingtalk.com/user/get?access_token=%s&userid=%s' % (access_token, user_id)
                                resp = requests.get(url).text
                                resp = json.loads(resp)
                                if resp['errcode'] == 0:
                                    self.env['hr.employee'].create(
                                        {'name': resp['name'],
                                         'department_id': hr_department_id.id,
                                         'ding_userid': resp['userid'],
                                         'work_location': resp['workPlace'],
                                         # 'job_id': resp['position'],
                                         'mobile_phone': resp['mobile'],
                                         'work_email': resp['email'],
                                         }
                                    )
                                else:
                                    raise werkzeug.exceptions.BadRequest(resp['errmsg'])

                    else:
                        raise werkzeug.exceptions.BadRequest(response['errmsg'])

        else:
            raise werkzeug.exceptions.BadRequest(result['errmsg'])



