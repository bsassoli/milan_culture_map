from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView
from django.utils.safestring import mark_safe

import json
import calendar

from .models import Venue, User, VManager, News, Map, Event
from .forms import VenueForm, NewsForm, EventForm
from .utils import Calendar, make_map, find_coordinates
from datetime import datetime, timedelta


# Create your views here.


def paginate(items, number):
    objects = [item for item in items]
    paginator = Paginator(objects, number)
    return paginator


def index(request):
    mymap = get_object_or_404(Map).html
    context = {"mymap": mymap}
    return render(request, "venues/index.html", context)


@login_required
@user_passes_test(lambda u: u.is_staff)
# Admin users or staff users can update/create maps
def map(request):

    m = make_map()

    # Map model currently unused
    mymap = m._repr_html_()

    context = {"mymap": mymap}

    Map.objects.update_or_create(defaults={"html": mymap})

    # Save map for rendering as include
    m.save("venues/templates/venues/map.html")

    return render(request, "venues/index.html", context)


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
            return render(
                request,
                "venues/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "venues/register.html", {
                    "message": "Passwords must match."
                    }
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

        except IntegrityError:
            return render(
                request, "venues/register.html", {
                    "message": "Username already taken."
                    }
            )
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
            return render(
                request,
                "venues/registermanager.html", {
                    "venues": Venue.objects.all(),
                    "message": "Passwords must match."
                },
            )

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
            return render(
                request,
                "venues/registermanager.html", {
                    "message": "Username already taken.",
                    "venues": Venue.objects.all()
                    },
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(
            request,
            "venues/registermanager.html", {
                "venues": Venue.objects.all()
                }
        )


def venue(request, venue):
    form = VenueForm()
    venue = get_object_or_404(Venue, name=venue)
    news = venue.news.all().order_by("-date")
    context = {
        "venue": venue,
        "form": form,
        "news": news,
    }
    return render(request, "venues/venue.html", context)


@login_required
def edit(request):
    if request.method == "POST":
        data = json.loads(request.body)
        venue = get_object_or_404(Venue, id=data["id"])
        venue.description = data["description"]
        venue.url = data["url"]
        if data["address"] != venue.address:
            new_coordinates = find_coordinates(data['address'])
            if new_coordinates == "Not found":
                return JsonResponse(data, status=404)       
        venue.latitude, venue.longitude = new_coordinates[0], new_coordinates[1]
        venue.address = data["address"]
        print(venue)
        venue.save()
        m = make_map()
        m.save("venues/templates/venues/map.html")
        return JsonResponse(data, status=201)


def about(request):
    return render(request, "venues/about.html")


@login_required
def favorites(request):
    try:
        venues = request.user.favorites.all()
    except Exception:
        venues = []
    paginator = paginate(venues, 5)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "venues/favorites.html", {"venues": page})


def news(request):
    news = News.objects.all().order_by("-date")
    paginator = paginate(news, 9)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "venues/news.html", {"news": page})


def events(request):
    events = Event.objects.all().order_by("-date")
    return render(request, "venues/events.html", {"events": events})


@login_required
def follow(request):
    if request.method == "POST":
        data = json.loads(request.body)
        venue = Venue.objects.get(id=data["venue"])
        data['name'] = venue.name
        if data["action"] == "follow":
            request.user.favorites.add(venue.id)
        else:
            request.user.favorites.remove(venue.id)
        return JsonResponse(data, status=200)


class CalendarView(ListView):
    model = Event
    template_name = 'venues/calendar.html'
    success_url = reverse_lazy("calendar")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return datetime(year, month, day=1)
    return datetime.today()


def prev_month(d_obj):
    first = d_obj.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d_obj):
    days_in_month = calendar.monthrange(d_obj.year, d_obj.month)[1]
    last = d_obj.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


@login_required
@user_passes_test(lambda u: u.is_vmanager)
def managed(request):
    manager = VManager.objects.get(user=request.user)
    context = {"venues": manager.venue.all()}
    return render(request, 'venues/managed.html', context)


def profile(request, user):
    return render(request, 'venues/profile.html')


@login_required
@user_passes_test(lambda u: u.is_vmanager)
def post_event(request, user):
    if request.method == 'POST':
        data = request.POST
        date = data['date'].strip('""') 
        date = datetime.strptime(date, "%d/%m/%Y %H:%M")
        author = request.user.vmanager
        event = Event(
            author=author,
            description=data['description'],    
            title=data['title'],
            venue=Venue.objects.get(id=data['venue']),
            date=date
        )
        event.save()
        return HttpResponseRedirect(reverse('events'))

    manager = get_object_or_404(VManager, user=request.user)
    form = EventForm()
    form.fields['venue'].queryset = manager.venue.all()
    context = {"form": form}
    return render(request, "venues/post_event.html", context)


@login_required
@user_passes_test(lambda u: u.is_vmanager)
def post_news(request, user):
    if request.method == 'POST':
        data = request.POST
        author = request.user.vmanager
        article = News(
            author=author,
            content=data['content'],    
            title=data['title'],
            venue=Venue.objects.get(id=data['venue']),
        )
        article.save()
        return HttpResponseRedirect(reverse('news'))
    manager = get_object_or_404(VManager, user=request.user)
    form = NewsForm()
    form.fields['venue'].queryset = manager.venue.all()
    context = {"form": form, }
    return render(request, "venues/post_news.html", context)
