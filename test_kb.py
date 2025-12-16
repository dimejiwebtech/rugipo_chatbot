#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from chatbot.services.openai_service import load_knowledge_base, fallback_keyword_search

# Test loading knowledge base
kb = load_knowledge_base()
print(f'✓ Knowledge base loaded: {len(kb)} items')

# Group by category
cats = {}
for item in kb:
    cat = item['category']
    cats[cat] = cats.get(cat, 0) + 1

print(f'\nCategories:')
for cat in sorted(cats.keys()):
    print(f'  {cat}: {cats[cat]}')

# Test search for "SSANIP" mentioned in the user's question
print(f'\n\nTesting search for "SSANIP activities":')
result = fallback_keyword_search("SSANIP NASU activities suspended")
print(result[:200] + "..." if len(result) > 200 else result)

# Test search for fees
print(f'\n\nTesting search for "school fees":')
result = fallback_keyword_search("how much are RUGIPO school fees")
print(result[:200] + "..." if len(result) > 200 else result)
