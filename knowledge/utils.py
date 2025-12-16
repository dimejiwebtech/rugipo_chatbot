import json
from pathlib import Path
from django.conf import settings

def export_engineering_qa_to_json():
    """
    Export all active Engineering RUGIPO Knowledge to JSON file
    """
    from knowledge.models import RUGIPOKnowledge
    
    qa_list = RUGIPOKnowledge.objects.filter(
        is_active=True,
        knowledge_type='engineering'
    ).order_by('category', 'created_at')
    
    data = {
        'last_updated': str(qa_list.latest('updated_at').updated_at) if qa_list.exists() else None,
        'total_count': qa_list.count(),
        'qa_data': []
    }
    
    for qa in qa_list:
        data['qa_data'].append({
            'id': qa.id,
            'category': qa.category,
            'category_display': qa.get_category_display(),
            'question': qa.question,
            'answer': qa.answer,
            'keywords': qa.keywords,
            'source_url': qa.source_url,
        })
    
    # Ensure data directory exists
    json_path = settings.KNOWLEDGE_BASE_JSON_PATH
    json_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write to JSON file
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return json_path


def export_general_qa_to_json():
    """
    Export all active General RUGIPO Knowledge to JSON file (general_qa.json)
    """
    from knowledge.models import RUGIPOKnowledge
    
    qa_list = RUGIPOKnowledge.objects.filter(
        is_active=True,
        knowledge_type='general'
    ).order_by('category', 'created_at')
    
    data = {
        'last_updated': str(qa_list.latest('updated_at').updated_at) if qa_list.exists() else None,
        'total_count': qa_list.count(),
        'qa_data': []
    }
    
    for qa in qa_list:
        data['qa_data'].append({
            'id': qa.id,
            'category': qa.category,
            'category_display': qa.get_category_display(),
            'question': qa.question,
            'answer': qa.answer,
            'keywords': qa.keywords,
            'source_url': qa.source_url,
        })
    
    # Save to general_qa.json instead
    json_path = Path(settings.BASE_DIR) / 'data' / 'general_qa.json'
    json_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write to JSON file
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    return json_path