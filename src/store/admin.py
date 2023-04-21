from django.contrib import admin
from store.models import Artist, Contact, Album, Booking
# from django.core.urlrsolvers import reverse
# from django.utils.safestring import mark_safe
# from django.contrib.contenttypes.models import ContentType
# Register your models here.

# admin.site.register(Artist, admin.ModelAdmin)
# admin.site.register(Album, admin.ModelAdmin)


# admin.site.register(Booking)

# admin: {{ nom_application }}_{{ nom_modèle }}_change
# admin:store_booking_change

# class AdminURLMixin(object):
#     def get_admin_url(self, obj):
#         content_type = ContentType.objects.get_for_model(obj.__class__)
#         #return reverse('admin:store_%s_change'. % (content_type.model), args=(obj.id,)
#         return reverse('admin:store_{}_change'.format(
#             self.model._meta.model_name
#         ), args=(obj.id,))


class BookingInline(admin.TabularInline):
    model = Booking
    readonly_fields = ['created_at', 'contacted', 'album']
    fieldsets = [
        (None, {'fields': ['album',  'contacted']})
        ] # list columns
    extra = 0 # number of empty rows to display
    verbose_name = 'Réservation'
    verbose_name_plural = 'Réservations'
    # permet de ne pas afficher le bouton "Ajouter" dans la page d'admin (pour éviter de créer une réservation sans passer par un contact)
    def has_add_permission(self, *args, **kwargs):
        return False
    


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
    # fieldsets = [
    #     (None, {'fields': ['album',  'contact', 'contacted']})
    #     ] 
    readonly_fields = ['created_at', 'contact', 'album', 'contacted']

    # permet de ne pas afficher le bouton "Ajouter" dans la page d'admin
    def has_add_permission(self, request):
        return False

    # def album_link(self, obj):
    #     url = reverse("admin:store_album_change", args=[obj.album.id])
    #     html = format_html('<a href="{}">{}</a>', url, obj.album.title)
    #     return html

    # from django.urls.safestring import mark_safe
    # def album_link(self, booking):
    #     #url = "/content"
    #     #path = "admin:store_album_change"
    #     #url = reverse(path, args=(booking.album.id, ))
    #     url = self.get_admin_url(booking.album)
    #     html = '<a href="{}">{}</a>'.format(url, booking.album.title)
    #     return mark_safe(html)

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
