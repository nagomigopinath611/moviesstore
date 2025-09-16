from django.urls import path
from . import views
urlpatterns = [
    path('signup', views.signup, name='accounts.signup'),
    path('login/', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    #Add view orders function in accounts because:
    #order is linked to a user's account
    path('orders/', views.orders, name='accounts.orders'),
    path('subscription/', views.subscription_level, name='accounts.subscription'),
]

