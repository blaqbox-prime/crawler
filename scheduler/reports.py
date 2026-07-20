import json
import os
from datetime import datetime, timezone
from typing import List
from utils.logger import get_logger, get_settings


logger = get_logger("scheduler.reports")


async def fetch_changes_since(since: datetime) -> List[dict]:
    cursor = Changes.find({"timestamp": {"$gte": since}}).sort("timestamp", 1)
    changes = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        changes.append(doc)
    return changes

def _write_json(changes: List[dict], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(changes, f, indent=2, default=str)

async def generate_daily_report(since: datetime, fmt: str = "json") -> str:
    """Write the change report to disk and return its path."""
    settings = get_settings()
    os.makedirs(settings.report_dir, exist_ok=True)

    changes = await fetch_changes_since(since)
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    filename = f"change_report_{date_str}.{fmt}"
    path = os.path.join(settings.report_dir, filename)

    _write_json(changes, path)

    logger.info("Wrote change report with %d entries to %s", len(changes), path)
    return path
