from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from knowledge.scraper import scrape_rugipo_data
from knowledge.utils import export_engineering_qa_to_json
import logging

logger = logging.getLogger(__name__)


@login_required
@require_http_methods(["POST"])
def trigger_scrape(request):
    """
    Manually trigger RUGIPO data scraping
    Only accessible to authenticated admin users
    """
    try:
        logger.info(f"Scrape triggered by {request.user}")
        result = scrape_rugipo_data()
        
        # Auto-export after scraping
        export_engineering_qa_to_json()
        
        return JsonResponse({
            'success': True,
            'message': 'Scraping completed successfully',
            'result': {
                'added': result['added'],
                'updated': result['updated'],
                'total': result['total']
            }
        })
    except Exception as e:
        logger.error(f"Scrape error: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@login_required
@require_http_methods(["POST"])
def export_qa_view(request):
    """
    Manually trigger JSON export
    Only accessible to authenticated admin users
    """
    try:
        json_path = export_engineering_qa_to_json()
        return JsonResponse({
            'success': True,
            'message': f'Exported to {json_path}',
            'path': str(json_path)
        })
    except Exception as e:
        logger.error(f"Export error: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)