from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages

@login_required # login decorator
def place_list(request):

    if request.method == 'POST':
        # create new place
        form = NewPlaceForm(request.POST) # creating form from data in the request
        place = form.save(commit=False) # Create a new Place from the form
        place.user = request.user # this saves and redirect
        if form.is_valid(): # validate against DB constraints
            place.save() # saves to db
            return redirect('place_list') # reload home page

    # Creating the place object and filtering by name
    # if not a POST, or the form is not valid, render the page
    # with the form to add a new place, and list of places
    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm() # used to create HTML
    # Render dictionary data into html
    return render(request, 'travel_wishlist/wishlist.html', { 'places': places, 'new_place_form': new_place_form })


@login_required
def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited })


@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user: # ensure user is same as the user making the request
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden() # else return http forbidden
    return redirect('place_list')


@login_required
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    
    # first thing is fetching the place form db associated with pk.
    # Does this place belong to the current user?
    if place.user != request.user:
        return HttpResponseForbidden()

    # is this a GET (show data + form) request, or POST (update place object) request?

    # if POST request, validate form data and update
    if request.method == 'POST': 
        # make new trip review form object from data sent w/http request.
        # then put user entered data as model instance from db.
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        # check if form is valid.
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors) # temporary, refine later

        return redirect('place_details', place_pk=place_pk) # redirect as a GET request

    else:
    # if GET request, show place info and optional form
    # if place is visited, show form; if place is not visited, no form.
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form} )

        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place} )


@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list') # redirect means make another request to the route with a name 'place_list'
    else:
        return HttpResponseForbidden() 


def about(request):
    author = 'Mynue'
    about = 'A website to create a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})
