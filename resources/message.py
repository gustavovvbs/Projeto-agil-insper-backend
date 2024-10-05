from flask import Blueprint, request, jsonify
from app import mongo
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.objectid import ObjectId
from datetime import datetime

message_bp = Blueprint('message', __name__)

@message_bp.route('/messages', methods=['POST'])
@jwt_required()
def send_message():
    data = request.get_json()
    required_fields = ['receiver_id', 'content']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Campos obrigatórios faltando"}), 400

    message = {
        "sender_id": ObjectId(get_jwt_identity()),
        "receiver_id": ObjectId(data['receiver_id']),
        "content": data['content'],
        "timestamp": datetime.utcnow(),
    }

    mongo.db.messages.insert_one(message)
    return jsonify({"message": "Mensagem enviada com sucesso"}), 201
