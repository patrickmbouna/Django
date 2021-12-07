from django.contrib import admin
#from django.contrib import admin

#admin.site.enable_nav_sidebar = False
from django.db import models
from django.utils.safestring import mark_safe
#from django.core.urlresolvers import reverse
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
# Register your models here.
from .models import Artist, Booking, Contact, Album


#admin.site.register(Booking)
#admin.site.register(models, admin_class=Booking)

class AdminURLMixin(object):
    def get_admin_url(self, obj):
        content_type= ContentType.objects.get_for_model(obj.__class__)
        return reverse("admin:store_%_change"%(content_type.model), args=(obj.id,))

class BookingInline(admin.TabularInline, AdminURLMixin):
    readonly_fields = ["created_at", "contacted", "album_link"]
    model = Booking
    fieldsets = [
        (None, {'fields': ['album_link', 'contacted']})
    ]# list coulumns
#    list_filter= ['create_at', 'contacted']
    extra = 0
    verbose_name = "Réservation"
    verbose_name_plural = "Réservations"

    def album_link(self, booking):
        #path ="admin:store_booking_change"
        url = self.get_admin_url(booking.album)
        #reverse(path, args=(booking.album.id,))
        return mark_safe("<a href='{}'>{}</a>".format(url, booking.album.title))

class AlbumArtistInline(admin.TabularInline):
    model = Album.artists.through
    extra = 1
    verbose_name = "Disque"
    verbose_name_plural = "Disques"

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    inlines = [BookingInline, ]

@admin.register(Artist)
class ContactAdmin(admin.ModelAdmin):
    inlines = [AlbumArtistInline, ]

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    search_fields= ['reference', 'title']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin, AdminURLMixin):
    readonly_fields = ["created_at", "contact", "album_link"]
    fields = ['created_at','album_link', 'contacted']
    list_filter= ['created_at', 'contacted']
    
    def has_add_permission(self, request) -> bool:
        return False

    def album_link(self, booking):
        #path ="admin:store_booking_change"
        url = self.get_admin_url(booking.album)
        #reverse(path, args=(booking.album.id,))
        return mark_safe("<a href='{}'>{}</a>".format(url, booking.album.title))