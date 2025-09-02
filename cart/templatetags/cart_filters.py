#import template module
from django import template

#Create an instance of template.Library
#To register custom template tags & filters
register = template.Library()
@register.filter(name='get_quantity')
def get_cart_quantity(cart, movie_id):
    return cart[str(movie_id)]