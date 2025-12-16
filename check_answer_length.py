#!/usr/bin/env python
import json

with open('data/general_qa.json') as f:
    data = json.load(f)

# Find admission-related item
for item in data['qa_data']:
    if 'admission' in item['question'].lower() or 'admission' in item['category']:
        print(f"Question: {item['question']}")
        print(f"Category: {item['category_display']}")
        print(f"Answer length: {len(item['answer'])} characters")
        print(f"\nAnswer preview:")
        print(item['answer'][:1200])
        print("\n---\n")
        break

# Check average answer length
total_len = sum(len(item['answer']) for item in data['qa_data'])
avg_len = total_len // len(data['qa_data'])
print(f"Average answer length: {avg_len} characters (~{avg_len//3} words)")
