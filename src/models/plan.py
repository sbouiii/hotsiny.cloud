from datetime import datetime

def create_plan(data):
    return {
        'name': data['name'],
        'description': data['description'],
        'monthlyPrice': data['monthlyPrice'],
        'annualPrice': data['annualPrice'],
        'features': data['features'],
        'recommended': data['recommended'],
        'created_at': datetime.now().isoformat()

    }
