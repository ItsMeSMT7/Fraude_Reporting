import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# -------------------- App Initialization --------------------
app = Flask(__name__)
CORS(app)

# -------------------- MongoDB Configuration --------------------
mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
client = MongoClient(mongo_uri)
db = client['fraud_report_api']
report_collection = db['Report']

# -------------------- File Uploads --------------------
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# -------------------- Email Configuration --------------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'fraudreportapi@gmail.com')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'atvg wtta hvcs gxih')

# Initialize Mail object (THIS WAS MISSING!)
mail = Mail(app)

# -------------------- Routes --------------------

@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return jsonify({"message": "Fraud Report API is running", "status": "healthy"}), 200

@app.route('/health', methods=['GET'])
def health_check():
    """Additional health check endpoint"""
    return jsonify({"status": "ok"}), 200

@app.route('/api/report', methods=['POST'])
def submit_report():
    try:
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
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                saved_files[field] = filename
            else:
                saved_files[field] = None

        # Create report document
        report = {
            "victim_name": data.get('victim_name'),
            "email": data.get('email'),
            "fraud_type": data.get('fraud_type'),
            "payment_method": data.get('payment_method'),
            "fraud_description": data.get('fraud_description'),
            "fraud_phone": data.get('fraud_phone'),
            "fraud_contact": data.get('fraud_contact'),
            "fraud_bank": data.get('fraud_bank'),
            "utr_number": data.get('utr_number'),
            "screenshot_path": saved_files.get("screenshot"),
            "chat_proof_path": saved_files.get("chat_proof"),
            "payment_proof_path": saved_files.get("payment_proof"),
            "call_recording_path": saved_files.get("call_recording")
        }

        # Insert into MongoDB
        result = report_collection.insert_one(report)
        
        # Send email confirmation
        if data.get('email'):
            try:
                msg = Message(
                    subject="Fraud Report Received",
                    sender=app.config['MAIL_USERNAME'],
                    recipients=[data.get('email')],
                    body=f"Dear {data.get('victim_name')},\n\nThank you for reporting the fraud. Our team will review your report and forward it to cybercrime authorities.\n\nReport ID: {str(result.inserted_id)}\n\nStay safe,\nFraud Reporting Team"
                )
                mail.send(msg)
            except Exception as e:
                print(f"Error sending email: {e}")

        return jsonify({
            "message": "Report submitted successfully",
            "report_id": str(result.inserted_id)
        }), 200

    except Exception as e:
        print(f"Error in submit_report: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/reports', methods=['GET'])
def get_reports():
    """Get all reports (for admin/testing purposes)"""
    try:
        reports = list(report_collection.find({}, {"_id": 0}))  # Exclude MongoDB _id
        return jsonify({"reports": reports, "count": len(reports)}), 200
    except Exception as e:
        print(f"Error fetching reports: {e}")
        return jsonify({"error": "Internal server error"}), 500

# -------------------- Error Handlers --------------------
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

# -------------------- Main --------------------
if __name__ == '__main__':
    print("Starting Fraud Report API...")
    print("Available endpoints:")
    print("- GET  /              - Health check")
    print("- GET  /health        - Health check")
    print("- POST /api/report    - Submit fraud report")
    print("- GET  /api/reports   - Get all reports")
    app.run(debug=True, host='0.0.0.0', port=5000)