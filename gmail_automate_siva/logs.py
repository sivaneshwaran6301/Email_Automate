import logging
import sys
import io

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(filename)s:%(lineno)d | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler("project.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
# Ensure stdout uses UTF-8 encoding for console output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
logger = logging.getLogger(__name__) 