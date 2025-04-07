from flask import Blueprint, request, jsonify
from src.services.database import messages_collection
from src.models.message import create_message as create_message_model

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/messages', methods=['POST'])
def add_message():  # Renommé de create_message à add_message
    data = request.get_json()

    # Validate required fields
    required_fields = ['name', 'email', 'subject', 'message']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"Missing or empty field: {field}"}), 400

    # Create the message document
    message = create_message_model(data)  # Utilise la fonction importée renommée

    # Insert the message
    message_id = messages_collection.insert_one(message).inserted_id
    return jsonify({"message": "Message created", "message_id": str(message_id)}), 201

@messages_bp.route('/messages', methods=['GET'])
def get_messages():
    messages = list(messages_collection.find({}, {'_id': 0}))
    return jsonify(messages)