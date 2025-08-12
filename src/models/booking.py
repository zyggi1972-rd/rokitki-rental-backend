from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    guest_name = db.Column(db.String(100), nullable=False)
    guest_email = db.Column(db.String(120), nullable=False)
    guest_phone = db.Column(db.String(20), nullable=False)
    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)

    def __repr__(self):
        return f'<Booking {self.id} - {self.guest_name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'property_id': self.property_id,
            'guest_name': self.guest_name,
            'guest_email': self.guest_email,
            'guest_phone': self.guest_phone,
            'check_in': self.check_in.isoformat() if self.check_in else None,
            'check_out': self.check_out.isoformat() if self.check_out else None,
            'total_price': self.total_price,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'notes': self.notes
        }

class Availability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('property.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    price_override = db.Column(db.Float)  # Special pricing for specific dates
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Unique constraint to prevent duplicate entries for same property and date
    __table_args__ = (db.UniqueConstraint('property_id', 'date', name='unique_property_date'),)

    def __repr__(self):
        return f'<Availability {self.property_id} - {self.date}>'

    def to_dict(self):
        return {
            'id': self.id,
            'property_id': self.property_id,
            'date': self.date.isoformat() if self.date else None,
            'is_available': self.is_available,
            'price_override': self.price_override,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

