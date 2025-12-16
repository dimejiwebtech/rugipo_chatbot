#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from knowledge.models import RUGIPOKnowledge, ScraperURL

# Check items from the fees URL
fees_url = 'https://backtoschool.com.ng/rufus-giwa-polytechnic-school-fees/'
items_from_fees = RUGIPOKnowledge.objects.filter(source_url=fees_url)
print(f'Items from {fees_url}:')
print(f'Total: {items_from_fees.count()}')

if items_from_fees.exists():
    print('\nItems:')
    for item in items_from_fees:
        print(f'  - [{item.category}] {item.question[:60]}...')
else:
    print('No items found from this URL')

# Check if URL was scraped
url_obj = ScraperURL.objects.filter(url=fees_url).first()
if url_obj:
    print(f'\nURL object found:')
    print(f'  Last scraped: {url_obj.last_scraped}')
