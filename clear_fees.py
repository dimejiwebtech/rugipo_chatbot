#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from knowledge.models import RUGIPOKnowledge

# Delete items from the fees URL
fees_url = 'https://backtoschool.com.ng/rufus-giwa-polytechnic-school-fees/'
deleted_count = RUGIPOKnowledge.objects.filter(source_url=fees_url).delete()[0]
print(f'✓ Deleted {deleted_count} items from fees URL')
