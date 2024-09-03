from app import db
from datetime import datetime

class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    property_type = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    postcode = db.Column(db.String(20), nullable=False)
    value = db.Column(db.Float, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Property {self.title} - {self.property_type}>"

    @staticmethod
    def allowed_property_types():
        return ["Terraced", "Semi-Detached", "Detached", "Bungalow", "Land", "Flat"]
