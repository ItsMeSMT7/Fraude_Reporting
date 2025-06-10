import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# -------------------- App Initialization --------------------
app = Flask(__name__)
CORS(app)

# -------------------- Configuration --------------------
# Database (PostgreSQL)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/fraud_db')  # Replace with your own environment variable
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 📌 Initialize db after app config
db = SQLAlchemy(app)

# File Uploads
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Email Config (Gmail SMTP + App Password)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')  # Get from .env
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Get from .env

# -------------------- Extensions --------------------
mail = Mail(app)

# -------------------- Routes --------------------
@app.route('/api/report', methods=['POST'])
def submit_report():
    data = request.form.to_dict()

    # File upload logic
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

    # Create a report instance
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

    # Send email confirmation
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


@app.route('/uploads/<filename>')
def serve_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Retrieve all reports
@app.route('/api/reports', methods=['GET'])
def get_all_reports():
    reports = FraudReport.query.all()
    return jsonify([r.to_dict() for r in reports])

# -------------------- Main --------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables in DB if they don't exist
    app.run(debug=True)  # Run Flask in debug mode
