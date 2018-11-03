# -*- coding: utf-8 -*-
{
   'name': "同步钉钉通讯录",
   'summary': """odoo员工和钉钉员工同步""",
   'description': """
   
功能
=======

* 一键将钉钉中部门及用户同步至odoo部门和员工中


   """,
   'author': "lhy",
   'website': "http://www.yourcompany.com",

   'category': 'Tools',
   'version': '0.1',

   'depends': ['base', 'web', 'hr'],
   'data': [
      'views/employee_ext_views.xml',
      'wizard/generate_dingd_transient_views.xml',
      'views/res_config_settings_views.xml',
   ],

}