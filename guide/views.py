from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm, ItineraryForm, ReviewForm
from .models import CustomUser, Itinerary, Review
from django.contrib.auth.decorators import login_required

# User Registration View
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard_view')
    else:
        form = CustomUserCreationForm()
    return render(request, 'guide/register.html', {'form': form})

# User Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard_view')
    else:
        form = AuthenticationForm()
    return render(request, 'guide/login.html', {'form': form})

# User Logout View
def logout_view(request):
    logout(request)
    return redirect('login_view')

# User Dashboard View
@login_required
def dashboard_view(request):
    user_itineraries = Itinerary.objects.filter(user=request.user)
    return render(request, 'guide/dashboard.html', {'itineraries': user_itineraries})

# Itinerary Creation View
@login_required
def itinerary_create_view(request):
    if request.method == 'POST':
        form = ItineraryForm(request.POST)
        if form.is_valid():
            itinerary = form.save(commit=False)
            itinerary.user = request.user
            itinerary.save()
            form.save_m2m()  # For saving many-to-many relationships
            return redirect('dashboard_view')
    else:
        form = ItineraryForm()
    return render(request, 'guide/itinerary_form.html', {'form': form})

# Itinerary Detail View
@login_required
def itinerary_detail_view(request, pk):
    itinerary = get_object_or_404(Itinerary, pk=pk, user=request.user)
    return render(request, 'guide/itinerary_detail.html', {'itinerary': itinerary})

# Review Submission View
@login_required
def review_submit_view(request, itinerary_pk):
    itinerary = get_object_or_404(Itinerary, pk=itinerary_pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.itinerary = itinerary
            review.save()
            return redirect('itinerary_detail_view', pk=itinerary_pk)
    else:
        form = ReviewForm()
    return render(request, 'guide/review_form.html', {'form': form, 'itinerary': itinerary})