from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction, IntegrityError
#from django.http import HttpResponse

#from store.models import ALBUMS
from store.models import Album, Artist, Contact, Booking
from store.forms import ContactForm, ParagraphErrorList

#from django.template import loader


# l'objet request est une instance de la classe WSGIRequest (qui gère les réglage du serveur web)

# def index(request):
#     message = "Salut tout le monde !"
#     return HttpResponse(message)


# def index(request):
#     #albums = Album.objects.filter(available=True).order_by('-created_at')[:12]
#     albums = Album.objects.all()
#     formatted_albums = ["<li>{}</li>".format(album.title) for album in albums]
#     #message = """<ul>{}</ul>""".format("\n".join(formatted_albums))

#     template = loader.get_template('store/index.html')

#     return HttpResponse(template.render(request=request))

def index(request):
    albums = Album.objects.all()
    formatted_albums = ["<li>{}</li>".format(album.title) for album in albums]
    context = {'albums': albums}

    return render(request, 'store/index.html', context)


# def listing(request):
#     albums = Album.objects.filter(available=True)
#     formatted_albums = ["<li>{}</li>".format(album.title) for album in albums]
#     message = """<ul>{}</ul>""".format("\n".join(formatted_albums))
#    #albums = ["<li>{}</li>".format(album['name']) for album in ALBUMS]
#     #message = """<ul>{}</ul>""".format("\n".join(albums))
#     return HttpResponse(message)

def listing(request):
    album_list = Album.objects.filter(available=True)
    paginator = Paginator(album_list, 9)
    page = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        albums = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g 9999), deliver last page of results
        albums = paginator.page(paginator.num_pages)

    context = {
        'albums': albums,
        'paginate': True}

    return render(request, 'store/listing.html', context)


# def detail(request, album_id):
#     #id = int(album_id)
#     #album = ALBUMS[id]
#     #artists = "".join([artist["name"] for artist in album["artists"]])
#     album = Album.objects.get(pk=album_id)
#     artists = " ".join([artist.name for artist in album.artists.all()])

#     #message = "Le nom de l'album est {}. Il a été écrit par {}".format(album['name'], artists)
#     message = "Le nom de l'album est {}. Il a été écrit par {}".format(
#         album.title, artists)

#     return HttpResponse(message)


# def detail(request, album_id):
#     #album = Album.objects.get(pk=album_id)
#     album = get_object_or_404(Album, pk=album_id)
#     artists = " ".join([artist.name for artist in album.artists.all()])
#     artists_name = " ".join(artists)
#     if request.method == "POST":
#         email = request.POST.get('email')
#         name = request.POST.get('name')

#         contact = Contact.objects.filter(email=email)
#         if not contact.exists():
#             contact = Contact.objects.create(
#                 email=email,
#                 name=name
#             )
#         album = get_object_or_404(Album, pk=album_id)
#         booking = Booking.objects.create(
#             contact=contact,
#             album=album
#         )

#         album.available = False
#         album.save()
#         context = {
#             'album_title': album.title
#         }
#         return render(request, 'store/merci.html', context)

#     context = {
#         'album_title': album.title,
#         'artists_name': artists_name,
#         'album_id': album.id,
#         'thumbnail': album.picture
#     }
#     return render(request, 'store/detail.html', context)


# @transaction.atomic
def detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    artists = [artist.name for artist in album.artists.all()]
    artists_name = " ".join(artists)
    context = {
        'album_title': album.title,
        'artists_name': artists_name,
        'album_id': album.id,
        'thumbnail': album.picture
    }
    if request.method == 'POST':
        form = ContactForm(request.POST, error_class=ParagraphErrorList)
        # If the form is correct, We can proceed to booking.
        # form is correct, We can proceed to booking.
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']

            try:
                with transaction.atomic():
                    contact = Contact.objects.filter(email=email)
                    if not contact.exists():
                        # If a contact is not registered, create a new one.
                        contact = Contact.objects.create(
                            email=email,
                            name=name
                        )
                    else:
                        contact = contact.first()
                    # If no album matches the id, it means the form must have been tweaked
                    # so returning a 404 is the best solution.
                    album = get_object_or_404(Album, id=album_id)
                    booking = Booking.objects.create(
                        contact=contact,
                        album=album
                    )

                    # Make sure no one can book the album again.
                    album.available = False
                    album.save()
                    context = {
                        'album_title': album.title
                    }
                    return render(request, 'store/merci.html', context)
            except IntegrityError:
                # If an IntegrityError is raised, it means the album has been booked
                # by another user in the meantime.
                # In this case, we just return the 404 page.
                form.errors['erros'] = "Une erreur interne est survenue. Merci de recommencer la requête."
                #raise Http404
    else:
        form = ContactForm()

    context['form'] = form
    # Form data doesn't match the expected format, Add errors to the template.
    context['errors'] = form.errors.items()
    return render(request, 'store/detail.html', context)


"""
Propriétés WSGIRequest :
-  GET : qui renvoie un dictionnaire contenant tous les arguments passés à l'url
"""
# def search(request):
#     obj = str(request.GET)
#     query = request.GET['query']
#     message = "propriété GET : {} et requête : {}".format(obj, query)

#     return HttpResponse(message)


# def search(request):
#     query = request.GET.get('query')
#     if not query:
#         message = "Aucun artiste n'est demandé"
#     else:
#         albums = [
#             album for album in ALBUMS
#             if query in " ".join(artist['name'] for artist in album['artists'])
#         ]

#         if len(albums) == 0:
#             message = "Misère de misère, nous n'avons trouvé aucun résultat !"
#         else:
#             albums = ["<li>{}</li>".format(album['name']) for album in albums]
#             message = """
#                 Nous avons trouvé les albums correspondant à votre requête ! Les voici :
#                 <ul>
#                     {}
#                 </ul>
#             """.format("</li><li>".join(albums))
#     return HttpResponse(message)


def search(request):
    query = request.GET.get('query')
    # hellofest
    if not query:
        albums = Album.objects.all()
    else:
        # title contains the query and query is not sensitive to case.
        albums = Album.objects.filter(title__icontains=query)

        if not albums.exists():
            albums = Album.objects.filter(artists__name__icontains=query)

    title = "Résultats pour la requête %s" % query
    context = {
        'albums': albums,
        'title': title,
    }

    return render(request, 'store/search.html', context)
