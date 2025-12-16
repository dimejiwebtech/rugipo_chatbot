from django.core.management.base import BaseCommand
from knowledge.utils import export_engineering_qa_to_json, export_general_qa_to_json


class Command(BaseCommand):
    help = 'Export all active Q&A from database to JSON files (engineering_qa.json and general_qa.json)'

    def handle(self, *args, **options):
        try:
            # Export engineering
            eng_path = export_engineering_qa_to_json()
            self.stdout.write(
                self.style.SUCCESS(f'✓ Exported Engineering Q&A to: {eng_path}')
            )
            
            # Export general
            gen_path = export_general_qa_to_json()
            self.stdout.write(
                self.style.SUCCESS(f'✓ Exported General Q&A to: {gen_path}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Error exporting Q&A: {str(e)}')
            )
