# 🧠 OmniMap - Personality-Based Activity Recommendation System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.3-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

OmniMap is a web-based personality assessment and activity recommendation system designed for university students. It uses the **OMNI Personality Test** (based on the Big Five personality model) to analyze users' personality traits and recommend suitable campus activities, organizations, and events.

## ✨ Features

### 🎯 Core Features
- **OMNI Personality Test** - 200-question comprehensive personality assessment
- **Big Five Analysis** - Measures Extraversion, Agreeableness, Conscientiousness, Neuroticism, and Openness
- **Smart Recommendations** - AI-powered activity matching based on personality traits
- **Match Percentage** - Shows compatibility score between user personality and activities
- **Interactive Dashboard** - Visual representation of personality dimensions and insights

### 📊 Personality Traits Analyzed
- **Extraversion**: Energy, Sociability, Assertiveness, Excitement-seeking
- **Agreeableness**: Warmth, Trustfulness, Sincerity, Modesty
- **Conscientiousness**: Dutifulness, Orderliness, Self-reliance, Ambition
- **Neuroticism**: Anxiety, Depression, Moodiness, Irritability
- **Openness**: Aestheticism, Intellect, Flexibility, Tolerance
- **Additional**: Narcissism, Sensation-seeking

### 🎓 Activity Categories
- UKM (Student Activity Units)
- Organizations
- Committees (Kepanitiaan)
- Competitions (Lomba)
- Workshops

### 🤖 AI Chatbot
- Integrated chatbot powered by Google Gemini API
- Provides personalized guidance and activity suggestions

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Omnimap.git
   cd Omnimap-main
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python init_db.py
   ```

5. **Seed sample data** (optional)
   ```bash
   python seed_data.py
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Open in browser**
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
Omnimap-main/
├── app.py                 # Main Flask application
├── init_db.py             # Database initialization script
├── seed_data.py           # Sample data seeder
├── requirements.txt       # Python dependencies
├── instance/              # SQLite database storage
├── static/
│   ├── css/              # Stylesheets
│   │   ├── style.css
│   │   ├── profile.css
│   │   ├── navbar.css
│   │   └── ...
│   ├── js/               # JavaScript files
│   │   ├── script.js
│   │   ├── profile.js
│   │   └── ...
│   └── img/              # Images and icons
└── templates/
    ├── dashboard.html     # Main dashboard
    ├── login.html         # Authentication
    ├── profile.html       # User profile
    ├── tes_omni.html      # Personality test
    ├── hasil_tes.html     # Test results
    ├── chatbot.html       # AI chatbot interface
    ├── detailkegiatan.html # Activity details
    └── partials/          # Reusable components
        ├── navbar.html
        ├── sidebar.html
        └── logout_modal.html
```

## 🛠️ Tech Stack

### Backend
- **Flask 3.0.0** - Web framework
- **Flask-SQLAlchemy** - ORM for database operations
- **SQLite** - Database
- **Werkzeug** - Password hashing and security

### Frontend
- **Bootstrap 5.3.3** - CSS framework
- **Bootstrap Icons** - Icon library
- **Chart.js 4.4.0** - Data visualization
- **Vanilla JavaScript** - Interactive features

### AI/ML
- **Google Generative AI** - Chatbot functionality
- **scikit-learn** - Machine learning utilities
- **NumPy & Pandas** - Data processing

## 📱 Screenshots

### Dashboard
The dashboard displays:
- Welcome banner with quick actions
- Personality dimension bars (Big Five traits)
- Insight badges showing dominant traits
- Activity recommendations with match percentages
- Category distribution chart

### Personality Test
- 200 comprehensive questions
- Progress tracking
- Likert scale responses (1-5)

### Results Page
- Detailed trait analysis
- T-score calculations
- Visual charts and graphs
- Personalized insights

## 🔐 Default Accounts

After running `seed_data.py`, you can use these accounts:

| Role | Username | Password |
|------|----------|----------|
| Admin | puti | admin123 |
| User | putrikusuma | mahasiswa123 |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Computing Project Team - Telkom University

## 🙏 Acknowledgments

- Big Five Personality Model research
- Flask documentation and community
- Bootstrap team for the excellent UI framework
- Chart.js for beautiful data visualizations  
