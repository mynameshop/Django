from __future__ import unicode_literals
from collections import OrderedDict

PRICING_TEMPLATE_SILVER = {
    'id': 1,
    'slug': 'silver-12', 
    'title': 'SILVER', 
    'subscription_cost': 12,
    'description': 'A perfect solution for<br>customers with simple<br>products.',
    'composition': [
        '3D Model of Product', 
        'Up to 3 Product Styles', 
        'Social Media Assets', 
        'Product Support', 
        ''
    ]
}
PRICING_TEMPLATE_GOLD = {
    'id': 2,
    'slug': 'gold-15', 
    'title': 'GOLD', 
    'subscription_cost': 15,
    'description': 'A great choice for<br>customers to show<br>how their product works.',
    'composition': [
        '3D Model of Product', 
        'Up to 5 Product Styles',
        'Up to 5 Animations',
        'Social Media Assets', 
        'Product Support',
    ]
}
                        
PRICING_TEMPLATE_PLATINUM = {
    'id': 3,
    'slug': 'platinum-19', 
    'title': 'PLATINUM', 
    'subscription_cost': 19,
    'description': 'A fantastic option for<br>customers whose detailed products<br>require complex animation.',
    'composition': [
        '3D Model of Product', 
        'Up to 15 Product Styles',
        'Up to 20 Interactive Animations',
        'Social Media Assets',
        'Product Support',
    ]
}

PRICING_TEMPLATES = OrderedDict([
    ('silver', PRICING_TEMPLATE_SILVER),
    ('gold', PRICING_TEMPLATE_GOLD),
    ('platinum', PRICING_TEMPLATE_PLATINUM),
])

PRICING_TEMPLATES_CHOICES = (
    (1, 'silver'),
    (2, 'gold'),
    (3, 'platinum'),
)