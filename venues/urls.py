from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("map", views.map, name="map"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("venue/<str:venue>", views.venue, name="venue"),
    path("registermanager", views.registermanager, name="registermanager"),
    path("edit", views.edit, name='edit'),
    path("favorites", views.favorites, name="favorites"),
    path("news", views.news, name="news"),
    path("events", views.events, name="events"),
    path("follow", views.follow, name="follow"),
    path('calendar/', views.CalendarView.as_view(), name='calendar'),
    path('managed', views.managed, name="managed"),
    path('post_news/<str:user>', views.post_news, name="post_news"),
    path('post_event/<str:user>', views.post_event, name="post_event"),
    path('profile/<str:user>', views.profile, name="profile"),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$',
        views.activate, name='activate'),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

