import subprocess
import logging

from worker.celery_app import app

logger = logging.getLogger(__name__)


@app.task
def rebuild_index():
    logger.info("Starting daily FAISS index rebuild...")
    result = subprocess.run(
        ["python", "index/build_index.py"],
        capture_output=True,
        text=True,
        cwd="/app",
    )
    if result.returncode != 0:
        logger.error("Index rebuild failed:\n%s", result.stderr)
    else:
        logger.info("Index rebuild complete:\n%s", result.stdout)
