from django.db import models

class RUGIPOKnowledge(models.Model):
    """
    Store questions and answers about RUGIPO - General and Engineering
    """
    KNOWLEDGE_TYPE_CHOICES = [
        ('engineering', 'Engineering Knowledge'),
        ('general', 'General Knowledge'),
    ]
    
    CATEGORY_CHOICES = [
        ('general', 'General RUGIPO Information'),
        ('abet', 'Agricultural and Bio-Environmental Engineering Technology'),
        ('cet', 'Civil Engineering Technology'),
        ('cte', 'Computer Engineering Technology'),
        ('eeet', 'Electrical/Electronics Engineering Technology'),
        ('met', 'Mechanical Engineering Technology'),
        ('admissions', 'Admissions & Registration'),
        ('facilities', 'Facilities & Campus'),
        ('news', 'News & Events'),
        ('academic', 'Academic Programs'),
        ('student_services', 'Student Services'),
        ('fees', 'Fees & Payments'),
    ]
    
    knowledge_type = models.CharField(
        max_length=20,
        choices=KNOWLEDGE_TYPE_CHOICES,
        default='general',
        help_text='Type of knowledge: Engineering or General'
    )
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    question = models.TextField(help_text='The question students might ask')
    answer = models.TextField(help_text='The answer to provide')
    keywords = models.CharField(
        max_length=255, 
        blank=True,
        help_text='Comma-separated keywords for better matching'
    )
    source_url = models.URLField(
        blank=True,
        null=True,
        help_text='Where this information was sourced from'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'RUGIPO Knowledge'
        verbose_name_plural = 'RUGIPO Knowledge Base'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"[{self.get_category_display()}] {self.question[:60]}"


# Keep old name for backward compatibility
class EngineeringQA(RUGIPOKnowledge):
    """
    Proxy model for backward compatibility
    """
    class Meta:
        proxy = True
        verbose_name = 'Engineering Q&A'
        verbose_name_plural = 'Engineering Q&As'


class ScraperURL(models.Model):
    """
    Store URLs to scrape for RUGIPO information
    """
    url = models.URLField(unique=True, help_text='Website URL to scrape')
    is_active = models.BooleanField(
        default=True,
        help_text='Enable/disable scraping for this URL'
    )
    scrape_frequency = models.CharField(
        max_length=50,
        default='daily',
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('manual', 'Manual Only'),
        ]
    )
    last_scraped = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Last time this URL was scraped'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notes = models.TextField(
        blank=True,
        help_text='Notes about this source'
    )
    
    class Meta:
        verbose_name = 'Scraper URL'
        verbose_name_plural = 'Scraper URLs'
        ordering = ['url']
    
    def __str__(self):
        return f"{'✓' if self.is_active else '✗'} {self.url}"