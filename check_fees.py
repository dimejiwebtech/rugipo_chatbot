#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from knowledge.models import RUGIPOKnowledge

# Check for fees category
fees_items = RUGIPOKnowledge.objects.filter(category='fees')
print(f'Fees items in database: {fees_items.count()}')

if fees_items.exists():
    print('\nFees items:')
    for item in fees_items:
        print(f'  - {item.question[:70]}...')
        print(f'    Source: {item.source_url}')
        print(f'    Knowledge Type: {item.knowledge_type}')
