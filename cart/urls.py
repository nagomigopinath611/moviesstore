from django.urls import path
from . import views

urlpatterns = [
    #To create a sort of home page for cart
    path('', views.index, name='cart.index'),
    path('<int:id>/', views.add, name='cart.add'),
    #No int because we do not need a movie id, etc to do this
    path('clear/', views.clear, name='cart.clear'),
    path('purchase/', views.purchase, name='cart.purchase'),
]