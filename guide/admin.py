from django.contrib import admin
from .models import CustomUser, Itinerary, Review, Place, Interest

admin.site.register(CustomUser)
admin.site.register(Itinerary)
admin.site.register(Review)
admin.site.register(Place)
admin.site.register(Interest)