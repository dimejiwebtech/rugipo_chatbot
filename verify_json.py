#!/usr/bin/env python
import json

with open('data/engineering_qa.json') as f:
    data = json.load(f)

print(f'Total items in JSON: {data["total_count"]}')
print(f'\nCategories breakdown:')

cats = {}
for item in data['qa_data']:
    cat = item['category']
    cats[cat] = cats.get(cat, 0) + 1

for cat in sorted(cats.keys()):
    print(f'  {cat}: {cats[cat]}')

print(f'\nSample items from scraped sources:')
for item in data['qa_data'][:5]:
    print(f'\n  Q: {item["question"][:60]}...')
    print(f'  Category: {item["category"]}')
    print(f'  Source: {item.get("source_url", "No source")}')
