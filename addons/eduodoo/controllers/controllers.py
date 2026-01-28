# -*- coding: utf-8 -*-
# from odoo import http


# class Eduodoo(http.Controller):
#     @http.route('/eduodoo/eduodoo', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/eduodoo/eduodoo/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('eduodoo.listing', {
#             'root': '/eduodoo/eduodoo',
#             'objects': http.request.env['eduodoo.eduodoo'].search([]),
#         })

#     @http.route('/eduodoo/eduodoo/objects/<model("eduodoo.eduodoo"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('eduodoo.object', {
#             'object': obj
#         })

