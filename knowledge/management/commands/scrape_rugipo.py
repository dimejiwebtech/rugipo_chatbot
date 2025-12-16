from django.core.management.base import BaseCommand
from knowledge.scraper import scrape_rugipo_data


class Command(BaseCommand):
    help = 'Scrape RUGIPO website for engineering information and update database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--export',
            action='store_true',
            help='Export to JSON after scraping',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('🔄 Starting RUGIPO data scrape...'))
        
        try:
            result = scrape_rugipo_data()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f"✓ Scrape completed!\n"
                    f"  • Added: {result['added']} Q&As\n"
                    f"  • Updated: {result['updated']} Q&As\n"
                    f"  • Total processed: {result['total']}"
                )
            )
            
            # Export to JSON if requested
            if options['export']:
                from knowledge.utils import export_engineering_qa_to_json
                json_path = export_engineering_qa_to_json()
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Exported to JSON: {json_path}')
                )
        
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Error during scrape: {str(e)}')
            )
