from django.db import models

# Create your models here.

# ARTISTS = {
#   'francis-cabrel': {'name': 'Francis Cabrel'},
#   'lej': {'name': 'Elijay'},
#   'rosana': {'name': 'Rosana'},
#   'maria-dolores-pradera': {'name': 'María Dolores Pradera'},
# }


# ALBUMS = [
#   {'name': 'Sarbacane',
#   'artists': [ARTISTS['francis-cabrel']]
#   },
#   {'name': 'La Dalle',
#    'artists': [ARTISTS['lej']]
#    },
#   {'name': 'Luna Nueva',
#   'artists': [ARTISTS['rosana'],
#               ARTISTS['maria-dolores-pradera']]}
# ]

class Artist(models.Model):
    name = models.CharField('Nom' , max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Artiste'
        ordering = ['name']


class Contact(models.Model):
    email = models.EmailField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Album(models.Model):
    reference = models.IntegerField(null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)
    title = models.CharField(max_length=200)
    picture = models.URLField()

    #artists = models.ManyToMany(Artist, related_name='albums', blank=True)
    artists = models.ManyToManyField(Artist, related_name='albums', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Album'
        ordering = ['title']


class Booking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    contacted = models.BooleanField(default=False)

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    album = models.OneToOneField(Album, on_delete=models.CASCADE)

    def __str__(self):
        return self.contact.name

    class Meta:
        verbose_name = 'Réservation'
        ordering = ['created_at']
