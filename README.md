# 🧠 OmniMap - AI-Powered Personality Assessment & Activity Recommendation System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-316192.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3.2-orange.svg)
![Machine Learning](https://img.shields.io/badge/ML-Neural_Network-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

> **A comprehensive web-based personality assessment system** that uses the **OMNI Personality Test** (Big Five Model) combined with **custom Machine Learning models** to analyze student personalities and recommend tailored campus activities.

---

## ✨ Features

### 🎯 **Core Capabilities**
- 🧪 **OMNI Personality Test** - 200-question comprehensive psychological assessment
- 📊 **Big Five Analysis** - Scientific measurement of Extraversion, Agreeableness, Conscientiousness, Neuroticism, and Openness
- 🤖 **Custom ML Models** - Neural Network-based personality prediction (no external API dependencies)
- 🎓 **Smart Recommendations** - AI-powered activity matching with compatibility scores
- 📈 **Interactive Dashboard** - Real-time visualization of personality dimensions and insights
- 💾 **PostgreSQL Database** - Production-ready database for optimal performance and scalability

### 🧬 **Personality Dimensions Analyzed**

| Trait | Facets Measured |
|-------|----------------|
| **Extraversion** | Energy, Sociability, Assertiveness, Excitement-seeking |
| **Agreeableness** | Warmth, Trustfulness, Sincerity, Modesty |
| **Conscientiousness** | Dutifulness, Orderliness, Self-reliance, Ambition |
| **Neuroticism** | Anxiety, Depression, Moodiness, Irritability |
| **Openness** | Aestheticism, Intellect, Flexibility, Tolerance |
| **Additional Traits** | Narcissism, Sensation-seeking |

### 🎓 **Activity Categories**
- **UKM** (Student Activity Units)
- **Organizations** (Campus Orgs)
- **Committees** (Kepanitiaan)
- **Competitions** (Lomba)
- **Workshops** & Training Programs

### 🤖 **Machine Learning Architecture**
- **Personality Classifier**: Multi-layer Perceptron (Neural Network) trained on 5,000+ samples
- **Recommendation Engine**: Content-based filtering using cosine similarity
- **Efficient Model Loading**: Models loaded once at startup for instant predictions (<100ms)
- **Intelligent Fallback**: Automatic API backup if ML models fail
- **No Re-training Required**: Models use pre-trained `.pkl` files for instant inference

---

## 🚀 Getting Started

### 📋 **Prerequisites**

Before you begin, ensure you have the following installed:

| Software | Version | Download Link |
|----------|---------|---------------|
| **Python** | 3.8+ | [python.org](https://www.python.org/downloads/) |
| **PostgreSQL** | 12+ | [postgresql.org](https://www.postgresql.org/download/) |
| **pip** | Latest | Included with Python |

---

## 📥 Installation Guide

### **Step 1: Clone the Repository**

```bash
git clone https://github.com/yourusername/Omnimap.git
cd Omnimap-main
```

---

### **Step 2: Setup PostgreSQL Database**

#### **Windows:**
1. Open **SQL Shell (psql)** from Start Menu
2. Login with your PostgreSQL credentials
3. Run the following commands:

```sql
CREATE DATABASE omnimap_db;
\q
```

#### **macOS/Linux:**
```bash
# Access PostgreSQL
psql -U postgres

# Inside psql terminal
CREATE DATABASE omnimap_db;
\q
```

> **💡 Tip**: Note down your PostgreSQL password - you'll need it in the next step!

---

### **Step 3: Configure Environment Variables**

Create a `.env` file in the project root directory:

```bash
# Create the file
touch .env  # macOS/Linux
# or
type nul > .env  # Windows
```

Add the following configuration to `.env`:

```env
# ============================================
# DATABASE CONFIGURATION
# ============================================
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password_here
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=omnimap_db

# ============================================
# FLASK CONFIGURATION
# ============================================
SECRET_KEY=change-this-to-random-secret-key-in-production
FLASK_ENV=development
```

⚠️ **IMPORTANT**: Replace `your_password_here` with your actual PostgreSQL password!

---

### **Step 4: Create Virtual Environment** *(Recommended)*

#### **Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

#### **macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

> **✅ Success Indicator**: Your terminal prompt should now show `(venv)` at the beginning

---

### **Step 5: Install Dependencies**

```bash
pip install -r requirements.txt
```

**If you encounter errors**, install packages individually:

```bash
pip install Flask==3.0.0
pip install Flask-SQLAlchemy==3.1.1
pip install psycopg2-binary==2.9.9
pip install scikit-learn==1.3.2
pip install pandas==2.1.3
pip install numpy==1.26.2
pip install python-dotenv==1.0.0
pip install openpyxl==3.1.2
```

---

### **Step 6: Initialize Database**

```bash
# Start the Flask app to create database tables
python app.py
```

Wait for the message:
```
* Running on http://127.0.0.1:5000
```

Then press **Ctrl+C** to stop the server.

Next, seed the database with sample data:

```bash
python seed_data.py
```

**Expected output:**
```
✓ Sample users created
✓ Sample activities created
✓ Database seeded successfully!
```

---

### **Step 7: Train Machine Learning Models** ⚡

> **⏰ Time Required**: 30-60 minutes (depending on your CPU)

This is a **critical step** - the system requires trained models to function!

#### **Step 7.1: Preprocess Training Data**
```bash
python ml_training/scripts/1_preprocess_data.py
```

**Expected output:**
```
✓ Data loaded from Excel
✓ Features extracted (200 questions)
✓ Train/test split complete
✓ Data saved to ml_training/data/processed/
```

#### **Step 7.2: Train Personality Prediction Model**
```bash
python ml_training/scripts/2_train_personality.py
```

**Expected output:**
```
Training Neural Network...
Epoch [100/500] - Loss: 0.0234
✓ Model trained successfully
✓ Model saved to ml_models/personality_classifier.pkl
✓ Test R² Score: 0.87
```

> **⏱️ Duration**: 20-40 minutes

#### **Step 7.3: Train Recommendation System**
```bash
python ml_training/scripts/3_train_recommender.py
```

**Expected output:**
```
Building activity-personality matrix...
✓ Recommender trained successfully
✓ Model saved to ml_models/activity_recommender.pkl
```

> **⏱️ Duration**: 5 minutes

#### **Verify Model Files**

After training, confirm these files exist:

```
ml_models/
├── personality_classifier.pkl  ✓
├── activity_recommender.pkl    ✓
├── scaler.pkl                  ✓
└── label_encoders.pkl          ✓
```

---

### **Step 8: Launch the Application** 🚀

```bash
python app.py
```

**Expected output:**
```
 * Running on http://127.0.0.1:5000
 * ML Models loaded successfully
 * Press CTRL+C to quit
```

Open your browser and navigate to:

🌐 **http://localhost:5000**

---

## 🔐 Default Login Accounts

After seeding the database, use these credentials:

| Role | Username | Password | Description |
|------|----------|----------|-------------|
| 👑 **Admin** | `puti` | `admin123` | Full system access |
| 👤 **Student** | `putrikusuma` | `mahasiswa123` | Regular user account |

---

## 📁 Project Structure

```
Omnimap-main/
│
├── 📄 app.py                       # Main Flask application
├── ⚙️ config.py                    # Database & app configuration
├── 🌱 seed_data.py                 # Database seeding script
├── 📋 requirements.txt             # Python dependencies
├── 🔒 .env                         # Environment variables (YOU CREATE THIS)
│
├── 📂 database/                    # Database layer
│   ├── models.py                   # SQLAlchemy ORM models
│   └── connection.py               # DB connection utilities
│
├── 🤖 ml_models/                   # Trained ML Models (Generated)
│   ├── personality_classifier.pkl  # 🔴 Neural Network model
│   ├── activity_recommender.pkl    # 🔴 Recommendation engine
│   ├── scaler.pkl                  # 🔴 Feature scaler
│   └── label_encoders.pkl          # 🔴 Category encoders
│
├── 🧪 ml_training/                 # ML Training Pipeline
│   ├── 📊 data/
│   │   ├── raw/
│   │   │   └── data_tes_omni.xlsx  # Training dataset (5000 samples)
│   │   └── processed/              # 🔴 Preprocessed data (auto-generated)
│   │
│   └── 📜 scripts/
│       ├── 1_preprocess_data.py    # Data cleaning & feature extraction
│       ├── 2_train_personality.py  # Train personality predictor
│       ├── 3_train_recommender.py  # Train recommendation system
│       └── evaluate_models.py      # Model performance evaluation
│
├── 🛠️ utils/                       # Helper Functions
│   ├── model_loader.py             # Efficient ML model loader
│   └── prediction.py               # Prediction utilities
│
├── 🌐 api/                         # API Routes
│   ├── ml_routes.py                # ML prediction endpoints
│   └── test_routes.py              # Test submission routes
│
├── 🎨 static/                      # Static Assets
│   ├── css/                        # Stylesheets
│   ├── js/                         # JavaScript files
│   └── img/                        # Images & icons
│
├── 📄 templates/                   # HTML Templates
│   ├── dashboard.html              # Main dashboard
│   ├── login.html                  # Authentication page
│   ├── profile.html                # User profile
│   ├── tes_omni.html               # Personality test interface
│   ├── hasil_tes.html              # Test results page
│   ├── chatbot.html                # AI chatbot
│   ├── detailkegiatan.html         # Activity details
│   └── partials/                   # Reusable components
│       ├── navbar.html
│       ├── sidebar.html
│       └── logout_modal.html
│
└── 💾 instance/                    # SQLite backup (auto-generated)
```

**Legend:**
- 🔴 Files generated by training scripts
- ⚙️ Configuration files
- 🤖 Machine Learning components
- 🌐 API endpoints
- 🎨 Frontend assets

---

## 🛠️ Technology Stack

### **Backend Technologies**

| Technology | Version | Purpose |
|------------|---------|---------|
| **Flask** | 3.0.0 | Web framework & routing |
| **PostgreSQL** | 15+ | Production database |
| **SQLAlchemy** | 3.1.1 | Object-Relational Mapping (ORM) |
| **Werkzeug** | 3.0.1 | Security & password hashing |

### **Machine Learning Stack**

| Technology | Version | Purpose |
|------------|---------|---------|
| **scikit-learn** | 1.3.2 | ML framework & algorithms |
| **Pandas** | 2.1.3 | Data manipulation & analysis |
| **NumPy** | 1.26.2 | Numerical computing |
| **Neural Network** | MLP | Personality classification model |
| **Cosine Similarity** | - | Content-based recommendation |

### **Frontend Technologies**

| Technology | Version | Purpose |
|------------|---------|---------|
| **Bootstrap** | 5.3.3 | Responsive UI framework |
| **Chart.js** | 4.4.0 | Data visualization & charts |
| **Bootstrap Icons** | 1.11.1 | Icon library |
| **JavaScript** | ES6+ | Client-side interactivity |

---


## 🆘 Troubleshooting Guide

### **Error 1: `psycopg2` Installation Failed**

**Windows Solution:**
```bash
# Install Visual C++ Build Tools first
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Then install psycopg2-binary
pip install psycopg2-binary==2.9.9
```

---

### **Error 2: PostgreSQL Connection Refused**

**Check if PostgreSQL is running:**

**Windows:**
```bash
# Open Services (services.msc)
# Look for "postgresql-x64-XX" service
# Status should be "Running"
```

**macOS:**
```bash
brew services list
brew services start postgresql@15
```

**Linux:**
```bash
sudo systemctl status postgresql
sudo systemctl start postgresql
```

**Test connection:**
```bash
psql -U postgres -d omnimap_db
```

---

### **Error 3: Model Files Not Found**

**Solution:**
```bash
# Ensure training data exists
ls ml_training/data/raw/data_tes_omni.xlsx

# Re-run training scripts in order
python ml_training/scripts/1_preprocess_data.py
python ml_training/scripts/2_train_personality.py
python ml_training/scripts/3_train_recommender.py

# Verify model files created
ls ml_models/*.pkl
```

---

### **Error 4: Training Takes Too Long**

**Solution - Reduce Training Iterations:**

Edit `ml_training/scripts/2_train_personality.py`:

```python
# Line ~50, reduce max_iter:
model = MLPRegressor(
    hidden_layers=(128, 64, 32),
    max_iter=100,  # Change from 500 to 100
    random_state=42,
    verbose=True
)
```

---

### **Error 5: Excel File Not Found**

**Solution:**
```bash
# Ensure file exists at:
ml_training/data/raw/data_tes_omni.xlsx

# If missing, training will skip but system still works
# It will use fallback algorithms
```

---

### **🔄 Complete Database Reset**

If you need to start fresh:

```bash
# Step 1: Drop existing database
psql -U postgres -c "DROP DATABASE omnimap_db;"

# Step 2: Create new database
psql -U postgres -c "CREATE DATABASE omnimap_db;"

# Step 3: Re-initialize
python app.py  # Press Ctrl+C after tables created

# Step 4: Re-seed data
python seed_data.py
```

---

## 📊 Model Performance Metrics

### **Personality Classification Model**

| Metric | Value | Details |
|--------|-------|---------|
| **Architecture** | MLP (128-64-32) | Multi-layer Perceptron |
| **Input Features** | 200 | OMNI test questions |
| **Output Dimensions** | 32 | 7 domains + 25 facets |
| **Training Samples** | 5,000 | Real student data |
| **R² Score** | 0.87 | Test set performance |
| **Training Time** | 20-40 min | Depends on CPU |
| **Inference Time** | <100ms | Per prediction |

### **Activity Recommendation System**

| Metric | Value | Details |
|--------|-------|---------|
| **Method** | Cosine Similarity | Content-based filtering |
| **Feature Space** | Personality vectors | Big Five + facets |
| **Training Time** | 5 min | Quick training |
| **Inference Time** | <50ms | Per recommendation |
| **Top-N Results** | 10 | Most relevant activities |

---

## 📝 Notes for Instructors & Reviewers

### **⏰ Setup Time Estimation**

| Task | Duration | Details |
|------|----------|---------|
| PostgreSQL Installation | 10 min | Download + install |
| Project Setup | 5 min | Clone + venv |
| Dependency Installation | 5 min | pip install |
| Database Initialization | 2 min | Create + seed |
| **ML Model Training** | **30-60 min** | **Most time-consuming** |
| **Total Estimated Time** | **~1 hour** | Varies by hardware |

### **💻 System Requirements**

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **RAM** | 4GB | 8GB+ |
| **Storage** | 500MB | 1GB |
| **CPU** | Dual-core | Quad-core+ |
| **Python** | 3.8 | 3.10+ |
| **PostgreSQL** | 12 | 15+ |

### **📦 Critical Files Checklist**

Before running the application, ensure these files exist:

- ✅ `.env` (create manually with PostgreSQL password)
- ✅ `ml_training/data/raw/data_tes_omni.xlsx` (5000 training samples)
- ✅ `ml_models/personality_classifier.pkl` (after training)
- ✅ `ml_models/activity_recommender.pkl` (after training)
- ✅ `ml_models/scaler.pkl` (after training)

### **🔄 Fallback System**

> **Important**: If ML model training fails or models are unavailable, the system automatically falls back to the original manual calculation algorithms. The ML models are an **enhancement**, not a requirement.

**Fallback Behavior:**
- ❌ ML Model fails → ✅ Use original calculation
- ❌ Recommender fails → ✅ Use manual matching
- ✅ System remains **fully functional**

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch:
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit** your changes:
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push** to the branch:
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open** a Pull Request

### **Development Guidelines**
- Follow PEP 8 style guide for Python code
- Add docstrings to all functions
- Update tests for new features
- Update documentation as needed

---


## 👥 Credits & Acknowledgments

### **Kelompok 2**
**Computing Project Team** - Telkom University

### **Special Thanks**
- 🎓 **Big Five Personality Model** research community
- 🐍 **Flask & SQLAlchemy** documentation and contributors
- 🤖 **scikit-learn** community for ML tools
- 🎨 **Bootstrap** team for the excellent UI framework
- 📊 **Chart.js** for beautiful data visualizations

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting Guide](#-troubleshooting-guide)
2. Open an issue on GitHub
3. Contact the development team

---

## 🔖 Version Information

| Version | Release Date | Changes |
|---------|--------------|---------|
| **2.0** | December 2024 | PostgreSQL + ML Models |
| **1.0** | November 2024 | Initial Release |

---

<div align="center">

**Made with ❤️ by Computing Project Team**

**Telkom University**

---

⭐ **Star this repository if you found it helpful!** ⭐

</div>