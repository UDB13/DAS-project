import requests
from datetime import timedelta
from django.utils import timezone
from .models import DisasterAlert



# Define India's approximate bounding box
INDIA_BOUNDS = {
    "min_lat": 6.0,
    "max_lat": 37.5,
    "min_lon": 68.0,
    "max_lon": 97.5,
}

def is_in_india(lat, lon):
    return (INDIA_BOUNDS["min_lat"] <= lat <= INDIA_BOUNDS["max_lat"] and
            INDIA_BOUNDS["min_lon"] <= lon <= INDIA_BOUNDS["max_lon"])

def fetch_eonet_data():
    url = 'https://eonet.gsfc.nasa.gov/api/v3/events?status=open'

    try:
        # response = requests.get(url, timeout=20)  # Add timeout for safety
        response = requests.get(url)
        response.raise_for_status()  # Raise error for bad status codes
        data = response.json()
    except requests.RequestException as e:
        print(f"❌ Failed to fetch data from EONET API: {e}")
        return False

    # Delete alerts older than 5 days
    five_days_ago = timezone.now() - timedelta(days=5)
    DisasterAlert.objects.filter(timestamp__lt=five_days_ago).delete()

    for event in data.get("events", []):
        try:
            title = event["title"]
            description = event.get("description", "No description available.")
            event_type = event["categories"][0]["title"]
            source_url = event["sources"][0]["url"] if event.get("sources") else ""
            geometry = event.get("geometry", [])
            location = geometry[0]["coordinates"] if geometry else None

            latitude = longitude = None
            if location:
                longitude, latitude = location  # (lon, lat)

            if latitude is not None and longitude is not None:
                if is_in_india(latitude, longitude):
                    location_text = "India"
                else:
                    location_text = "Global"
            else:
                location_text = "Global"
            
            # Save or update alert
            DisasterAlert.objects.update_or_create(
                title=title,
                defaults={
                    "description": description,
                    "event_type": event_type,
                    "location": location_text,
                    "latitude": latitude,
                    "longitude": longitude,
                    "timestamp": timezone.now(),
                    "source_url": source_url,
                },
            )
        except (KeyError, IndexError, TypeError) as e:
            print(f"⚠️ Skipping event due to data error: {e}")
            continue  # Move to the next event safely

    return True  # Success after processing events