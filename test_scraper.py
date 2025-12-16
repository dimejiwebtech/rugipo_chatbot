#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from knowledge.models import ScraperURL, RUGIPOKnowledge
from knowledge.scraper import scrape_single_url

# Get a URL to test
url_obj = ScraperURL.objects.first()
print(f'Testing with URL: {url_obj.url}')
print('---')

# Test the scraper
try:
    result = scrape_single_url(url_obj.url)
    print(f'✓ Scraper completed successfully')
    print(f'  Total items processed: {result.get("total", 0)}')
    print(f'  Items added to DB: {result.get("added", 0)}')
    print(f'  Items updated: {result.get("updated", 0)}')
    
    # Show some saved items
    print(f'\n✓ Sample items from database:')
    items = RUGIPOKnowledge.objects.filter(source_url=url_obj.url).order_by('-created_at')[:2]
    for i, item in enumerate(items, 1):
        print(f'\nItem {i}:')
        print(f'  Q: {item.question[:60]}...')
        print(f'  Category: {item.category}')
        print(f'  Source: {item.source_url}')
except Exception as e:
    import traceback
    print(f'✗ Error: {str(e)}')
    traceback.print_exc()
