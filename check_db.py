#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from knowledge.models import RUGIPOKnowledge
from django.db.models import Count

print(f'Total items in RUGIPOKnowledge: {RUGIPOKnowledge.objects.count()}')
print(f'\nBy category:')
for item in RUGIPOKnowledge.objects.values('category').annotate(count=Count('id')):
    print(f'  {item["category"]}: {item["count"]}')

print(f'\nRecent items:')
for item in RUGIPOKnowledge.objects.order_by('-created_at')[:5]:
    print(f'  - [{item.category}] {item.question[:60]}...')
    print(f'    Source: {item.source_url}')
