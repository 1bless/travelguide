from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
from django.core.validators import MaxValueValidator, MinValueValidator

class CustomUser(AbstractUser):
    bio = models.TextField(_("Biography"), blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    interests = models.ManyToManyField('Interest', related_name='interested_users', blank=True)
    location = models.CharField(_("Location"), max_length=100, blank=True)
    
    def update_statistics(self):
        self.total_reviews = self.reviews.count()
        self.save()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # custom save behavior, processing the profile picture
        super().save(*args, **kwargs)

    def update_statistics(self):
        # Custom method to update user statistics
        pass


class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Itinerary(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='itineraries')
    title = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    notes = models.TextField(null=True, blank=True)
    places_to_visit = models.ManyToManyField('Place', related_name='itineraries', blank=True)

    def __str__(self):
        return self.title

    def duration(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days + 1
        return 0


class Place(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='place_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user.username} on {self.itinerary.title}'


@receiver(post_save, sender=Review)
def update_user_statistics_on_review_save(sender, instance, created, **kwargs):
    if created:
        instance.user.update_statistics()

@receiver(post_delete, sender=Review)
def update_user_statistics_on_review_delete(sender, instance, **kwargs):
    instance.user.update_statistics()
