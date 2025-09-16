from django.db import models
#Import user model
from django.contrib.auth.models import User

#The Python class Movie inherits from models.Model
class Movie(models.Model):
    #AutoField value automatically increments its value for every new record
    #primary_key = True means this field is the primary key for the table
    id = models.AutoField(primary_key=True)
    #Max length of 255 characters
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    #upload_to specifies directory where photos will be uploaded
    image = models.ImageField(upload_to='movie_images/')
    #__str__ returns string representation of object
    def __str__(self):
        return str(self.id) + ' - ' + self.name
    
#Python class Review that inherits from models.Model
class Review(models.Model):
    #autofield that automatically increments for each database record
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    #date & time data
    date = models.DateTimeField(auto_now_add=True)
    #foreign key relationship to Movie model
    #CASCADE means that if movie deleted, associated review deleted
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    #foreign key relationship to User model
    #CASCADE, if user deleted, associated review deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #Returns string representation of review
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name
