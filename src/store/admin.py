from django.contrib import admin
from store.models import Artist, Contact, Album, Booking
# Register your models here.




# admin.site.register(Artist, admin.ModelAdmin)
# admin.site.register(Album, admin.ModelAdmin)


# admin.site.register(Booking)

class BookingInline(admin.TabularInline):
    model = Booking
    fieldsets = [
        (None, {'fields': ['album',  'contacted']})
        ] # list columns
    extra = 0 # number of empty rows to display
    verbose_name = 'Réservation'
    verbose_name_plural = 'Réservations'


class ContactAdmin(admin.ModelAdmin):
    inlines = [BookingInline, ]
    # list_display = ('name', 'email')
    # list_filter = ('name', 'email')
    # search_fields = ('name', 'email')
admin.site.register(Contact, ContactAdmin)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('contact', 'album', 'contacted')
    list_filter = ('created_at', 'contacted', 'album__title')
    search_fields = ('contact__name', 'album__title')
    #extra = 0 # number of empty rows to display
admin.site.register(Booking, BookingAdmin)



class AlbumArtistInline(admin.TabularInline):
    model = Album.artists.through # the query goes through an intermediate table.
    extra = 1
    verbose_name = 'Disque'
    verbose_name_plural = 'Disques'


class ArtistAdmin(admin.ModelAdmin):
    inlines = [AlbumArtistInline, ]
    list_display = ('name', 'albums_count')
    list_filter = ('name', )
    search_fields = ('name', )

    def albums_count(self, obj):
        return obj.albums.count()
admin.site.register(Artist, ArtistAdmin)


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'reference', 'available')
    list_filter = ('available', 'title', 'reference')
    search_fields = ('title', 'reference')
admin.site.register(Album, AlbumAdmin)
