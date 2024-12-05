from app.celery_app import create_celery
from smartbook.data import Data
from smartbook.llms.poe import Poe
from smartbook.booking import Booker

# Async task
def create_booking_task(celery, booker, data_fetcher):
    @celery.task
    def process_booking_request(requirements):
        """Process the booking asynchronously."""
        return booker.book(data_fetcher, requirements)
    
    return process_booking_request
