from django.contrib import admin
from chatbot.models import ChatSession, ChatMessage

class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ['message_type', 'content', 'created_at']
    can_delete = False

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'created_at', 'last_activity', 'message_count']
    readonly_fields = ['session_id', 'created_at', 'last_activity']
    inlines = [ChatMessageInline]
    list_filter = ['created_at', 'last_activity']
    date_hierarchy = 'created_at'
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session_link', 'message_type', 'content_preview', 'created_at']
    list_filter = ['message_type', 'created_at']
    readonly_fields = ['session', 'message_type', 'content', 'created_at']
    search_fields = ['content']
    date_hierarchy = 'created_at'
    
    def session_link(self, obj):
        return str(obj.session.session_id)[:8]
    session_link.short_description = 'Session'
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'