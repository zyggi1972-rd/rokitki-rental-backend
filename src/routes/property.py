from flask import Blueprint, jsonify, request
from src.models.user import db
from src.models.property import Property, PropertyImage
from datetime import datetime
import json

property_bp = Blueprint('property', __name__)

@property_bp.route('/properties', methods=['GET'])
def get_properties():
    """Get all active properties with optional filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    
    # Filtering parameters
    max_guests = request.args.get('max_guests', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    featured_only = request.args.get('featured', type=bool)
    
    query = Property.query.filter_by(is_active=True)
    
    if max_guests:
        query = query.filter(Property.max_guests >= max_guests)
    if min_price:
        query = query.filter(Property.price_per_night >= min_price)
    if max_price:
        query = query.filter(Property.price_per_night <= max_price)
    if featured_only:
        query = query.filter_by(is_featured=True)
    
    # Order by featured first, then by creation date
    query = query.order_by(Property.is_featured.desc(), Property.created_at.desc())
    
    properties = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'properties': [prop.to_dict() for prop in properties.items],
        'total': properties.total,
        'pages': properties.pages,
        'current_page': page,
        'per_page': per_page
    })

@property_bp.route('/properties/<int:property_id>', methods=['GET'])
def get_property(property_id):
    """Get single property details"""
    property = Property.query.get_or_404(property_id)
    return jsonify(property.to_dict())

@property_bp.route('/properties', methods=['POST'])
def create_property():
    """Create new property listing"""
    data = request.json
    
    try:
        property = Property(
            user_id=data['user_id'],
            title=data['title'],
            description=data['description'],
            price_per_night=data['price_per_night'],
            max_guests=data['max_guests'],
            bedrooms=data['bedrooms'],
            bathrooms=data['bathrooms'],
            amenities=json.dumps(data.get('amenities', [])),
            address=data['address'],
            latitude=data.get('latitude'),
            longitude=data.get('longitude')
        )
        
        db.session.add(property)
        db.session.flush()  # Get the property ID
        
        # Add images if provided
        if 'images' in data:
            for i, image_data in enumerate(data['images']):
                image = PropertyImage(
                    property_id=property.id,
                    image_url=image_data['url'],
                    is_main=image_data.get('is_main', i == 0),
                    order=i
                )
                db.session.add(image)
        
        db.session.commit()
        return jsonify(property.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@property_bp.route('/properties/<int:property_id>', methods=['PUT'])
def update_property(property_id):
    """Update property details"""
    property = Property.query.get_or_404(property_id)
    data = request.json
    
    try:
        # Update basic fields
        for field in ['title', 'description', 'price_per_night', 'max_guests', 
                     'bedrooms', 'bathrooms', 'address', 'latitude', 'longitude']:
            if field in data:
                setattr(property, field, data[field])
        
        if 'amenities' in data:
            property.amenities = json.dumps(data['amenities'])
        
        # Update images if provided
        if 'images' in data:
            # Remove existing images
            PropertyImage.query.filter_by(property_id=property_id).delete()
            
            # Add new images
            for i, image_data in enumerate(data['images']):
                image = PropertyImage(
                    property_id=property.id,
                    image_url=image_data['url'],
                    is_main=image_data.get('is_main', i == 0),
                    order=i
                )
                db.session.add(image)
        
        db.session.commit()
        return jsonify(property.to_dict())
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@property_bp.route('/properties/<int:property_id>', methods=['DELETE'])
def delete_property(property_id):
    """Soft delete property (set inactive)"""
    property = Property.query.get_or_404(property_id)
    property.is_active = False
    db.session.commit()
    return '', 204

@property_bp.route('/users/<int:user_id>/properties', methods=['GET'])
def get_user_properties(user_id):
    """Get all properties for a specific user"""
    properties = Property.query.filter_by(user_id=user_id).order_by(Property.created_at.desc()).all()
    return jsonify([prop.to_dict() for prop in properties])

@property_bp.route('/properties/search', methods=['POST'])
def search_properties():
    """Advanced property search"""
    data = request.json
    
    query = Property.query.filter_by(is_active=True)
    
    # Date availability check would go here
    # For now, just basic filtering
    
    if 'location' in data and data['location']:
        query = query.filter(Property.address.contains(data['location']))
    
    if 'guests' in data and data['guests']:
        query = query.filter(Property.max_guests >= data['guests'])
    
    if 'min_price' in data and data['min_price']:
        query = query.filter(Property.price_per_night >= data['min_price'])
    
    if 'max_price' in data and data['max_price']:
        query = query.filter(Property.price_per_night <= data['max_price'])
    
    properties = query.order_by(Property.is_featured.desc(), Property.created_at.desc()).all()
    
    return jsonify([prop.to_dict() for prop in properties])

