 Health Prediction Application

Project Overview
This is a web-based Health Prediction Application built using Flask.  
It collects patient blood test data and uses an AI-powered API to generate health risk predictions.

The system performs CRUD operations and stores patient records in a SQLite database.

 Features

- Add new patient records (Create)
- View all patient records (Read)
- Update patient details (Update)
- Delete patient records (Delete)
- AI-generated health risk analysis in remarks field
- Input validation (email, DOB, numeric checks)
- Clean and simple UI using HTML

 AI/ML Integration

The application uses Google Gemini API to analyze:

- Glucose level
- Haemoglobin level
- Cholesterol level

It returns a short health risk assessment which is stored in the **Remarks** field.
Tech Stack

- Python (Flask)
- SQLite (Database)
- HTML, CSS (Frontend)
- Bootstrap (UI styling)
- Google Gemini API (AI prediction)

---

## 📂 Project Structure
