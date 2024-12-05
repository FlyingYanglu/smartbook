from flask import Flask, request, jsonify
from celery import Celery
import hashlib
from datetime import datetime
from smartbook.data import Data
from smartbook.llms.poe import Poe
from smartbook.booking import Booker

app = Flask(__name__)

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
celery.conf.update(app.config)

# Initialize system components
data_fetcher = Data()
model = Poe(headless=False)
booker = Booker(model)


SECRET_KEY = "92312se"  # Keep this secret

# Helper: Generate MD5 Signature
def generate_signature(data):
    raw_string = f"{data['system_time'][:10]}|{SECRET_KEY}|{data['user_id'][3:-1]}|{data['sig_version']}"
    return hashlib.md5(raw_string.encode()).hexdigest()

# Async Task
@celery.task
def process_booking_request(requirements):
    return booker.book(data_fetcher, requirements)

# Booking Endpoint
@app.route('/book-room', methods=['POST'])
def book_room():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    # Validate signature
    client_signature = data.get('signature')
    expected_signature = generate_signature(data)
    if client_signature != expected_signature:
        return jsonify({"error": "Invalid signature"}), 403

    # Submit async task
    requirements = data.get("requirements", "")
    task = process_booking_request.apply_async(args=[requirements])
    return jsonify({"task_id": task.id}), 202

# Task Status Endpoint
@app.route('/status/<task_id>', methods=['GET'])
def get_task_status(task_id):
    task = process_booking_request.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {"state": task.state, "status": "Pending..."}
    elif task.state != 'FAILURE':
        response = {"state": task.state, "result": task.result}
    else:
        response = {"state": task.state, "status": str(task.info)}  # Exception info
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
