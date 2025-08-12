from flask import Blueprint, jsonify, request, session
from src.models.user import db
from src.models.payment import Payment, ListingPlan
from datetime import datetime

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/listing-plans', methods=['GET'])
def get_listing_plans():
    """Get all available listing plans"""
    plans = ListingPlan.query.filter_by(is_active=True).order_by(ListingPlan.price).all()
    return jsonify([plan.to_dict() for plan in plans])

@payment_bp.route('/payments', methods=['POST'])
def create_payment():
    """Create new payment for listing"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.json
    
    try:
        payment = Payment(
            user_id=session['user_id'],
            property_id=data.get('property_id'),
            amount=data['amount'],
            payment_method=data['payment_method'],
            payment_type=data['payment_type'],
            description=data.get('description', '')
        )
        
        db.session.add(payment)
        db.session.commit()
        
        # Here you would integrate with actual payment providers
        # For now, we'll simulate payment processing
        
        return jsonify({
            'payment_id': payment.id,
            'status': 'pending',
            'redirect_url': f'/payment/process/{payment.id}'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@payment_bp.route('/payments/<int:payment_id>/confirm', methods=['POST'])
def confirm_payment(payment_id):
    """Confirm payment completion (webhook endpoint)"""
    payment = Payment.query.get_or_404(payment_id)
    data = request.json
    
    try:
        payment.status = 'completed'
        payment.transaction_id = data.get('transaction_id')
        payment.completed_at = datetime.utcnow()
        
        # If this is a listing fee, activate the property
        if payment.payment_type == 'listing_fee' and payment.property_id:
            from src.models.property import Property
            property = Property.query.get(payment.property_id)
            if property:
                property.is_active = True
                
        # If this is for featured listing, mark property as featured
        elif payment.payment_type == 'featured_listing' and payment.property_id:
            from src.models.property import Property
            property = Property.query.get(payment.property_id)
            if property:
                property.is_featured = True
        
        db.session.commit()
        
        return jsonify({
            'message': 'Payment confirmed',
            'payment': payment.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@payment_bp.route('/payments/<int:payment_id>/cancel', methods=['POST'])
def cancel_payment(payment_id):
    """Cancel payment"""
    payment = Payment.query.get_or_404(payment_id)
    
    payment.status = 'failed'
    db.session.commit()
    
    return jsonify({
        'message': 'Payment cancelled',
        'payment': payment.to_dict()
    })

@payment_bp.route('/users/<int:user_id>/payments', methods=['GET'])
def get_user_payments(user_id):
    """Get payment history for user"""
    if 'user_id' not in session or session['user_id'] != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    payments = Payment.query.filter_by(user_id=user_id).order_by(Payment.created_at.desc()).all()
    return jsonify([payment.to_dict() for payment in payments])

# Simulated payment processing endpoints
@payment_bp.route('/payment/blik', methods=['POST'])
def process_blik_payment():
    """Simulate BLIK payment processing"""
    data = request.json
    
    # In real implementation, this would integrate with Polish payment gateway
    # like Przelewy24, PayU, or Tpay
    
    return jsonify({
        'status': 'success',
        'transaction_id': f'BLIK_{datetime.utcnow().strftime("%Y%m%d%H%M%S")}',
        'message': 'BLIK payment processed successfully'
    })

@payment_bp.route('/payment/paypal', methods=['POST'])
def process_paypal_payment():
    """Simulate PayPal payment processing"""
    data = request.json
    
    # In real implementation, this would use PayPal SDK
    
    return jsonify({
        'status': 'success',
        'transaction_id': f'PP_{datetime.utcnow().strftime("%Y%m%d%H%M%S")}',
        'message': 'PayPal payment processed successfully'
    })

@payment_bp.route('/payment/stripe', methods=['POST'])
def process_stripe_payment():
    """Simulate Stripe payment processing"""
    data = request.json
    
    # In real implementation, this would use Stripe SDK
    
    return jsonify({
        'status': 'success',
        'transaction_id': f'STRIPE_{datetime.utcnow().strftime("%Y%m%d%H%M%S")}',
        'message': 'Card payment processed successfully'
    })

