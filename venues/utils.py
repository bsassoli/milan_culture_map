import functools
import folium
import numpy as np
import os
from PIL import Image
from calendar import HTMLCalendar
from folium.plugins import (
    LocateControl,
    MarkerCluster,
    FeatureGroupSubGroup,
    Fullscreen,
    Search,
)
from geopy.geocoders import Here
from .models import Event, Category, Venue
from .constants import MILAN_CENTER, ICONS

# code from https://stackoverflow.com/a/30462851


def image_transpose_exif(img):
    """
    Apply Image.transpose to ensure 0th row of pixels is at the visual
    top of the image, and 0th column is the visual left-hand side.
    Return the original image if unable to determine the orientation.
    As per CIPA DC-008-2012, the orientation field contains an integer,
    1 through 8. Other values are reserved.
    Parameters
    ----------
    im: PIL.Image
       The image to be rotated.
    """

    exif_orientation_tag = 0x0112
    exif_transpose_sequences = [                   # Val  0th row  0th col
        [],  # 0    (reserved)
        [],  # 1   top      left
        [Image.FLIP_LEFT_RIGHT],  # 2   top      right
        [Image.ROTATE_180],  # 3   bottom   right
        [Image.FLIP_TOP_BOTTOM],  # 4   bottom   left
        [Image.FLIP_LEFT_RIGHT, Image.ROTATE_90],  # 5   left     top
        [Image.ROTATE_270],  # 6   right    top
        [Image.FLIP_TOP_BOTTOM, Image.ROTATE_90],  # 7   right    bottom
        [Image.ROTATE_90],  # 8   left     bottom
    ]

    try:
        seq = exif_transpose_sequences[img._getexif()[exif_orientation_tag]]
    except Exception:
        return img
    else:
        return functools.reduce(type(img).transpose, seq, img)


def resize_image(img_path, height, width):
    """ Resizes the img and blocks its rotation """

    img = Image.open(img_path)
    img = image_transpose_exif(img)

    if img.height > height or img.width > width:
        output_size = (height, width)
        img.thumbnail(output_size)
    img.save(img_path)


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, events):
        events_per_day = events.filter(date__day=day)
        d = ''
        for event in events_per_day:
            d += f'<li class="calendar event begin span-2 list-unstyled bg-warning"> {event.title} </li>'  # This is where get_event_html_url was
        if day != 0:
            return f"<td><span class='calendar days'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    def formatmonth(self, withyear=True):
        events = Event.objects.filter(date__year=self.year, date__month=self.month)
        cal = '<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal


def make_map(center=MILAN_CENTER):
    # Creating Map object

    m = folium.Map(
        location=center,
        tiles="cartodbpositron",
        zoom_start=12,
        control_scale=True,
        height="90%",
    )
    # Overriding default CSS which will interfere with navbar
    m.default_css = [
        ("leaflet_css", "https://cdn.jsdelivr.net/npm/leaflet@1.6.0/dist/leaflet.css"),
        (
            "awesome_markers_font_css",
            "https://maxcdn.bootstrapcdn.com/font-awesome/4.6.3/css/font-awesome.min.css",
        ),
        (
            "awesome_markers_css",
            "https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css",
        ),
        (
            "awesome_rotate_css",
            "https://cdn.jsdelivr.net/gh/python-visualization/folium/folium/templates/leaflet.awesome.rotate.min.css",
        ),
    ]
    # Add fullscreen button
    Fullscreen(
        title="Fullscreen",
        title_cancel="Exit fullscreen",
        force_separate_button=True
    ).add_to(m)

    # Create Folium cluster
    cluster = MarkerCluster(
        name="Tutte le venues",
        options={
            "showCoverageOnHover": False,
            "zoomToBoundsOnClick": True,
            "spiderfyOnMaxZoom": False,
            "disableClusteringAtZoom": 17,
        },
        control=False,
    )
    # Add cluster to map
    m.add_child(cluster)

    # Add categories
    layers = {}
    for category in Category.objects.all():
        layers[category.name] = FeatureGroupSubGroup(
            group=cluster,
            name=category.name)
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
            location[0] += np.random.uniform(0.0005, 10 ** (-20)) - 0.0000007
        locations.append(location)

        page = f"venue/{name}"
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
                  <a href="{page}">
                  {name}
                  <i class="fas fa-info-circle"></i>
                  </a>
                </h4>
                <h6 class="card-category">
                  {subgroup_category}
                </h6>
            </div>
            <div class="card-footer justify-content-center">
                {address}
            </div>
        </div>
    """,
            script=True,
        )
        category = ICONS[subgroup_category]
        try:
            category = ICONS[subgroup_category]
            venue_marker = folium.Marker(
                location=location,
                tooltip=name,
                popup=folium.Popup(html=html, max_width=600),
                icon=folium.Icon(
                    color=category["color"],
                    icon=category["icon"],
                    prefix=category["prefix"],
                ),
                name=name,
            )
            layers[subgroup_category].add_child(venue_marker)
        except Exception:
            print("Problem")

    # Add Layer Control to map
    folium.LayerControl().add_to(m)

    search = Search(layer=cluster, search_label='name', position='topright',
                    placeholder="Cerca", search_zoom=18)
    search.add_to(m)

    return m

def find_coordinates(address: str) -> list:
    """Return coordinates of an address from Here.

    Args:
        address (str): the address to be searched

    Returns:
        list: a list of [latitude, longitude]
    """
    # Choosing geolocation API
    geolocator = Here(apikey=os.environ['HERE_API'])
    try:
        coordinates = geolocator.geocode(address)
        return [coordinates.latitude, coordinates.longitude]
    except Exception:
        return "Not found"
