#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from knowledge.models import RUGIPOKnowledge

# Find admission items
admission_items = RUGIPOKnowledge.objects.filter(category='admissions', knowledge_type='general')
print(f"Found {admission_items.count()} admission items\n")

for item in admission_items:
    print(f"Q: {item.question}")
    print(f"Answer length: {len(item.answer)} chars")
    print(f"Answer:\n{item.answer}\n")
    print("-" * 70)
