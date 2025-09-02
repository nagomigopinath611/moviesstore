#To calculate total price of movies in cart & display total amount
#Not recommended to do this under views or models file

def calculate_cart_total(cart, movies_in_cart):
    total = 0
    for movie in movies_in_cart:
        #Keys are movie ids so we access the quantity like this
        quantity = cart[str(movie.id)]
        total += movie.price * int(quantity)
    return total