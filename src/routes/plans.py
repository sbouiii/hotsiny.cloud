from flask import Blueprint, request, jsonify
from src.services.database import db
from src.models.plan import create_plan
from bson import ObjectId

plans_collection = db['plans']
plans_bp = Blueprint('plans', __name__)

@plans_bp.route('/plans', methods=['POST'])
def create_plan_route():
    data = request.get_json()

    # Validate required fields
    required_fields = ['name', 'description', 'monthlyPrice', 'annualPrice', 'features', 'recommended']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"Missing or empty field: {field}"}), 400

    # Create the plan document
    plan = create_plan(data)

    # Insert the plan
    plan_id = plans_collection.insert_one(plan).inserted_id
    return jsonify({"message": "Plan created", "plan_id": str(plan_id)}), 201

@plans_bp.route('/plans', methods=['GET'])
def get_plans():
    plans = list(plans_collection.find({}))
    # Convertir l'_id en chaîne pour chaque plan
    for plan in plans:
        plan['_id'] = str(plan['_id'])
    return jsonify(plans)