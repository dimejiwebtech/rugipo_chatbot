from django.contrib import admin
from django.contrib import messages
from .models import RUGIPOKnowledge, EngineeringQA, ScraperURL
from .utils import export_engineering_qa_to_json
from .scraper import scrape_rugipo_data

@admin.register(RUGIPOKnowledge)
class RUGIPOKnowledgeAdmin(admin.ModelAdmin):
    list_display = ['question_preview', 'category', 'is_active', 'source_url', 'updated_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['question', 'answer', 'keywords']
    list_editable = ['is_active']
    date_hierarchy = 'created_at'
    actions = ['activate_selected', 'deactivate_selected', 'export_to_json', 'scrape_websites']
    
    fieldsets = (
        ('Question & Answer', {
            'fields': ('category', 'question', 'answer')
        }),
        ('Metadata', {
            'fields': ('keywords', 'source_url', 'is_active')
        }),
    )
    
    def question_preview(self, obj):
        return obj.question[:60] + '...' if len(obj.question) > 60 else obj.question
    question_preview.short_description = 'Question'
    
    def activate_selected(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} Q&A(s) activated successfully.', messages.SUCCESS)
    activate_selected.short_description = 'Activate selected Q&As'
    
    def deactivate_selected(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} Q&A(s) deactivated successfully.', messages.SUCCESS)
    deactivate_selected.short_description = 'Deactivate selected Q&As'
    
    def export_to_json(self, request, queryset):
        json_path = export_engineering_qa_to_json()
        self.message_user(request, f'✓ Exported to {json_path}', messages.SUCCESS)
    export_to_json.short_description = 'Export all active Q&As to JSON'
    
    def scrape_websites(self, request, queryset):
        """Trigger website scraping and update database"""
        try:
            result = scrape_rugipo_data()
            export_engineering_qa_to_json()
            self.message_user(
                request,
                f'✓ Scrape completed: Added {result["added"]}, Updated {result["updated"]}',
                messages.SUCCESS
            )
        except Exception as e:
            self.message_user(request, f'✗ Scrape failed: {str(e)}', messages.ERROR)
    scrape_websites.short_description = 'Scrape configured websites for new data'


# Register EngineeringQA as proxy
admin.site.unregister(RUGIPOKnowledge)

@admin.register(EngineeringQA)
class EngineeringQAAdmin(RUGIPOKnowledgeAdmin):
    list_filter = ['category', 'is_active', 'created_at']
    
    class Meta:
        proxy = True


@admin.register(ScraperURL)
class ScraperURLAdmin(admin.ModelAdmin):
    list_display = ['url', 'is_active', 'scrape_frequency', 'last_scraped', 'notes']
    list_filter = ['is_active', 'scrape_frequency', 'created_at']
    search_fields = ['url', 'notes']
    list_editable = ['is_active', 'scrape_frequency']
    date_hierarchy = 'created_at'
    actions = ['test_scrape_url', 'activate_urls', 'deactivate_urls']
    
    fieldsets = (
        ('URL Information', {
            'fields': ('url', 'notes')
        }),
        ('Scraping Settings', {
            'fields': ('is_active', 'scrape_frequency')
        }),
        ('Status', {
            'fields': ('last_scraped',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('last_scraped', 'created_at', 'updated_at')
    
    def test_scrape_url(self, request, queryset):
        """Test scraping selected URLs"""
        try:
            from .scraper import scrape_single_url
            total_added = 0
            total_updated = 0
            
            for scraper_url in queryset:
                result = scrape_single_url(scraper_url.url)
                total_added += result['added']
                total_updated += result['updated']
                scraper_url.last_scraped = __import__('django.utils.timezone', fromlist=['now']).now()
                scraper_url.save()
            
            export_engineering_qa_to_json()
            self.message_user(
                request,
                f'✓ Test scrape completed: Added {total_added}, Updated {total_updated}',
                messages.SUCCESS
            )
        except Exception as e:
            self.message_user(request, f'✗ Test scrape failed: {str(e)}', messages.ERROR)
    test_scrape_url.short_description = 'Test scrape selected URLs'
    
    def activate_urls(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} URL(s) activated.', messages.SUCCESS)
    activate_urls.short_description = 'Activate selected URLs'
    
    def deactivate_urls(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} URL(s) deactivated.', messages.SUCCESS)
    deactivate_urls.short_description = 'Deactivate selected URLs'
