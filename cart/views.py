from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from movies.models import Movie
from .utils import calculate_cart_total
from .models import Order, Item
from django.contrib.auth.decorators import login_required

#index function is designed to render the cart page
#showing the movies in the cart & the total cost of these movies
def index(request):
    cart_total = 0
    movies_in_cart = []
    #Retrieve cart information from session
    cart = request.session.get('cart', {})
    movie_ids = list(cart.keys())
    if (movie_ids != []):
        movies_in_cart = Movie.objects.filter(id__in=movie_ids)
        cart_total = calculate_cart_total(cart,
            movies_in_cart)
    template_data = {}
    template_data['title'] = 'Cart'
    template_data['movies_in_cart'] = movies_in_cart
    template_data['cart_total'] = cart_total
    return render(request, 'cart/index.html',
        {'template_data': template_data})

def add(request, id):
    get_object_or_404(Movie, id=id)
    #check storage session for a key called cart
    #If it doesnt't exist then cart will be an empty dictionary
    cart = request.session.get('cart', {})
    #id is movie id & we assign the number of that movie to add to cart
    cart[id] = request.POST['quantity']
    request.session['cart'] = cart
    #Redirect users to home page
    return redirect('cart.index')

def clear(request):
    #Empty cart
    request.session['cart'] = {}
    #Redirect to cart home page
    return redirect('cart.index')

@login_required
def purchase(request):
    cart = request.session.get('cart', {})
    #Retrieve movie ids stored in cart (since they are the keys)
    #Then converted them to a list called movie_ids
    movie_ids = list(cart.keys())
    #no movie ids, redirect user to cart.index page
    if (movie_ids == []):
        return redirect('cart.index')
    #Retrieve all movies based on their ids
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    #Calculate total cost of movies
    cart_total = calculate_cart_total(cart, movies_in_cart)
    #Create Order object and set attributes
    order = Order()
    order.user = request.user
    order.total = cart_total
    order.save()
    #Iterate over movies and create Item object for each movie
    #Set price & quantity for each Item, and link to movie & order
    for movie in movies_in_cart:
        item = Item()
        item.movie = movie
        item.price = movie.price
        item.order = order
        item.quantity = cart[str(movie.id)]
        item.save()
    #Clear cart after session is over
    request.session['cart'] = {}
    template_data = {}
    #Prepare data to be sent to payment confirmation page
    template_data['title'] = 'Purchase confirmation'
    template_data['order_id'] = order.id
    #Render cart/purchase.html
    return render(request, 'cart/purchase.html',
        {'template_data': template_data})