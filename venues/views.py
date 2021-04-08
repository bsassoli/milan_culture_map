from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import TemplateView

import json
import folium
import numpy as np
from folium.plugins import LocateControl, MarkerCluster, FeatureGroupSubGroup, Fullscreen, Search, BeautifyIcon
from folium.map import Layer, FeatureGroup, LayerControl, Marker

from .models import Venue, Category, User, VManager, News, Map, Event
from .forms import VenueForm

# Create your views here.


def paginate(items, number):
    objects = [item for item in items]
    paginator = Paginator(objects, number)
    return paginator


def index(request):
    mymap = get_object_or_404(Map).html
    context = {'mymap': mymap}
    return render(request, 'venues/index.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff)
# Admin users or staff users can update/create maps
def map(request):
    icons = {
        'Museo': {
            'icon': 'university',
            'prefix': 'fa',
            'color': 'cadetblue'
        },

        'Biblioteca': {
            'icon': 'building',
            'prefix': 'fa',
            'color': 'darkred'
        },
        'Spazio Espositivo': {
            'icon': 'picture-o',
            'prefix': 'fa',
            'color': 'orange'
        },
        'Spazio ibrido ':
        {
            'icon': 'star',
            'prefix': 'fa',
            'color': 'blue'
        },
        'Centro culturale':
        {
            'icon': 'sign-in',
            'prefix': 'fa',
            'color': 'red'
        },
        'Teatro':
        {
            'icon': 'eye',
            'prefix': 'fa',
            'color': 'black'
        },
        'Spazio ibrido':  {
            'icon': 'lightbulb-o',
            'prefix': 'fa',
            'color': 'lightgray'
        },
        'Live club':  {
            'icon': 'music',
            'prefix': 'fa',
            'color': 'purple'
        },
        'Archivio':
        {
            'icon': 'archive',
            'prefix': 'fa',
            'color': 'beige'
        },
        'Istituto di cultura':
        {
            'icon': 'globe',
            'prefix': 'fa',
            'color': 'lightred'
        },
        'Galleria':
        {
            'icon': 'paint-brush',
            'prefix': 'fa',
            'color': 'darkgreen'
        },
        'Libreria':  {
            'icon': 'book',
            'prefix': 'fa',
            'color': 'lightblue'
        },
        'Cinema':  {
            'icon': 'video-camera',
            'prefix': 'fa',
            'color': 'darkpurple'

        }}
    # Creating Map object
    milan_center = [45.46429322174771, 9.191872853615125]
    
    m = folium.Map(location=milan_center, tiles='cartodbpositron',
                   zoom_start=12, control_scale=True, height='90%',
                   )
    # Overriding default CSS which will interfere with navbar
    m.default_css = [('leaflet_css', 'https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.css'),
                                   ('awesome_markers_font_css',
                                    'https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css'),
                                   ('awesome_markers_css', 'https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css'),
                                   ('awesome_rotate_css', 'https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css')]
    # Add fullscreen button
    Fullscreen(
                title='Fullscreen',
                title_cancel='Exit fullscreen',
                force_separate_button=True
                ).add_to(m)
    
    # Create Folium cluster
    cluster = MarkerCluster(name="Tutte le venues", options={
                                'showCoverageOnHover': False,
                                'zoomToBoundsOnClick': True,
                                'spiderfyOnMaxZoom': False,
                                'disableClusteringAtZoom': 17}, control=False)
    # Add cluster to map
    m.add_child(cluster)

    # Add categories
    layers = {}
    for category in Category.objects.all():
        layers[category.name] = FeatureGroupSubGroup(
            group=cluster,
            name=category.name
            )
        m.add_child(layers[category.name])

    # Enable geolocation button on map.
    LocateControl(auto_start=False, fly=True).add_to(m)
    
    # memoize locations for avoiding overlapping markers later
    locations = []
    
    # Add html and create markers
    for venue in Venue.objects.all():
        name = venue.name
        address = venue.address
        subgroup_category = venue.category.name
        location = [venue.latitude, venue.longitude]
        
        # check for location overlaps and if so perturb it minimally
        if location in locations:
            location[0] += np.random.uniform(0.0005, 10**(-20))-0.0000007
        locations.append(location)
        
        page = f'venue/{name}'
        image = venue.image.url
        url = venue.url
        html = folium.Html(
            f"""
        <div class="card card-profile card-plain">
            <div class="card-header card-avatar">
                <img class="img" src="{image}">
            </div>
            <div class="card-body ">
                <h4 class="card-title">
                  <a href="{page}">{name}</a>            
                </h4>
                <h6 class="card-category text-muted">
                  <i>Categoria: </i>{subgroup_category}
                </h6>
                    <p><a href='{url}' target='_blank'>Sito</a></p>
            </div>
            <div class="card-footer justify-content-center">
                {address}
            </div>
        </div>
    """, script=True)
        category = icons[subgroup_category]
        try:
            category = icons[subgroup_category]
            venue_marker = folium.Marker(
                location=location,
                tooltip=name,
                popup=folium.Popup(html=html, max_width=600),
                icon=folium.Icon(
                    color=category['color'],
                    icon=category['icon'],
                    prefix=category['prefix']
                    ),
                )
            layers[subgroup_category].add_child(venue_marker)
        except Exception:
            print('Problem')

    # Add Layer Control to map
    folium.LayerControl().add_to(m)
    """
    search = Search(layer=feature_collection,
                    search_label='name',
                    position='bottomleft',
                    )
    search.add_to(m)
    """
    # Map model currently unused 
    mymap = m._repr_html_()

    old_css = '<link rel = "stylesheet" href = "https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css"/> <link rel = "stylesheet" href = "https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css"/>'
    mymap = mymap.replace(old_css, '')
    mymap = mymap.replace('height: 100', 'height: 90')

    context = {'mymap': mymap}

    Map.objects.update_or_create(defaults={'html': mymap})
    
    # Save map for rendering as include 
    m.save('venues/templates/venues/map.html')

    return render(request, 'venues/index.html', context)


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "venues/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "venues/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("venues/index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "venues/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

        except IntegrityError:
            return render(request, "venues/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "venues/register.html")


# Venue managers will require to be flagged as active by admin
# They will have access to venue editing for their venues
def registermanager(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        venue = Venue.objects.get(name=request.POST["venue"])
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "venues/registermanager.html", {
                'venues': Venue.objects.all(),
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            manager = VManager(user=user)
            user.is_vmanager = True
            user.is_active = False
            user.save()
            manager.save()
            manager.venue.add(venue)
        except IntegrityError:
            return render(request, "venues/registermanager.html", {
                "message": "Username already taken.",
                'venues': Venue.objects.all()
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "venues/registermanager.html", {
            'venues': Venue.objects.all()
        })


def venue(request, venue):
    form = VenueForm()
    venue = get_object_or_404(Venue, name=venue)
    news = venue.news.all().order_by('-date')
    context = {'venue': venue,
               'form': form,
               'news': news,
               }
    return render(request, 'venues/venue.html', context)


@login_required
def edit(request):
    if request.method == "POST":
        data = json.loads(request.body)
        venue = get_object_or_404(Venue, id=data['id'])
        venue.description = data['description']
        venue.url = data['url']
        venue.address = data['address']
        venue.save()
        return JsonResponse(data, status=201)


def about(request):
    return render(request, 'venues/about.html')


@login_required
def favorites(request):
    try:
        venues = request.user.favorites.all()
    except Exception:
        venues = []
    paginator = paginate(venues, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'venues/favorites.html', {
        'venues': page
        })


def news(request):
    news = News.objects.all().order_by('-date')
    return render(request, 'venues/news.html', {'news': news})


def events(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'venues/events.html', {'events': events})


@login_required
def follow(request):
    if request.method == "POST":
        data = json.loads(request.body)
        venue = Venue.objects.get(id=data['venue'])
        if data['action'] == "follow":
            request.user.favorites.add(venue.id)
        else:
            request.user.favorites.remove(venue.id)
        return JsonResponse(data, status=200)
