from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from knowledge.models import EngineeringQA
from knowledge.utils import export_engineering_qa_to_json

@receiver(post_save, sender=EngineeringQA)
def export_on_save(sender, instance, **kwargs):
    """
    Auto-export to JSON whenever a Q&A is created or updated
    """
    export_engineering_qa_to_json()

@receiver(post_delete, sender=EngineeringQA)
def export_on_delete(sender, instance, **kwargs):
    """
    Auto-export to JSON whenever a Q&A is deleted
    """
    export_engineering_qa_to_json()