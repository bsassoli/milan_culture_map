"""
Run this script in django shell to import venues as model instances
"""
import pandas as pd
from venues.models import Venue, Category
df = pd.read_excel('venues/venues.xlsx')

for index, row in df.iterrows():
    name = row['name']
    latitude = float(row['latitude'])
    longitude = float(row['longitude'])
    address = row['address']
    url = str(row['url'])
    try:
        category = Category.objects.get(name=row['category'])
        venue = Venue(category=category, name=name, latitude=latitude,
                      longitude=longitude, address=address, url=url)
        venue.save()
    except Exception:
        print(name, row['category'])
    
