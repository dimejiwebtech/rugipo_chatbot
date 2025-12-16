from django.core.management.base import BaseCommand
from knowledge.models import ScraperURL


class Command(BaseCommand):
    help = 'Load default scraper URLs into database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing URLs before loading',
        )

    def handle(self, *args, **options):
        if options['clear']:
            ScraperURL.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared existing URLs'))

        # Define default URLs
        urls = [
            {
                'url': 'https://thenigeriaeducationnews.com/',
                'notes': 'Nigeria Education News - RUGIPO updates and stories'
            },
            {
                'url': 'https://www.rugipopress.com.ng/',
                'notes': 'RUGIPO Press - Official news and announcements'
            },
            {
                'url': 'https://myschool.ng/news/latest?school=rufus-giwa-polytechnic',
                'notes': 'MySchool.ng - RUGIPO news and updates'
            },
            {
                'url': 'https://r.rugipo.edu.ng/news/',
                'notes': 'RUGIPO Official News - Internal news portal'
            },
            {
                'url': 'https://www.newslineng.com.ng/search?q=rugipo',
                'notes': 'NewsLine Nigeria - RUGIPO search results'
            },
            {
                'url': 'https://www.newslineng.com.ng/search?q=rufus+giwa',
                'notes': 'NewsLine Nigeria - Rufus Giwa search results'
            },
            {
                'url': 'https://backtoschool.com.ng/rufus-giwa-polytechnic-school-fees/',
                'notes': 'Back to School - RUGIPO school fees information'
            },
        ]

        created_count = 0
        for url_data in urls:
            scraper_url, created = ScraperURL.objects.get_or_create(
                url=url_data['url'],
                defaults={
                    'is_active': True,
                    'scrape_frequency': 'daily',
                    'notes': url_data['notes']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {url_data["url"]}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠ Already exists: {url_data["url"]}'))

        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Loaded {created_count} new scraper URLs')
        )
