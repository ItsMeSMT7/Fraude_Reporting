import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from models import db, FraudReport  # ✅ Make sure models.py uses the same db

# -------------------- App Initialization --------------------

app = Flask(__name__)
CORS(app)

# -------------------- Configuration --------------------

# Database (PostgreSQL)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Admin%401234@localhost:5432/fraud_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 📌 2. Initialize db after app config
db = SQLAlchemy(app)

# File Uploads
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Email Config (Gmail SMTP + App Password)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'fraudreportapi@gmail.com'
app.config['MAIL_PASSWORD'] = 'atvg wtta hvcs gxih'  # 🔐 App Password only

# -------------------- Extensions --------------------

db.init_app(app)
mail = Mail(app)

# -------------------- Routes --------------------

@app.route('/api/report', methods=['POST'])
def submit_report():
    data = request.form.to_dict()

    # File upload logic...
    uploaded_files = {
        "screenshot": request.files.get('screenshot'),
        "chat_proof": request.files.get('chat_proof'),
        "payment_proof": request.files.get('payment_proof'),
        "call_recording": request.files.get('call_recording')
    }

    saved_files = {}
    for field, file in uploaded_files.items():
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            saved_files[field] = filename
        else:
            saved_files[field] = None

    # ✅ This is where your line goes:
    report = FraudReport(
        victim_name=data.get('victim_name'),
        email=data.get('email'),
        fraud_type=data.get('fraud_type'),
        payment_method=data.get('payment_method'),
        fraud_description=data.get('fraud_description'),
        fraud_phone=data.get('fraud_phone'),
        fraud_contact=data.get('fraud_contact'),
        fraud_bank=data.get('fraud_bank'),
        utr_number=data.get('utr_number'),
        screenshot_path=saved_files.get("screenshot"),
        chat_proof_path=saved_files.get("chat_proof"),
        payment_proof_path=saved_files.get("payment_proof"),
        call_recording_path=saved_files.get("call_recording")
    )

    # Save to DB
    db.session.add(report)
    db.session.commit()


    # Email Confirmation
    if data.get('email'):
        try:
            msg = Message(
                subject="Fraud Report Received",
                sender=app.config['MAIL_USERNAME'],
                recipients=[data.get('email')],
                body=f"Dear {data.get('victim_name')},\n\nThank you for reporting the fraud. Our team will review your report and forward it to cybercrime authorities.\n\nStay safe,\nFraud Reporting Team"
            )
            mail.send(msg)
        except Exception as e:
            print("Error sending email:", e)

    return jsonify({"message": "Report submitted successfully"}), 200

# Serve uploaded files
@app.route('/uploads/<filename>')
def serve_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


#----------------retrieves and displays all reports----------------
@app.route('/api/reports', methods=['GET'])
def get_all_reports():
    reports = FraudReport.query.all()
    return jsonify([r.to_dict() for r in reports])


# -------------------- Main --------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
