#!/usr/bin/env python
import json

with open('data/general_qa.json', encoding='utf-8') as f:
    data = json.load(f)

print("Top 5 longest answers:\n")
sorted_items = sorted(data['qa_data'], key=lambda x: len(x['answer']), reverse=True)[:5]

for i, item in enumerate(sorted_items, 1):
    print(f"{i}. {item['question'][:60]}...")
    print(f"   Length: {len(item['answer'])} characters (~{len(item['answer'])//3} words)")
    print(f"   Answer: {item['answer'][:200]}...")
    print()
