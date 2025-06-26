from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import ChatMessage, User, db
from utils.chatbot_logic import ChatbotProcessor
import uuid
from datetime import datetime

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route('/message', methods=['POST'])
@jwt_required()
def process_message():
    """Process chatbot message and return response"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data['message'].strip()
        session_id = data.get('session_id', str(uuid.uuid4()))
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Initialize chatbot processor
        chatbot = ChatbotProcessor()
        
        # Process the message
        response_data = chatbot.process_message(user_message, current_user_id)
        
        # Save chat message to database
        chat_message = ChatMessage(
            user_id=current_user_id,
            message=user_message,
            response=response_data['response'],
            intent=response_data.get('intent'),
            session_id=session_id
        )
        
        if response_data.get('entities'):
            chat_message.set_entities(response_data['entities'])
        
        db.session.add(chat_message)
        db.session.commit()
        
        return jsonify({
            'message_id': chat_message.id,
            'user_message': user_message,
            'bot_response': response_data['response'],
            'intent': response_data.get('intent'),
            'entities': response_data.get('entities', {}),
            'products': response_data.get('products', []),
            'session_id': session_id,
            'timestamp': chat_message.timestamp.isoformat()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to process message', 'details': str(e)}), 500

@chatbot_bp.route('/history', methods=['GET'])
@jwt_required()
def get_chat_history():
    """Get user's chat history"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        session_id = request.args.get('session_id')
        
        per_page = min(per_page, 100)
        
        # Build query
        query = ChatMessage.query.filter(ChatMessage.user_id == current_user_id)
        
        if session_id:
            query = query.filter(ChatMessage.session_id == session_id)
        
        # Order by timestamp (newest first)
        query = query.order_by(ChatMessage.timestamp.desc())
        
        # Paginate results
        messages = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'chat_history': [message.to_dict() for message in messages.items],
            'pagination': {
                'page': messages.page,
                'pages': messages.pages,
                'per_page': messages.per_page,
                'total': messages.total,
                'has_next': messages.has_next,
                'has_prev': messages.has_prev
            },
            'session_id': session_id
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get chat history', 'details': str(e)}), 500

@chatbot_bp.route('/sessions', methods=['GET'])
@jwt_required()
def get_chat_sessions():
    """Get user's chat sessions"""
    try:
        current_user_id = get_jwt_identity()
        
        # Get distinct session IDs with message counts and latest timestamps
        sessions = db.session.query(
            ChatMessage.session_id,
            db.func.count(ChatMessage.id).label('message_count'),
            db.func.max(ChatMessage.timestamp).label('last_message'),
            db.func.min(ChatMessage.timestamp).label('first_message')
        ).filter(
            ChatMessage.user_id == current_user_id
        ).group_by(
            ChatMessage.session_id
        ).order_by(
            db.func.max(ChatMessage.timestamp).desc()
        ).all()
        
        session_list = []
        for session in sessions:
            session_list.append({
                'session_id': session.session_id,
                'message_count': session.message_count,
                'last_message': session.last_message.isoformat(),
                'first_message': session.first_message.isoformat()
            })
        
        return jsonify({
            'sessions': session_list,
            'total_sessions': len(session_list)
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get chat sessions', 'details': str(e)}), 500

@chatbot_bp.route('/clear-history', methods=['DELETE'])
@jwt_required()
def clear_chat_history():
    """Clear user's chat history"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json() or {}
        session_id = data.get('session_id')
        
        # Build query
        query = ChatMessage.query.filter(ChatMessage.user_id == current_user_id)
        
        if session_id:
            query = query.filter(ChatMessage.session_id == session_id)
            message = f"Chat history cleared for session {session_id}"
        else:
            message = "All chat history cleared"
        
        # Delete messages
        deleted_count = query.delete()
        db.session.commit()
        
        return jsonify({
            'message': message,
            'deleted_count': deleted_count
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to clear chat history', 'details': str(e)}), 500

@chatbot_bp.route('/message/<int:message_id>', methods=['DELETE'])
@jwt_required()
def delete_message(message_id):
    """Delete a specific chat message"""
    try:
        current_user_id = get_jwt_identity()
        
        message = ChatMessage.query.filter(
            ChatMessage.id == message_id,
            ChatMessage.user_id == current_user_id
        ).first()
        
        if not message:
            return jsonify({'error': 'Message not found'}), 404
        
        db.session.delete(message)
        db.session.commit()
        
        return jsonify({
            'message': 'Chat message deleted successfully',
            'deleted_message_id': message_id
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to delete message', 'details': str(e)}), 500

@chatbot_bp.route('/feedback', methods=['POST'])
@jwt_required()
def submit_feedback():
    """Submit feedback for a chat response"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'message_id' not in data or 'rating' not in data:
            return jsonify({'error': 'Message ID and rating are required'}), 400
        
        message_id = data['message_id']
        rating = data['rating']  # 1-5 scale
        feedback_text = data.get('feedback', '')
        
        # Validate rating
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        
        # Find the message
        message = ChatMessage.query.filter(
            ChatMessage.id == message_id,
            ChatMessage.user_id == current_user_id
        ).first()
        
        if not message:
            return jsonify({'error': 'Message not found'}), 404
        
        # Store feedback in entities (for simplicity)
        entities = message.get_entities()
        entities['feedback'] = {
            'rating': rating,
            'text': feedback_text,
            'timestamp': datetime.utcnow().isoformat()
        }
        message.set_entities(entities)
        
        db.session.commit()
        
        return jsonify({
            'message': 'Feedback submitted successfully',
            'message_id': message_id,
            'rating': rating
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to submit feedback', 'details': str(e)}), 500

@chatbot_bp.route('/quick-actions', methods=['GET'])
def get_quick_actions():
    """Get quick action suggestions for the chatbot"""
    try:
        quick_actions = [
            {
                'text': 'Show me laptops under $1000',
                'intent': 'product_search',
                'description': 'Search for affordable laptops'
            },
            {
                'text': 'What are the latest smartphones?',
                'intent': 'product_search',
                'description': 'Browse newest smartphones'
            },
            {
                'text': 'I need running shoes',
                'intent': 'product_search',
                'description': 'Find athletic footwear'
            },
            {
                'text': 'Show me top rated products',
                'intent': 'recommendation',
                'description': 'Browse best-rated items'
            },
            {
                'text': 'What books do you recommend?',
                'intent': 'recommendation',
                'description': 'Get book recommendations'
            },
            {
                'text': 'Help me find a gift under $50',
                'intent': 'product_search',
                'description': 'Find affordable gifts'
            }
        ]
        
        return jsonify({
            'quick_actions': quick_actions
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'Failed to get quick actions', 'details': str(e)}), 500
