from datetime import datetime, timezone

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from utils.logger import get_logger
from utils.settings import get_settings
from utils.crawler import BooksCrawler

logger = get_logger("scheduler.scheduler")

_scheduler: AsyncIOScheduler | None = None

async def daily_task() -> None:
    logger.info("Daily Crawl Starting")
    task_start = datetime.utcnow() #so we can log the time of each crawl
    crawler = BooksCrawler()
    crawler.crawl_books()
    
    #generate a json report 
    await generate_daily_report()  
    logger.info("Daily Crawl task completed")
    

def start_scheduler() -> AsyncIOScheduler:
    global _scheduler
    if _scheduler is not None:
        return _scheduler

    settings = get_settings()
    _scheduler = AsyncIOScheduler(timezone="UTC")
    _scheduler.add_job(
        daily_job,
        trigger=CronTrigger(hour=settings.schedule_cron_hour, minute=settings.schedule_cron_minute),
        id="daily_crawl",
        replace_existing=True,
        misfire_grace_time=3600,
    )
    _scheduler.start()
    logger.info(
        "Scheduler started: daily crawl at %02d:%02d UTC",
        settings.schedule_cron_hour, settings.schedule_cron_minute,
    )
    return _scheduler


def shutdown_scheduler() -> None:
    global _scheduler
    if _scheduler is not None:
        _scheduler.shutdown(wait=False)
        _scheduler = None
