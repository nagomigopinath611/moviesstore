from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'movies.index'),
    #<int:id> means that an int associated with variable id is expected
    path('<int:id>/', views.show, name='movies.show'),
    path('<int:id>/review/create/', views.create_review, name='movies.create_review'),
    #captures 2 int values (review id & movie id, then passes
    #to edit_review function as arguments)
    path('<int:id>/review/<int:review_id>/edit/', views.edit_review, name='movies.edit_review'),
    path('<int:id>/review/<int:review_id>/delete/', views.delete_review, name='movies.delete_review'),
]