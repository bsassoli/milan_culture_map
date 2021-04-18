from django.test import TestCase
from venues.models import Venue, Category

# Create your tests here.


class VenuesTestCase(TestCase):
    def setUp(self):
        category = Category.objects.create(name="Cinema")
        venue1 = Venue.objects.create(
            name="Fake Venue", 
            address="Via dei Piatti, 9", 
            latitude=2.12,
            longitude=2.33,
            url="http://www.sassoli.io",
            category=category,
        )

    def test_category(self):
        venue = Venue.objects.get(name="Fake Venue")
        category = Category.objects.get(name="Cinema")
        self.assertEqual(venue.category, category)
