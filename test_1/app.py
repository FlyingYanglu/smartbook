from test_1.tasks import flask_app, process_booking_request, generate_signature
from celery.result import AsyncResult
from flask import request, jsonify

@flask_app.route('/book-room', methods=['POST'])
def book_room() -> dict[str, object]:
    data = request.json
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    # # Validate signature
    # client_signature = data.get('signature')
    # expected_signature = generate_signature(data)
    # if client_signature != expected_signature:
    #     return jsonify({"error": "Invalid signature"}), 403

    # Submit async task
    requirements = data.get("requirements", "")
    task = process_booking_request.apply_async(args=[requirements])
    return jsonify({"task_id": task.id}), 202

@flask_app.route('/status/<task_id>', methods=['GET'])
def get_task_status(task_id: str) -> dict[str, object]:
    task = AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {"state": task.state, "status": "Pending..."}
    elif task.state != 'FAILURE':
        response = {"state": task.state, "result": task.result}
    else:
        response = {"state": task.state, "status": str(task.info)}  # Exception info
    return jsonify(response)

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=5000, debug=True)
