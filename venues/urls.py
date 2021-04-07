from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


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
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
