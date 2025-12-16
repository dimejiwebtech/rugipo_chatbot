#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from chatbot.services.openai_service import fallback_keyword_search

test_queries = [
    "what is the latest admission process?",
    "how much is RUGIPO school fees",
    "hostel fees",
    "news about RUGIPO"
]

for query in test_queries:
    print(f"\n{'='*70}")
    print(f"Query: {query}")
    print(f"{'='*70}")
    result = fallback_keyword_search(query)
    # Show first 400 chars
    if len(result) > 400:
        print(result[:400] + "...\n[Response continues...]")
    else:
        print(result)
