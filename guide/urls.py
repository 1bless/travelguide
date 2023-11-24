from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # User dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Itinerary management
    path('itinerary/create/', views.itinerary_create_view, name='itinerary_create'),
    path('itinerary/<int:pk>/', views.itinerary_detail_view, name='itinerary_detail'),

    # Review submission
    path('itinerary/<int:itinerary_pk>/review/', views.review_submit_view, name='review_submit'),

    # User profile
    #path('profile/', views.profile_view, name='profile'),
    
    # ... include other URL patterns as needed ...
]
