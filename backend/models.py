from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FraudReport(db.Model):
    __tablename__ = 'fraud_reports'

    id = db.Column(db.Integer, primary_key=True)
    victim_name = db.Column(db.String(100))
    fraud_type = db.Column(db.String(100))
    fraud_description = db.Column(db.Text)
    fraud_phone = db.Column(db.String(20))
    utr_number = db.Column(db.String(50))
    email = db.Column(db.String(100))
    screenshot_path = db.Column(db.String(200))
    submitted_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "victim_name": self.victim_name,
            "fraud_type": self.fraud_type,
            "fraud_description": self.fraud_description,
            "fraud_phone": self.fraud_phone,
            "utr_number": self.utr_number,
            "email": self.email,
            "screenshot_path": self.screenshot_path,
            "submitted_at": self.submitted_at
        }
