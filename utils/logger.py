import logging
from pathlib import Path
from datetime import datetime
from utils.settings import get_settings

LOG_DIR = Path(__file__).resolve().parent.parent / get_settings().logs_dir
LOG_DIR.mkdir(exist_ok=True)

log_file = LOG_DIR / f"{datetime.today().strftime("%Y-%m-%d")}.log"

logger = logging.getLogger("books_crawler")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def log_book_event(message: str, level: str = "info") -> None:
    getattr(logger, level.lower(), logger.info)(message)


def log_scrape_start(book_url: str) -> None:
    log_book_event(f"Starting scrape for URL: {book_url}")


def log_extraction_step(step: str, value: str | None = None) -> None:
    if value is None:
        log_book_event(f"Extraction step: {step}")
    else:
        log_book_event(f"Extraction step: {step} -> {value}")


def log_scrape_error(book_url: str, error: Exception) -> None:
    log_book_event(f"Error scraping {book_url}: {error}", level="error")
