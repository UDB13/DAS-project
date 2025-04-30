from django.core.management.base import BaseCommand
from alerts.utils import fetch_eonet_data  # Import your fetch function

class Command(BaseCommand):
    help = 'Fetch latest disaster alerts from NASA EONET API'

    def handle(self, *args, **kwargs):
        success = fetch_eonet_data()
        if success:
            self.stdout.write(self.style.SUCCESS('✅ Successfully fetched latest disaster alerts!'))
        else:
            self.stdout.write(self.style.ERROR('❌ Failed to fetch latest disaster alerts!'))