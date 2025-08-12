from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price_per_night = db.Column(db.Float, nullable=False)
    max_guests = db.Column(db.Integer, nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Integer, nullable=False)
    amenities = db.Column(db.Text)  # JSON string of amenities
    address = db.Column(db.String(300), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('properties', lazy=True))
    images = db.relationship('PropertyImage', backref='property', lazy=True, cascade='all, delete-orphan')
    bookings = db.relationship('Booking', backref='property', lazy=True)

    def __repr__(self):
        return f'<Property {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'price_per_night': self.price_per_night,
            'max_guests': self.max_guests,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'amenities': self.amenities,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active,
            'is_featured': self.is_featured,
            'images': [img.to_dict() for img in self.images],
            'user': self.user.to_dict() if self.user else None
        }

class PropertyImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    is_main = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<PropertyImage {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'property_id': self.property_id,
            'image_url': self.image_url,
            'is_main': self.is_main,
            'order': self.order,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

