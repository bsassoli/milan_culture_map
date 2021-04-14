from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse


import datetime



# Create your models here.
class User(AbstractUser):
    is_vmanager = models.BooleanField(default=False)


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Venue(models.Model):
    name = models.CharField(max_length=400)

    latitude = models.FloatField()

    longitude = models.FloatField()

    address = models.TextField()

    url = models.URLField(
        max_length=300,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.RESTRICT,
        related_name="venues",
    )
    
    image = models.ImageField(
        upload_to="images/",
        default="logo-comune-milano.png",
    )

    description = models.TextField(
        default="",
        blank=True,
    )

    followers = models.ManyToManyField(
        User,
        blank=True,
        related_name="favorites",
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class VManager(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True, 
        default="",
        related_name="vmanager",
    )

    venue = models.ManyToManyField(
        Venue,
        related_name="vmanager",
    )

    class Meta:
        verbose_name = "Venue Manager"
        ordering = ["user"]

    def __str__(self):
        return self.user.username


class Event(models.Model):
    author = models.ForeignKey(
        VManager,
        on_delete=models.RESTRICT
    )
    
    venue = models.ForeignKey(
        Venue,
        related_name="event",
        on_delete=models.CASCADE
    )

    title = models.TextField()

    date = models.DateTimeField(default=datetime.date.today)

    description = models.TextField()

    def __str__(self):
        return f"{self.title} di {self.venue} il {self.date}"
    
    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        return f'<p>{self.title}</p><a href="{url}">edit</a>'


class News(models.Model):
    author = models.ForeignKey(
        VManager,
        on_delete=models.RESTRICT,
    )

    venue = models.ForeignKey(
        Venue,
        related_name="news",
        on_delete=models.CASCADE
    )

    title = models.TextField()

    date = models.DateTimeField(auto_now_add=True)

    content = models.TextField()

    class Meta:
        verbose_name_plural = "news"

    def __str__(self):
        return f"{self.title}, {self.venue}"


class Map(models.Model):
    html = models.TextField()
