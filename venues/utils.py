import functools
from PIL import Image
from datetime import datetime, timedelta
from calendar import HTMLCalendar

from .models import Event


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
