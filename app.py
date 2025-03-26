from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
from datetime import datetime

app = Flask(__name__)

# Load environment variables
load_dotenv()
uri = os.getenv('MONGO_URI')
client = MongoClient(uri, server_api=ServerApi('1'))

# Connect to the database and create/select the "messages" collection
db = client['hosting_platform']
messages_collection = db['messages']

# Test MongoDB connection
try:
    client.admin.command('ping')
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")

# Route to create a new message (POST)
@app.route('/api/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'email', 'subject', 'message']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"Missing or empty field: {field}"}), 400

    # Create the message document
    message = {
        'name': data['name'],
        'email': data['email'],
        'subject': data['subject'],
        'message': data['message'],
        'created_at': datetime.now().isoformat()
    }

    # Insert the message into the "messages" collection
    message_id = messages_collection.insert_one(message).inserted_id
    return jsonify({"message": "Message created", "message_id": str(message_id)}), 201

# Route to get all messages (GET)
@app.route('/api/messages', methods=['GET'])
def get_messages():
    messages = list(messages_collection.find({}, {'_id': 0}))  # Exclude the '_id' field from the response
    return jsonify(messages)

if __name__ == '__main__':
    app.run(debug=True, port=5000)