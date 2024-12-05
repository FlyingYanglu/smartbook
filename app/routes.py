from flask import request, jsonify
from app.helpers import generate_signature
from app.booking import create_booking_task

def register_routes(app, celery):
    """Register Flask routes."""
    # Initialize booking task
    from app import data_fetcher, model, booker
    process_booking_request = create_booking_task(celery, booker, data_fetcher)

    @app.route('/book-room', methods=['POST'])
    def book_room():
        """Handle room booking requests."""
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

    @app.route('/status/<task_id>', methods=['GET'])
    def get_task_status(task_id):
        """Get the status of a Celery task."""
        task = process_booking_request.AsyncResult(task_id)
        if task.state == 'PENDING':
            response = {"state": task.state, "status": "Pending..."}
        elif task.state != 'FAILURE':
            response = {"state": task.state, "result": task.result}
        else:
            response = {"state": task.state, "status": str(task.info)}  # Exception info
        return jsonify(response)
