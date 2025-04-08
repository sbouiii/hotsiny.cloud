from datetime import datetime

def create_message(data):
    return {
        'name': data['name'],
        'email': data['email'],
        'subject': data['subject'],
        'message': data['message'],
        'created_at': datetime.now().isoformat()
    }
