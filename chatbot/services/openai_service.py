from openai import OpenAI
from django.conf import settings
import json

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def load_knowledge_base():
    """
    Load all Q&A from JSON files (engineering + general)
    """
    qa_data = []
    
    # Load engineering knowledge
    try:
        with open(settings.KNOWLEDGE_BASE_JSON_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            qa_data.extend(data.get('qa_data', []))
    except FileNotFoundError:
        pass
    
    # Load general knowledge
    try:
        from pathlib import Path
        general_path = Path(settings.BASE_DIR) / 'data' / 'general_qa.json'
        with open(general_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            qa_data.extend(data.get('qa_data', []))
    except FileNotFoundError:
        pass
    
    return qa_data

def create_system_prompt():
    """
    Create system prompt with knowledge base
    """
    knowledge_base = load_knowledge_base()
    
    prompt = """You are an AI assistant for Rufus Giwa Polytechnic (RUGIPO) student support services.
Your role is to help students with information about RUGIPO, including engineering programs, general information, admissions, fees, and other student services.

IMPORTANT INSTRUCTIONS:
1. Be friendly, professional, and helpful
2. Use the comprehensive knowledge base provided below
3. If you don't have information in the knowledge base, use your general knowledge
4. If you still don't know, be honest and suggest they contact the admin office
5. Keep responses concise but informative
6. Use simple, clear language

RUGIPO KNOWLEDGE BASE:
"""
    
    if knowledge_base:
        for qa in knowledge_base:
            prompt += f"\n\nCategory: {qa['category_display']}"
            prompt += f"\nQ: {qa['question']}"
            prompt += f"\nA: {qa['answer']}"
    else:
        prompt += "\n(No Faculty of Engineering data available yet)"
    
    prompt += "\n\nRemember: Always be helpful and guide students to the right information or resources."
    
    return prompt

def fallback_keyword_search(user_message):
    """
    Simple keyword-based search for when OpenAI is unavailable
    """
    knowledge_base = load_knowledge_base()
    user_message_lower = user_message.lower()
    
    # Search for matching questions
    best_match = None
    highest_score = 0
    
    for qa in knowledge_base:
        score = 0
        question_lower = qa['question'].lower()
        answer_lower = qa['answer'].lower()
        keywords = qa.get('keywords', '').lower()
        
        # Check if words from user message appear in question, answer or keywords
        words = user_message_lower.split()
        for word in words:
            if len(word) > 3:  # Ignore short words
                if word in question_lower:
                    score += 3
                if word in keywords:
                    score += 2
                if word in answer_lower:
                    score += 1
        
        if score > highest_score:
            highest_score = score
            best_match = qa
    
    if best_match and highest_score > 0:
        return f"**{best_match['category_display']}**\n\n{best_match['answer']}\n\nIf you need more specific information, please contact the Faculty office."
    
    return """Hello! I'm the RUGIPO AI assistant. I can help you with information about:

**RUGIPO Knowledge Base:**
- Faculty of Engineering courses and programs
- Admissions & Registration procedures
- School Fees & Payments
- Academic Programs & Calendar
- Student Services & Facilities
- News & Events
- General RUGIPO Information

**Available Categories:**
- Civil Engineering Technology
- Computer Engineering Technology
- Electrical/Electronics Engineering Technology
- Mechanical Engineering Technology
- Agricultural & Bio-Environmental Engineering
- General Information
- Fees & Payments
- Academic Programs
- And more...

"""

def get_chatbot_response(user_message, conversation_history=None):
    """
    Get response from OpenAI ChatGPT with fallback to keyword search
    """
    if not settings.OPENAI_API_KEY:
        return "OpenAI API key is not configured. Using basic mode.\n\n" + fallback_keyword_search(user_message)
    
    try:
        messages = [
            {"role": "system", "content": create_system_prompt()}
        ]
        
        # Add conversation history if exists
        if conversation_history:
            for msg in conversation_history:
                messages.append({
                    "role": msg['role'],
                    "content": msg['content']
                })
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        pass
        # If OpenAI fails (quota, network, etc), use fallback
        error_msg = str(e)
        if 'insufficient_quota' in error_msg or '429' in error_msg:
            return "⚠️ OpenAI quota exceeded. Using basic search mode.\n\n" + fallback_keyword_search(user_message)
        return "Sorry, I encountered an error. Using basic mode.\n\n" + fallback_keyword_search(user_message)