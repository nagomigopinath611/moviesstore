from django.contrib import admin
#Movie & Review are both Django models
from .models import Movie, Review

#MovieAdmin class that inherits from admin.ModelAdmin
#Allows you to customise behaviour of admin interface for the Movie model
class MovieAdmin(admin.ModelAdmin):
    #Sets default ordering system by name
    ordering = ['name']
    #Allows searching by name
    search_fields = ['name']

#Register Movie model to the admin panel.
#Customises admin interface for Movie model
admin.site.register(Movie, MovieAdmin)
#Regitser the new model to the admin site
admin.site.register(Review)
