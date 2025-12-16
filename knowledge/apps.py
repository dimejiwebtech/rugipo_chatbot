from django.apps import AppConfig

class KnowledgeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'knowledge'
    
    def ready(self):
        import knowledge.signals
        
        # Start background scheduler for periodic scraping (only in production-like setups)
        # Comment this out during development if you want manual control
        try:
            from django.conf import settings
            if getattr(settings, 'START_SCHEDULER', False):
                from knowledge.scheduler import start_scheduler
                start_scheduler()
        except Exception as e:
            # Scheduler is optional, app works without it
            pass