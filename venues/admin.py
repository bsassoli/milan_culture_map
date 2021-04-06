from django.contrib import admin

# Register your models here.
from .models import User, Venue, Category, Event, News, VManager, Map


class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'url')
    list_filter = ('category', )
    ordering = ('name', )
    search_fields = ['name']


class VenueInLineAdmin(admin.TabularInline):
    model = Venue.followers.through


class UserAdmin(admin.ModelAdmin):
    search_fields = ['username']
    ordering = ('username', )
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'is_staff', 'is_vmanager', 'is_active')
        }),
    )
    inlines = [VenueInLineAdmin]


admin.site.register(User, UserAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Category)
admin.site.register(Event)
admin.site.register(News)
admin.site.register(VManager)
admin.site.register(Map)
