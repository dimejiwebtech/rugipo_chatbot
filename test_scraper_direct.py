#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from knowledge.scraper import GenericScraper

# Test the scraper directly
scraper = GenericScraper()
test_urls = [
    'https://thenigeriaeducationnews.com/',
    'https://www.rugipopress.com.ng/',
]

for url in test_urls:
    print(f'\nTesting: {url}')
    print('-' * 60)
    try:
        html_content = scraper.fetch_page(url)
        if html_content:
            print(f'✓ Page fetched ({len(html_content)} bytes)')
            is_rugipo = scraper.is_rugipo_related(html_content)
            print(f'✓ RUGIPO related: {is_rugipo}')
            
            qa_list = scraper.extract_content(html_content, url)
            print(f'✓ Extracted {len(qa_list)} Q&A items')
            
            if qa_list:
                print(f'\nFirst item:')
                item = qa_list[0]
                print(f'  Q: {item["question"][:80]}')
                print(f'  Category: {item["category"]}')
        else:
            print('✗ Failed to fetch page')
    except Exception as e:
        import traceback
        print(f'✗ Error: {str(e)}')
        traceback.print_exc()
