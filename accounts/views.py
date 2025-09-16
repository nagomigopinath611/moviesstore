from django.shortcuts import render
#import for user authentication
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
#imported UserCreationForm built-in class to create new user accounts
from django.contrib.auth.forms import UserCreationForm
#import redirect function to redirect users to a different URL within the app
from django.shortcuts import redirect
#Custom UserCreationForm
from .forms import CustomUserCreationForm, CustomErrorList
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from cart.models import Order

#To log out & redirect users to home page
@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')

def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    #For GET requests, the function renders the accounts/login.html template
    if request.method == 'GET':
        return render(request, 'accounts/login.html',
            {'template_data': template_data})
    #For POST requests, the function attempts to authenticate the user
    #using the provided username and password
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] ='The username or password is incorrect.'
            return render(request, 'accounts/login.html',
                {'template_data': template_data})
        #If valid, re-directs to home page
        else:
            auth_login(request, user)
            return redirect('home.index')

def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    #If request is GET, then user is navigating to signup for via:
    #localhost:8000/accounts/signup url
    #Then send instance of UserCreationForm to the template
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        #render the accounts/signup.html
        return render(request, 'accounts/signup.html',
            {'template_data': template_data})
    #Post indicates that the form has been submitted
    elif request.method == 'POST':
        #initialises form with submitted data
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        #checks if form is valid (passwords match, not common password, etc)
        if form.is_valid():
            #saves user data to database (create new user account)
            form.save()
            #redirect users to the home page based on URL pattern
            return redirect('accounts.login')
        else:
            #if not valid, pass form to template
            #render accounts/signup.html template again
            template_data['form'] = form
            return render(request, 'accounts/signup.html',
                {'template_data': template_data})

@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html',
        {'template_data': template_data})

@login_required
def subscription_level(request):
    # Calculate total amount the user has spent
    total_spent = Order.objects.filter(user=request.user).aggregate(
        total=Sum('total')
    )['total'] or 0

    # Decide subscription level
    if total_spent < 15:
        level = "Basic"
    elif 15 <= total_spent < 30:
        level = "Medium"
    else:
        level = "Premium"

    return render(request, 'accounts/subscription.html', {
        'template_data': {
            'title': 'My Subscription',
            'total_spent': total_spent,
            'level': level,
        }
    })