from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class FraudReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    victim_name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    fraud_type = db.Column(db.String(100))
    payment_method = db.Column(db.String(100))
    fraud_description = db.Column(db.Text)
    fraud_phone = db.Column(db.String(20))
    fraud_contact = db.Column(db.String(100))
    fraud_bank = db.Column(db.String(100))
    utr_number = db.Column(db.String(50))

    screenshot_path = db.Column(db.String(200))
    chat_proof_path = db.Column(db.String(200))
    payment_proof_path = db.Column(db.String(200))
    call_recording_path = db.Column(db.String(200))

    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
