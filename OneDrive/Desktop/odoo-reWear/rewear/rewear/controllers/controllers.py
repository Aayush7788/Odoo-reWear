# from odoo import http


# class Rewear(http.Controller):
#     @http.route('/rewear/rewear', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/rewear/rewear/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rewear.listing', {
#             'root': '/rewear/rewear',
#             'objects': http.request.env['rewear.rewear'].search([]),
#         })

#     @http.route('/rewear/rewear/objects/<model("rewear.rewear"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rewear.object', {
#             'object': obj
#         })

