#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from knowledge.models import RUGIPOKnowledge

# Mark original engineering items as 'engineering' type
# These are the ones with engineering-specific categories
engineering_categories = ['abet', 'cet', 'cte', 'eeet', 'met']

# Get all items without source_url (the original ones)
original_items = RUGIPOKnowledge.objects.filter(source_url__isnull=True)
updated_count = 0

for item in original_items:
    if item.category in engineering_categories:
        item.knowledge_type = 'engineering'
        item.save()
        updated_count += 1

print(f'✓ Marked {updated_count} original engineering items')

# Check the counts
eng_count = RUGIPOKnowledge.objects.filter(knowledge_type='engineering').count()
gen_count = RUGIPOKnowledge.objects.filter(knowledge_type='general').count()

print(f'\nDatabase stats:')
print(f'  Engineering: {eng_count}')
print(f'  General: {gen_count}')
print(f'  Total: {eng_count + gen_count}')
