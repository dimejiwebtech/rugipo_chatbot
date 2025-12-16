#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from knowledge.models import RUGIPOKnowledge

# Clear all general knowledge items (keep engineering)
deleted_count = RUGIPOKnowledge.objects.filter(knowledge_type='general').delete()[0]
print(f'✓ Deleted {deleted_count} general knowledge items')
print(f'Remaining items (engineering): {RUGIPOKnowledge.objects.filter(knowledge_type="engineering").count()}')
