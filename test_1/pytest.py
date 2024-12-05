import pytest
import requests
import hashlib
from datetime import datetime
import time

BASE_URL = "http://localhost:5000"
SECRET_KEY = "92312se"  # Same as in your code

# Helper: Generate MD5 Signature
def generate_signature(data):
    raw_string = f"{data['system_time'][:10]}|{SECRET_KEY}|{data['user_id'][3:-1]}|{data['sig_version']}"
    return hashlib.md5(raw_string.encode()).hexdigest()

@pytest.fixture
def booking_data():
    system_time = datetime.utcnow().isoformat()
    data = {
        "user_id": "user1234",
        "system_time": system_time,
        "sig_version": "1",
        "requirements": "2 beds, near downtown",
    }
    data["signature"] = generate_signature(data)
    return data

@pytest.fixture
def task_id(booking_data):
    response = requests.post(f"{BASE_URL}/book-room", json=booking_data)
    assert response.status_code == 202
    response_json = response.json()
    assert "task_id" in response_json
    return response_json["task_id"]

def test_book_room(task_id):
    # Validate that the task_id is properly generated
    assert len(task_id) > 0

def test_get_task_status(task_id):
    status_url = f"{BASE_URL}/status/{task_id}"

    # Poll the task status
    for _ in range(10):  # Retry 10 times
        response = requests.get(status_url)
        assert response.status_code == 200
        response_json = response.json()

        if response_json["state"] == "SUCCESS":
            assert "result" in response_json
            print("Task Result:", response_json["result"])
            break
        elif response_json["state"] == "FAILURE":
            pytest.fail(f"Task failed with error: {response_json['status']}")
        else:
            print("Task is still pending...")
            time.sleep(2)