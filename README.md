# Smart-Civic-Complaint-System
A Flask-based Smart Civic Complaint Management System with User and Admin modules.

A robust, web-based platform built with Flask that allows users to log, track, and manage issues. Designed with a clean interface and secure backend processing, this application simplifies the dispute or resolution workflow.

---

## ✨ Features
* **User Authentication:** Secure user registration, login, and session tracking.
* **Complaint/Issue Logging:** Users can easily submit detailed complaints (e.g., `my_complaint`).
* **Real-time Tracking:** Dynamic updates on the status of submitted issues.
* **Responsive UI:** Fully optimized for both desktop and mobile viewing.
* **Database Management:** Auto-initializes required tables (`create_table()`) upon starting the application.

---

## 🛠️ Tech Stack
* **Backend:** Python, Flask
* **Database/Storage:** [Insert your DB type here, e.g., SQLite / PostgreSQL]
* **Environment Management:** Python `os` module for dynamic port and environment configuration

---

## 💻 Local Setup & Installation

To run this project locally on your machine, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/sachirrane/Smart-Civic-Complaint-System.git](https://github.com/sachirrane/Smart-Civic-Complaint-System.git)
   cd Smart-Civic-Complaint-System



2.Set up a virtual environment (Optional but recommended):

Bash
python -m venv venv
# Activate on Windows:
venv\Scripts\activate
# Activate on Mac/Linux:
source venv/bin/activate


3.Install dependencies:
(Ensure you have your dependencies listed in a requirements.txt file)

Bash
pip install -r requirements.txt

4. Run the application:

Bash
python app.py
Open your browser and navigate to http://127.0.0.1:5000


🔮 Future Scope & Upcoming Enhancements
Here are the planned features and improvements to scale the application moving forward:

☁️ Cloud Deployment: Configure environment variables to seamlessly host and deploy the live application on platforms like Render.

🛡️ Advanced Role-Based Access Control (RBAC): Introduce distinct dashboards for "Admin", "Staff", and "End User" to manage resolution permissions.

📧 Automated Email Notifications: Integrate an email API (like SendGrid) to automatically notify users when their complaint status changes.

📊 Analytics Dashboard: Implement data visualization charts for admins to track the total volume of complaints, pending issues, and resolution rates.

📎 File Attachment Support: Allow users to upload images or screenshots alongside their complaints for better context.
