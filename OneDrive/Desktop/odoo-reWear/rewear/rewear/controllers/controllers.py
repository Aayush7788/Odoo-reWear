from odoo import http
from odoo.http import request

class RewearWebsite(http.Controller):
    @http.route('/', type='http', auth='public', website=True)
    def landing(self, **kw):
        featured_items = request.env['rewear.item'].search([('availability', '=', 'available')], limit=5)
        return request.render('rewear.landing', {'featured_items': featured_items})

    @http.route('/rewear/browse', type='http', auth='public', website=True)
    def browse(self, **kw):
        items = request.env['rewear.item'].search([('availability', '=', 'available')])
        return request.render('rewear.browse', {'items': items})

    @http.route('/rewear/item/<int:item_id>', type='http', auth='public', website=True)
    def item_detail(self, item_id, **kw):
        item = request.env['rewear.item'].sudo().browse(item_id)
        return request.render('rewear.item_detail', {'item': item})

    @http.route('/rewear/add', type='http', auth='user', website=True, methods=['GET', 'POST'])
    def add_item(self, **post):
        if request.httprequest.method == 'POST':
            vals = {
                'title': post.get('title'),
                'description': post.get('description'),
                'category': post.get('category'),
                'type': post.get('type'),
                'size': post.get('size'),
                'condition': post.get('condition'),
                'tags': post.get('tags'),
                'image': post.get('image'),
                'points_cost': int(post.get('points_cost', 10)),
                'owner_id': request.env.user.id,
            }
            request.env['rewear.item'].sudo().create(vals)
            # Award points to user (logic can be improved)
            request.env.user.sudo().points_balance += 10
            return request.redirect('/my/dashboard')
        return request.render('rewear.add_item', {})

    @http.route('/my/dashboard', type='http', auth='user', website=True)
    def user_dashboard(self, **kw):
        user = request.env.user
        my_items = request.env['rewear.item'].search([('owner_id', '=', user.id)])
        my_swaps = request.env['rewear.swap'].search([('requester_id', '=', user.id)])
        return request.render('rewear.user_dashboard', {
            'user': user,
            'my_items': my_items,
            'my_swaps': my_swaps,
        })

