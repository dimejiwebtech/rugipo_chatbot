from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from chatbot.models import ChatSession, ChatMessage
from chatbot.services.openai_service import get_chatbot_response

@csrf_exempt
@require_http_methods(["POST"])
def send_message(request):
    """
    Handle incoming chat messages
    """
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', '')
        
        if not user_message:
            return JsonResponse({
                'success': False,
                'error': 'Message cannot be empty'
            }, status=400)
        
        # Get or create session
        session = None
        if session_id:
            try:
                session = ChatSession.objects.get(session_id=session_id)
            except ChatSession.DoesNotExist:
                pass
        
        if not session:
            session = ChatSession.objects.create()
        
        # Save user message
        ChatMessage.objects.create(
            session=session,
            message_type='user',
            content=user_message
        )
        
        # Get conversation history (last 10 messages)
        history = ChatMessage.objects.filter(session=session).order_by('-created_at')[:10]
        conversation_history = [
            {
                'role': 'assistant' if msg.message_type == 'bot' else 'user',
                'content': msg.content
            }
            for msg in reversed(history)
        ]
        
        # Get bot response from OpenAI
        bot_response = get_chatbot_response(user_message, conversation_history[:-1])
        
        # Save bot message
        ChatMessage.objects.create(
            session=session,
            message_type='bot',
            content=bot_response
        )
        
        return JsonResponse({
            'success': True,
            'bot_response': bot_response,
            'session_id': str(session.session_id)
        })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@require_http_methods(["GET"])
def get_history(request):
    """
    Retrieve chat history for a session
    """
    session_id = request.GET.get('session_id', '')
    
    if not session_id:
        return JsonResponse({
            'success': False,
            'error': 'Session ID required'
        }, status=400)
    
    try:
        session = ChatSession.objects.get(session_id=session_id)
        messages = ChatMessage.objects.filter(session=session).order_by('created_at')
        
        message_list = [
            {
                'type': msg.message_type,
                'content': msg.content,
                'timestamp': msg.created_at.isoformat()
            }
            for msg in messages
        ]
        
        return JsonResponse({
            'success': True,
            'messages': message_list
        })
    
    except ChatSession.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Session not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)