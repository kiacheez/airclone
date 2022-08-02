from django.db import models
from django_countries.fields import CountryField
from django.urls import reverse
from django.utils import timezone
from core import models as core_models
from users import models as user_models
from cal import Calendar


class AbstractItem(core_models.TimeStampedModel):
    name = models.CharField(max_length=80)

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.name


class RoomType(AbstractItem):
    
    class Meta:
        verbose_name = "Room Type"
        ordering = ["created"]

class Amenity(AbstractItem):
    
    class Meta:
        verbose_name_plural = "Amenities"

class Facility(AbstractItem):
    
    class Meta:
        verbose_name_plural = "Facilities"

class HouseRule(AbstractItem):
    
    class Meta:
        verbose_name = "House Rule"


class Photo(core_models.TimeStampedModel):

    caption = models.CharField(max_length = 100)
    file = models.ImageField(upload_to = "room_photos")
    room = models.ForeignKey("Room", related_name = "photos", on_delete = models.CASCADE)

    def __str__(self):
        return self.caption


class Room(core_models.TimeStampedModel):

    name = models.CharField(max_length=140)
    description = models.TextField()
    country = CountryField()
    city = models.CharField(max_length=50)
    price = models.IntegerField()
    address = models.CharField(max_length= 140)
    beds = models.IntegerField()
    bedrooms = models.IntegerField()
    baths = models.IntegerField()
    guests = models.IntegerField()
    check_in = models.TimeField()
    check_out = models.TimeField()
    instant_book = models.BooleanField(default=False)
    host = models.ForeignKey("users.User", related_name = "rooms", on_delete = models.CASCADE)
    room_type = models.ForeignKey("RoomType", related_name = "rooms",on_delete = models.SET_NULL, null = True)
    amenities = models.ManyToManyField("Amenity", related_name = "rooms", blank = True)
    facilities = models.ManyToManyField("Facility", related_name = "rooms", blank = True)
    house_rules = models.ManyToManyField("HouseRule", related_name = "rooms", blank = True )



    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        
        self.city = str.capitalize(self.city)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("rooms:detail", kwargs={'pk': self.pk})

    def total_rating(self):
        
        all_reviews = self.reviews.all() 
        """review 모델에 room = models.ForeignKey("rooms.Room", related_name = "reviews", on_delete = models.CASCADE)이 있기에 호출가능"""

        all_ratings = 0
        
        if len(all_reviews) > 0:
            for review in all_reviews:
                all_ratings += review.rating_average()
            return all_ratings / len(all_reviews)

        return 0
    
    def first_photo(self):
        try:  
            photo, = self.photos.all()[:1]
            return photo.file.url

        except ValueError:
            return None

    def get_next_four_photos(self):
        photos = self.photos.all()[1:5]

        print(photos)
        return photos

    def get_calendars(self):

        now = timezone.now()  
        this_year = now.year
        this_month = now.month
        next_month = this_month + 1

        if this_month == 12:
            next_month == 1
        this_month_cal = Calendar(this_year, this_month)
        next_month_cal = Calendar(this_year, next_month)
        return [this_month_cal, next_month_cal]