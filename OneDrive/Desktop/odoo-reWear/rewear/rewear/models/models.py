from odoo import models, fields, api
from odoo.exceptions import ValidationError

class RewearItem(models.Model):
    _name = 'rewear.item'
    _description = 'Clothing Exchange Item'
    _order = 'id desc'

    title = fields.Char(required=True)
    description = fields.Text()
    category = fields.Selection([
        ('men', 'Men'),
        ('women', 'Women'),
        ('kids', 'Kids'),
        ('accessories', 'Accessories'),
        ('other', 'Other'),
    ], required=True)
    type = fields.Char(string='Type')
    size = fields.Selection([
        ('xs', 'XS'), ('s', 'S'), ('m', 'M'), ('l', 'L'), ('xl', 'XL'), ('xxl', 'XXL'),
        ('kids', 'Kids'), ('other', 'Other'),
    ], required=True)
    condition = fields.Selection([
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('worn', 'Worn'),
    ], required=True)
    tags = fields.Char(string='Tags')
    image = fields.Binary(string='Image')
    points_cost = fields.Integer(required=True, default=10)
    availability = fields.Selection([
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('swapped', 'Swapped'),
        ('unavailable', 'Unavailable'),
    ], default='available')
    owner_id = fields.Many2one('res.users', string='Owner', required=True, ondelete='cascade')

    def action_redeem(self):
        for item in self:
            if item.owner_id.points_balance < item.points_cost:
                raise ValidationError('Not enough points to redeem this item.')
            item.owner_id.points_balance -= item.points_cost
            item.availability = 'swapped'

class ResUsers(models.Model):
    _inherit = 'res.users'
    points_balance = fields.Integer(string='Points Balance', default=0)

# Optional: Swap model for direct swaps
class RewearSwap(models.Model):
    _name = 'rewear.swap'
    _description = 'Clothing Swap Request'
    requester_id = fields.Many2one('res.users', string='Requester', required=True)
    owner_id = fields.Many2one('res.users', string='Owner', required=True)
    item_id = fields.Many2one('rewear.item', string='Item', required=True)
    status = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')

