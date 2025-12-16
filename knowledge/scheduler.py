"""
Background task scheduler for periodic scraping
Uses APScheduler for scheduled tasks
"""
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings

logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler = None


def start_scheduler():
    """
    Initialize and start the background scheduler
    """
    global scheduler
    
    if scheduler is not None:
        return
    
    scheduler = BackgroundScheduler()
    
    # Schedule scraper to run daily at 2 AM
    try:
        from knowledge.scraper import scrape_rugipo_data
        
        scheduler.add_job(
            func=scheduled_scrape,
            trigger=CronTrigger(hour=2, minute=0),  # 2 AM daily
            id='rugipo_scraper',
            name='RUGIPO Data Scraper',
            replace_existing=True
        )
        
        scheduler.start()
        logger.info("✓ Background scheduler started - Scraper scheduled for 2 AM daily")
    except Exception as e:
        logger.error(f"Error starting scheduler: {str(e)}")


def stop_scheduler():
    """
    Stop the background scheduler
    """
    global scheduler
    
    if scheduler is not None:
        try:
            scheduler.shutdown()
            scheduler = None
            logger.info("✓ Background scheduler stopped")
        except Exception as e:
            logger.error(f"Error stopping scheduler: {str(e)}")


def scheduled_scrape():
    """
    Wrapper function for scheduled scraping
    """
    try:
        from knowledge.scraper import scrape_rugipo_data
        
        logger.info("⏰ Running scheduled RUGIPO data scrape...")
        result = scrape_rugipo_data()
        logger.info(
            f"✓ Scheduled scrape completed: "
            f"Added {result['added']}, Updated {result['updated']}"
        )
    except Exception as e:
        logger.error(f"✗ Scheduled scrape failed: {str(e)}")


def get_scheduler_status():
    """
    Get current scheduler status
    """
    global scheduler
    
    if scheduler is None:
        return {
            'status': 'not_running',
            'jobs': []
        }
    
    try:
        return {
            'status': 'running' if scheduler.running else 'stopped',
            'jobs': [
                {
                    'id': job.id,
                    'name': job.name,
                    'next_run': str(job.next_run_time) if job.next_run_time else 'Unknown'
                }
                for job in scheduler.get_jobs()
            ]
        }
    except Exception as e:
        logger.error(f"Error getting scheduler status: {str(e)}")
        return {'status': 'error', 'error': str(e)}
