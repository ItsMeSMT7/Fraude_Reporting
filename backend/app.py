import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from models import db, FraudReport

app = Flask(__name__)
CORS(app)

# -------------------- Configuration --------------------

# PostgreSQL Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Admin%401234@localhost:5432/fraud_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Email configuration (Flask-Mail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'fraudreportapi@gmail.com'       # 🔁 Change this
app.config['MAIL_PASSWORD'] = 'atvg wtta hvcs gxih'          # 🔁 Use Gmail App Password

# -------------------- Initialize Extensions --------------------

db.init_app(app)
mail = Mail(app)

# -------------------- API Routes --------------------

@app.route('/api/report', methods=['POST'])
def submit_report():
    data = request.form.to_dict()

    uploaded_files = {
        "screenshot": request.files.get('screenshot'),
        "chat_proof": request.files.get('chat_proof'),
        "payment_proof": request.files.get('payment_proof'),
        "call_recording": request.files.get('call_recording')
    }

    saved_files = {}
    for field_name, file in uploaded_files.items():
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            saved_files[field_name] = filename
        else:
            saved_files[field_name] = None

    report = FraudReport(
        victim_name=data.get('victim_name'),
        fraud_type=data.get('fraud_type'),
        fraud_description=data.get('fraud_description'),
        fraud_phone=data.get('fraud_phone'),
        utr_number=data.get('utr_number'),
        email=data.get('email'),
        fraud_contact=data.get('fraud_contact'),
        fraud_bank=data.get('fraud_bank'),
        payment_method=data.get('payment_method'),
        screenshot_path=saved_files.get("screenshot"),
        chat_proof_path=saved_files.get("chat_proof"),
        payment_proof_path=saved_files.get("payment_proof"),
        call_recording_path=saved_files.get("call_recording")
    )

    db.session.add(report)
    db.session.commit()

    # Send email confirmation
    if data.get('email'):
        try:
            msg = Message(
                subject="Fraud Report Received",
                sender=app.config['MAIL_USERNAME'],
                recipients=[data.get('email')],
                body=f"Dear {data.get('victim_name')},\n\nThank you for reporting the fraud. Our team will review the details and take necessary action.\n\nRegards,\nFraud Detection Team"
            )
            mail.send(msg)
        except Exception as e:
            print("Email send error:", e)

    return jsonify({"message": "Report submitted successfully"}), 200

# Serve uploaded files
@app.route('/uploads/<filename>')
def serve_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# -------------------- App Entry Point --------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
