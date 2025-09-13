#get_object_or_404 raises a 404 error if object not found
from django.shortcuts import render, redirect, get_object_or_404
#import movie model from the models file
#Use this model to access database information
#Review model to make reviews
from .models import Movie, Review, ReviewUpvote
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

#Variable called movies is a list of dictionaries where each dictionary
#represents information about a certain movie
def index(request):
    #will retrieve all movies if search parameter if not in the current request
    #or will retrieve specific movies based on search parameter
    search_term = request.GET.get('search')
    #if search_term is not null, we filter for movies
    if search_term:
        #icontains used for case-insensitive search
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    #Pass extracted movies to template_data dictionary
    template_data['movies'] = movies
    return render(request, 'movies/index.html',
                  {'template_data': template_data})

#id is collected from the url
def show(request, id):
#extract movie object based on the id
#id is passed on by the url and received as a parameter for show function
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html',
                  {'template_data': template_data})

@login_required
#Method to create review
#request contains info about HTTP request
#id is ID of movie being reviewed
def create_review(request, id):
    #checks that POST's data is not empty
    if request.method == 'POST' and request.POST['comment']!= '':
        #retrieve movie using id
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        #redirect function to redirect user to different URL
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
    
@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
    
@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)  

def upvote_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    try:
        # Try to create a new upvote record
        ReviewUpvote.objects.create(review=review, user=request.user)
        review.upvotes += 1
        review.save()
    except IntegrityError:
        # This means the (review, user) pair already exists — ignore
        pass

    # Redirect back to the movie detail page
    return redirect('movie_detail', id=review.movie.id)

def movie_detail(request, id):
    movie = get_object_or_404(Movie, id=id)
    reviews = Review.objects.filter(movie=movie).order_by('-upvotes', '-date')

    print("=== Reviews being sent to template ===")
    for r in reviews:
        print(r.comment, r.upvotes)
        
    return render(request, 'movie_detail.html', {
        'template_data': {
            'movie': movie,
            'reviews': reviews,
        }
    })
