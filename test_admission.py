#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from chatbot.services.openai_service import fallback_keyword_search

# Test the exact user query
result = fallback_keyword_search("what is the latest admission process?")
print("Response to: 'what is the latest admission process?'")
print("=" * 70)
print(result)
print("=" * 70)
print(f"\nResponse length: {len(result)} characters (~{len(result)//3} words)")
