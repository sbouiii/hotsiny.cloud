from flask import Blueprint, request, jsonify, current_app
from flask_mail import Message
from src.services.database import messages_collection
from src.models.message import create_message as create_message_document
from src.services.mail import mail  # Importer mail depuis le nouveau module

messages_bp = Blueprint('messages', __name__)

@messages_bp.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()

    # Validate required fields
    required_fields = ['name', 'email', 'subject', 'message']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"Missing or empty field: {field}"}), 400

    # Create the message document
    message = create_message_document(data)

    # Insert the message
    message_id = messages_collection.insert_one(message).inserted_id

    # Send an email to the client
    try:
        # HTML template for the email
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 32px; background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <div style="text-align: center; margin-bottom: 32px;">
                <svg xmlns="http://www.w3.org/2000/svg" style="width: 48px; height: 48px; color: #a9866c;" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M2 5a2 2 0 012-2h12a2 2 0 012 2v10a2 2 0 01-2 2H4a2 2 0 01-2-2V5zm3.293 1.293a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 01-1.414-1.414L7.586 10 5.293 7.707a1 1 0 010-1.414zM11 12a1 1 0 100 2h3a1 1 0 100-2h-3z" />
                </svg>
                <h1 style="color: #7d5b44; font-size: 28px; margin: 24px 0 16px;">Welcome to Hostiny!</h1>
                <div style="width: 60px; height: 4px; background-color: #a9866c; margin: 0 auto;"></div>
            </div>

            <p style="color: #574035; font-size: 16px; line-height: 1.6;">Hello {data['name']},</p>
            <p style="color: #574035; font-size: 16px; line-height: 1.6;">Thank you for reaching out! We have received your message:</p>
            <blockquote style="color: #574035; font-size: 16px; line-height: 1.6; background-color: #f9f7f5; padding: 16px; border-left: 4px solid #a9866c; border-radius: 8px;">{data['message']}</blockquote>
            <p style="color: #574035; font-size: 16px; line-height: 1.6;">We will get back to you shortly.</p>

            <div style="text-align: center; margin: 32px 0;">
                <a href="https://hostiny.cloud/dashboard" style="background-color: #a9866c; color: white; padding: 12px 32px; text-decoration: none; border-radius: 6px; font-weight: 500;">Visit Dashboard</a>
            </div>

            <p style="color: #574035; font-size: 16px; line-height: 1.6; text-align: center;">Need help? Our support team is always here to assist you.</p>

            <div style="border-top: 1px solid #e3d9ce; margin-top: 32px; padding-top: 32px; text-align: center;">
                <p style="color: #7d5b44; margin: 0;">Best regards,<br><strong>The Hostiny Team</strong></p>
            </div>
        </div>
        """

        msg = Message(
            subject="Thank you for your message!",
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            recipients=[data['email']],  # Email du client
            html=html_content  # Contenu HTML
        )
        mail.send(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")

    return jsonify({"message": "Message created and email sent", "message_id": str(message_id)}), 201

@messages_bp.route('/messages', methods=['GET'])
def get_messages():
    messages = list(messages_collection.find({}, {'_id': 0}))
    return jsonify(messages)