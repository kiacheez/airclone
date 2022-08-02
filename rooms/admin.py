from django.contrib import admin
from django.utils.html import mark_safe
from .import models

@admin.register(models.RoomType, models.Amenity, models.Facility, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):
    
    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()

class PhotoInline(admin.TabularInline):

    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):

    """Room Admin Definition"""

    inlines = (PhotoInline,)


    fieldsets = (
        (
            "Basic Info", {
                "fields" : ("name", "description", "country", "city", "address", "price")
            }
        ),

        (
            "Times", {
                "fields" : ("check_in", "check_out", "instant_book")
            }
        ),

        (
            "Spaces", {
                "fields" : ("guests", "beds", "bedrooms", "baths")
            }
        ),

        (
            "More about the Space", {
                "fields" : ("amenities", "facilities", "house_rules")
            }
        ),

        (
            "Last details", {
                "fields" : ("host",)
            }
        ),
    )

    
    list_display = (
        "name",
        "country",
        "city",
        "price",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )

    raw_id_fields = ("host", )

    list_filter = ("city", "instant_book", "room_type", "amenities", "facilities", "house_rules",)

    search_fields = ("=city", "^host__username")

    filter_horizontal = ("amenities", "facilities", "house_rules",)

    def count_amenities(self, obj):
        
        return obj.amenities.count()

    """function이라 어드민상 클릭은 불가"""


    count_amenities.short_description = "hello amenitiy fart!"

    def count_photos(self, obj):
        return obj.photos.count() 
    
    count_photos.short_description = "Photo count"

    
@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    
    """Photo Admin Definition"""

    list_display = (
        "__str__",
        "get_thumbnail",
    )

    def get_thumbnail(self, obj):
        
        return mark_safe(f'<img width = "60px" src="{obj.file.url}" />')

    get_thumbnail.short_description = "Thumbnail"