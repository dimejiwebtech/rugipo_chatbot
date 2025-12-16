#!/usr/bin/env python
import json

print("=== ENGINEERING QA ===")
with open('data/engineering_qa.json') as f:
    eng_data = json.load(f)
    print(f'Total: {eng_data["total_count"]}')
    print(f'Categories: {set(item["category"] for item in eng_data["qa_data"])}')
    if eng_data["qa_data"]:
        print(f'Sample: {eng_data["qa_data"][0]["question"][:60]}...')

print("\n=== GENERAL QA ===")
with open('data/general_qa.json') as f:
    gen_data = json.load(f)
    print(f'Total: {gen_data["total_count"]}')
    cats = {}
    for item in gen_data["qa_data"]:
        cat = item["category"]
        cats[cat] = cats.get(cat, 0) + 1
    print(f'Categories breakdown:')
    for cat in sorted(cats.keys()):
        print(f'  {cat}: {cats[cat]}')
    print(f'\nRecent items:')
    for item in gen_data["qa_data"][:3]:
        print(f'  - {item["question"][:70]}...')
        print(f'    Source: {item.get("source_url", "N/A")}')
