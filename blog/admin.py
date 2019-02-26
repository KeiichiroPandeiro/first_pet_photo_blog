from django.contrib import admin
from .models import Photo, Good, Pet

# Register your models here.
class GoodInline(admin.TabularInline):
    model = Good
    fk_name = 'photo'


class PhotoInline(admin.TabularInline):
    model = Photo
    fk_name = 'pet'


class PhotoAdmin(admin.ModelAdmin):

    list_display = ('id','good_count' ,'image', 'is_primary','is_dispalyed')

    inlines = [
        GoodInline,
    ]

class PetAdmin(admin.ModelAdmin):

    list_display = ('id','name','pet_type','together_with','sex','owner',)

    inlines = [
        PhotoInline,
    ]


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Pet, PetAdmin)
