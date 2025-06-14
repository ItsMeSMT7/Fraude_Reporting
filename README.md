# 🛡️ Fraud Reporting and Detection Platform

The **Fraud Reporting and Detection Platform** provides a secure and efficient way for users to report fraudulent activities with detailed evidence. It aims to simplify fraud reporting and accelerate the investigation process by forwarding submitted reports to the concerned authorities in real time.

---

## 🚀 Overview

This platform enables victims of fraud to:

- Submit a detailed report of the incident
- Upload supporting evidence (screenshots, payment proofs, chat logs, call recordings)
- Automatically notify authorities and receive email confirmation of submission
- Store all data securely in MongoDB for future retrieval

---

## 🔑 Key Features

- ✅ **User-Friendly Interface** – Clean and intuitive design for ease of use
- 📎 **Multiple File Uploads** – Submit images, PDFs, audio, and more
- 📧 **Email Confirmation** – Confirmation sent to the reporter’s email
- ⏱ **Real-Time Submission** – Instant data storage and notification
- 🔐 **Secure Data Handling** – Stored securely in MongoDB
- 📡 **RESTful API Support** – Flask backend with structured API endpoints

---

## 🧰 Tech Stack

| Layer     | Technology               |
|-----------|--------------------------|
| Frontend  | HTML, CSS, JavaScript (React) |
| Backend   | Python (Flask)           |
| Database  | MongoDB (Local/Cloud)    |
| Email     | Gmail SMTP via Flask-Mail |
| Hosting   | Local / AWS / Heroku / Netlify |

---

## 🛠️ How It Works

1. **User Submission**: Victims fill out the fraud report form.
2. **File Upload**: Upload screenshots, chat logs, payment proof, or call recordings.
3. **Backend Processing**: Flask processes and stores data in MongoDB.
4. **Confirmation Email**: User receives an automated email.
5. **Authority Notification**: Concerned officials are notified with report data.

---

## 📡 API Endpoints

### 🔸 `POST /api/report`

- **Description**: Submit a fraud report
- **Fields**:
  - `victim_name`, `email`, `fraud_type`, `fraud_description`
  - `fraud_phone`, `fraud_contact`, `fraud_bank`, `utr_number` (optional)
  - File Uploads: `screenshot`, `chat_proof`, `payment_proof`, `call_recording`
- **Response**: `{"message": "Report submitted successfully."}`

### 🔸 `GET /api/reports`

- **Description**: Fetch all submitted reports
- **Response**: List of all stored reports

---

## 🧪 Running the Project Locally

### 🔧 Backend (Flask)


```bash
# Clone the repository
git clone https://github.com/ItsMeSMT7/Fraude_Reporting.git
cd fraude-reporting-app/backend

# Create virtual environment
python -m venv venv
# Activate it
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Add your environment variables in a .env file
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
DATABASE_URL=mongodb://localhost:27017/fraud_report_api

# Start the server
python app.py
```
  
## 🌐 Frontend (React)

```bash
# Navigate to the frontend folder
cd ../frontend

# Install dependencies
npm install

# Start the React development server
npm start
```
## ☁️ Deployment
- **Backend:** Host via Heroku, AWS, DigitalOcean

- **Frontend:** Deploy on Netlify, Vercel, or GitHub Pages

- **Use environment variables on the cloud to protect credentials and database strings.**

## 🤝 Contributing
## Contributions are welcome! Feel free to:

- **Submit issues**

- **Suggest features**

- **Create pull requests**

  ## Next features might include:

- **SMS alerts via Twilio**

- **AI-based fraud detection patterns**

## 📄 License

This project is licensed under the MIT License.

## 📬 Contact

For suggestions or issues, contact: asalkarsumit@gmail.com

GitHub: ItsMeSMT7
