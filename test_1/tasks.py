from test_1.config import create_app
from celery import shared_task
from smartbook.data import Data
from smartbook.llms.poe import Poe
from smartbook.llms.deepseek import Deepseek
from smartbook.booking import Booker
import hashlib
from datetime import datetime

flask_app = create_app()
celery_app = flask_app.extensions["celery"]

# Initialize system components
data_fetcher = Data()
# model = Poe(headless=False)
model = Deepseek()
booker = Booker(model)

SECRET_KEY = "92312se"  # Keep this secret

# Helper: Generate MD5 Signature
def generate_signature(data):
    raw_string = f"{data['system_time'][:10]}|{SECRET_KEY}|{data['user_id'][3:-1]}|{data['sig_version']}"
    return hashlib.md5(raw_string.encode()).hexdigest()

# Async Task
@shared_task(ignore_result=False)
def process_booking_request(requirements: str) -> dict:
    return booker.book(data_fetcher, requirements)
