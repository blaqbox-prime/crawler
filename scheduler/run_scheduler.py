"""
Standalone entrypoint to run the scheduler as its own process, separate
from the API server:

    python -m scheduler.run_scheduler
"""
import asyncio
import os
import signal

from utils.logger import get_logger
from scheduler.scheduler import start_scheduler, daily_job

logger = get_logger("scheduler.run_scheduler")


async def main() -> None:
    if os.getenv("RUN_ON_STARTUP", "false").lower() == "true":
        logger.info("RUN_ON_STARTUP=true - running an immediate crawl")
        await daily_job()

    start_scheduler()

    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop_event.set)

    logger.info("Scheduler process running. Press Ctrl+C to exit.")
    await stop_event.wait()


if __name__ == "__main__":
    asyncio.run(main())
