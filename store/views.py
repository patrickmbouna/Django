from django.db import reset_queries
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.
#from django.http import HttpResponse
#from .models import ALBUMS
#from django.shortcuts import render
#from __future__ import absolute_import
from store.models import Album, Artist, Contact, Booking
#from django.template import loader
from .forms import ContactForm, ParagraphErrorList
from django.db import transaction, IntegrityError

@transaction.atomic


def index(request):
    albums = Album.objects.filter(available=True).order_by('-created_at')[:12]
    formatted_albums = ["<li>{}</li>".format(album.title) for album in albums]
    #message= """<ul>{}</ul>""".format("\n".join(formatted_albums))
    #template = loader.get_template('store/index.html')
    context={'albums': albums}
    return render( request, 'store/index.html', context)
    #return HttpResponse(message)

def listing(request):
    albums_list = Album.objects.filter(available=True)
    paginator = Paginator(albums_list, 4)
    page = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        albums = paginator.page(1)
    except EmptyPage:
        albums = paginator.page(paginator.num_pages)
#    formatted_albums = ["<li>{}</li>".format(album.title) for album in albums]
#    message= """<ul>{}</ul>""".format("\n".join(formatted_albums))
    context={
        'albums': albums,
        'paginate': True 
        }
    return render( request, 'store/listing.html', context)
#def detail(request, album_id):
def detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    artists_name = " ".join([artist.name for artist in album.artists.all()])
    context={
        'albums': album.title,
        'artists_name': artists_name,
        'album_id': album.id, 
        'thumbnail': album.picture
    }
#    artists = " ".join([artist['name'] for artist in album['artists']])
#    message = "Le nom de l'album est, {}. Il a été écrit par {}".format(album.title, artists)
    if request.method == 'POST':
        form = ContactForm(request.POST, error_class=ParagraphErrorList) 
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']

            try:
                with transaction.atomic():
                    contact = Contact.objects.filter(email=email)
            except IntegrityError:
                form.errors['internal'] = "Une erreur interne est apparue. Merci de recommencer votre requête."

            if not contact.exists():
                contact = Contact.objects.create(
                    email=email,
                    name=name
                )
            else:
                contact = contact.first()
            
            album = get_object_or_404(Album, id=album_id)
            booking = Booking.objects.create(
                contact=contact,
                album=album
            )
            album.available =False
            album.save()
            
            context = {
                'album_title': album.title
            }   
            return render(request, 'store/merci.html', context)
        else:
            context['errors'] = form.errors.items()
    else:
        form = ContactForm()

    context['form'] = form
    return render( request, 'store/detail.html', context)

def search(request):
    #obj=str(request.GET)
    query = request.GET.get('query')
    if not query:
        albums = Album.objects.all()
    else:
        albums = Album.objects.filter(title__icontains=query)
        if not albums.exists():
            albums = Artist.objects.filter(artists__name__icontains=query)
 # """      if not albums.exists():
 #           message = "Misère des misère nous n'avons trouvé aucun resultat"
 #       else:
 #           albums = ["<li>{}</li>".foramt(album.title) for album in albums]
 #           message = """ 
 #                   Nous avons trouver les albums correspondant à votre requette ! les voici:
  #                  <ul>
  #                  {}
  #                  </ul>
  #          """.format("<li></li>".join(albums)) """
    title = "Résultats pour la requête %s"%query
    context = {
        'albums': albums,
        'title': title
    }
       
    #message= "propriété GET :{} et requêtes".fora(obj, query)
    return render( request, 'store/search.html', context)

# Create your views here.