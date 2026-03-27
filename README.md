# 🎓 AI-Based College Approval Prediction System

A comprehensive AI-powered system designed to evaluate educational institutions based on AICTE norms. This project integrates **rule-based compliance checks** and **machine learning models** to predict approval probability, risk score, and faculty shortages.

Built as a **decision-support system** to improve transparency, efficiency, and accuracy in institutional approval processes.

---

## 🚀 Features

### 🏛️ For Administrators / Institutions

* 📊 **Institution Evaluation:** Analyze compliance based on AICTE norms
* 🧑‍🏫 **Faculty Analysis:** Check faculty strength, PhD %, duplication detection
* 🏢 **Infrastructure Validation:** Evaluate labs, classrooms, area, computers
* 🎓 **Accreditation Checks:** Validate NAAC, NBA, ISO certifications
* 📄 **Document Upload:** Upload and validate institutional PDF reports
* 📊 **Dashboard:** View risk score, approval probability, and compliance status

---

### 🤖 AI & Machine Learning Features

* **Approval Prediction:** ML-based probability using XGBoost
* **Risk Score Calculation:** Combines 18+ rule-based checks
* **Faculty Shortage Detection:** Predicts shortage using ML model
* **Feature Engineering:** Faculty ratio, infra score, compliance metrics
* **Real-Time Predictions:** Integrated with backend APIs

---

### 🌐 System Features

* 🔐 OTP-based authentication system
* 📄 PDF validation and section matching
* ⚡ Real-time API-based predictions
* 📊 Structured output (Risk Level: Low / Medium / High)

---

## 🛠️ Tech Stack

### Backend

* Framework: **Python Django**
* Database: **SQLite**
* Authentication: OTP-based verification

### Machine Learning

* Models: **XGBoost, Scikit-learn**
* Explainability: Feature-based scoring
* Storage: Joblib (.pkl models)

### Frontend

* Core: **HTML5, CSS3, JavaScript**
* Design: Responsive UI with dashboard layout

---

## 📂 Project Structure

```
AICTE-Approval-System
├── backend
│   ├── aicteapproval
│   │   ├── views.py              # API + risk checks
│   │   ├── models.py             # Database models
│   │   ├── ml
│   │   │   ├── predictor.py      # ML prediction pipeline
│   │   │   ├── feature_builder.py# Feature engineering
│   │   │   ├── train_models.py   # Model training
│   │   │   ├── *.pkl             # Trained models
│   │   └── urls.py               # API routing
│
├── frontend
│   ├── pages/
│   │   ├── *.html                # UI pages
│   ├── css/
│   ├── js/
│
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Prerequisites

* Python 3.10+
* pip
* Git

---

### 2️⃣ Backend Setup

Clone the repository:

```
git clone https://github.com/b-tejasri/AICTE-Approval-System
cd backend
```

Create virtual environment:

```
python -m venv venv
venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Run server:

```
python manage.py runserver
```

---

### 3️⃣ ML Model Setup

Ensure trained model files exist:

* risk_model.pkl
* approval_model.pkl
* faculty_model.pkl

Place inside:

```
backend/aicteapproval/ml/
```

---

### 4️⃣ Frontend Setup

```
cd frontend
python -m http.server 5500
```

Open:

```
http://localhost:5500
```

---

## 🧠 How It Works

1. User enters institutional data
2. Backend processes data using Django
3. Rule-based checks (`_compute_risk`) evaluate compliance
4. ML models (`predictor.py`) generate predictions
5. Output displayed:

   * Risk Score
   * Approval Probability
   * Faculty Shortage

---

## 🔍 Key Checks Implemented

* Faculty shortage detection
* Student–faculty ratio validation
* PhD percentage check
* Duplicate faculty detection
* Infrastructure evaluation (labs, classrooms, area)
* Accreditation validation (NAAC, NBA, ISO)
* Financial and student data checks
* Historical rejection analysis

---

## 📈 Results

* Provides real-time institutional evaluation
* Improves transparency in approval process
* Reduces manual effort and errors
* Helps institutions improve compliance

---

## 🔮 Future Scope

* Integration with real AICTE database
* AI-based document verification
* Advanced deep learning models
* Cloud deployment (AWS / Azure)
* Explainable AI dashboards


## 📜 License

This project is developed for academic and educational purposes.
