#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from knowledge.scraper import scrape_single_url

fees_url = 'https://backtoschool.com.ng/rufus-giwa-polytechnic-school-fees/'
result = scrape_single_url(fees_url)

print(f'✓ Scraped fees URL')
print(f'  Added: {result.get("added", 0)}')
print(f'  Updated: {result.get("updated", 0)}')
