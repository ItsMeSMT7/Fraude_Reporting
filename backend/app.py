import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
from models import db, FraudReport

app = Flask(__name__)
CORS(app)

# Config
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Admin@1234@localhost:5432/fraud_db' # <-- update these
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Admin%401234@localhost:5432/fraud_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# API: Submit Fraud Report (with file)
@app.route('/api/report', methods=['POST'])
def submit_report():
    data = request.form.to_dict()
    file = request.files.get('screenshot')

    filename = None
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    report = FraudReport(
        victim_name=data.get('victim_name'),
        fraud_type=data.get('fraud_type'),
        fraud_description=data.get('fraud_description'),
        fraud_phone=data.get('fraud_phone'),
        utr_number=data.get('utr_number'),
        email=data.get('email'),
        screenshot_path=filename
    )

    db.session.add(report)
    db.session.commit()
    return jsonify({"message": "Report submitted successfully"}), 200

# API: Get All Reports
@app.route('/api/reports', methods=['GET'])
def get_reports():
    reports = FraudReport.query.order_by(FraudReport.submitted_at.desc()).all()
    return jsonify([r.to_dict() for r in reports])

# Serve uploaded file
@app.route('/uploads/<filename>')
def serve_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# App Start
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
