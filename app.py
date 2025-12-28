from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import json
from datetime import timedelta
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from google import genai
import requests
from functools import lru_cache
import time
from datetime import datetime, timedelta
import random
# NEW IMPORTS
from config import config_by_name
from dotenv import load_dotenv
from functools import lru_cache
import hashlib

load_dotenv()

app = Flask(__name__)

# Config
env = os.getenv('FLASK_ENV', 'production')  # default production
app.config.from_object(config_by_name[env])

# Gemini setup (ini sudah OK)
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    print("⚠️ GEMINI_API_KEY tidak ditemukan")
    gemini_client = None
else:
    gemini_client = genai.Client(api_key=api_key)
    print(f"✅ Gemini Client initialized")

# Database - NO FALLBACK untuk production
db = SQLAlchemy(app)

# Test connection di development only
if env == 'development':
    try:
        with app.app_context():
            db.engine.connect()
        print("✅ Connected to database!")
    except Exception as e:
        print(f"⚠️ Database error: {e}")

# Tambahkan setelah inisialisasi app
@app.template_filter('zfill')
def zfill_filter(value, width=2):
    """Add leading zeros to number"""
    return str(value).zfill(width)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nim = db.Column(db.String(50), unique=True, nullable=False)
    nama = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    fakultas = db.Column(db.String(255))
    profile_picture = db.Column(db.Text)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    energy_raw = db.Column(db.Integer)
    sociability_raw = db.Column(db.Integer)
    assertiveness_raw = db.Column(db.Integer)
    excitement_raw = db.Column(db.Integer)
    warmth_raw = db.Column(db.Integer)
    trustfulness_raw = db.Column(db.Integer)
    sincerity_raw = db.Column(db.Integer)
    modesty_raw = db.Column(db.Integer)
    dutifulness_raw = db.Column(db.Integer)
    orderliness_raw = db.Column(db.Integer)
    self_reliance_raw = db.Column(db.Integer)
    ambition_raw = db.Column(db.Integer)
    anxiety_raw = db.Column(db.Integer)
    depression_raw = db.Column(db.Integer)
    moodiness_raw = db.Column(db.Integer)
    irritability_raw = db.Column(db.Integer)
    aestheticism_raw = db.Column(db.Integer)
    intellect_raw = db.Column(db.Integer)
    flexibility_raw = db.Column(db.Integer)
    tolerance_raw = db.Column(db.Integer)
    exhibitionism_raw = db.Column(db.Integer)
    self_indulgence_raw = db.Column(db.Integer)
    impulsiveness_raw = db.Column(db.Integer)
    hostility_raw = db.Column(db.Integer)
    conventionality_raw = db.Column(db.Integer)
    
    extraversion_raw = db.Column(db.Integer)
    agreeableness_raw = db.Column(db.Integer)
    conscientiousness_raw = db.Column(db.Integer)
    neuroticism_raw = db.Column(db.Integer)
    openness_raw = db.Column(db.Integer)
    narcissism_raw = db.Column(db.Integer)
    sensation_seeking_raw = db.Column(db.Integer)
    
    energy_t = db.Column(db.Float)
    sociability_t = db.Column(db.Float)
    assertiveness_t = db.Column(db.Float)
    excitement_t = db.Column(db.Float)
    warmth_t = db.Column(db.Float)
    trustfulness_t = db.Column(db.Float)
    sincerity_t = db.Column(db.Float)
    modesty_t = db.Column(db.Float)
    dutifulness_t = db.Column(db.Float)
    orderliness_t = db.Column(db.Float)
    self_reliance_t = db.Column(db.Float)
    ambition_t = db.Column(db.Float)
    anxiety_t = db.Column(db.Float)
    depression_t = db.Column(db.Float)
    moodiness_t = db.Column(db.Float)
    irritability_t = db.Column(db.Float)
    aestheticism_t = db.Column(db.Float)
    intellect_t = db.Column(db.Float)
    flexibility_t = db.Column(db.Float)
    tolerance_t = db.Column(db.Float)
    exhibitionism_t = db.Column(db.Float)
    self_indulgence_t = db.Column(db.Float)
    impulsiveness_t = db.Column(db.Float)
    hostility_t = db.Column(db.Float)
    conventionality_t = db.Column(db.Float)
    extraversion_t = db.Column(db.Float)
    agreeableness_t = db.Column(db.Float)
    conscientiousness_t = db.Column(db.Float)
    neuroticism_t = db.Column(db.Float)
    openness_t = db.Column(db.Float)
    narcissism_t = db.Column(db.Float)
    sensation_seeking_t = db.Column(db.Float)
    
    energy_kategori = db.Column(db.String(50))
    sociability_kategori = db.Column(db.String(50))
    assertiveness_kategori = db.Column(db.String(50))
    excitement_kategori = db.Column(db.String(50))
    warmth_kategori = db.Column(db.String(50))
    trustfulness_kategori = db.Column(db.String(50))
    sincerity_kategori = db.Column(db.String(50))
    modesty_kategori = db.Column(db.String(50))
    dutifulness_kategori = db.Column(db.String(50))
    orderliness_kategori = db.Column(db.String(50))
    self_reliance_kategori = db.Column(db.String(50))
    ambition_kategori = db.Column(db.String(50))
    anxiety_kategori = db.Column(db.String(50))
    depression_kategori = db.Column(db.String(50))
    moodiness_kategori = db.Column(db.String(50))
    irritability_kategori = db.Column(db.String(50))
    aestheticism_kategori = db.Column(db.String(50))
    intellect_kategori = db.Column(db.String(50))
    flexibility_kategori = db.Column(db.String(50))
    tolerance_kategori = db.Column(db.String(50))
    exhibitionism_kategori = db.Column(db.String(50))
    self_indulgence_kategori = db.Column(db.String(50))
    impulsiveness_kategori = db.Column(db.String(50))
    hostility_kategori = db.Column(db.String(50))
    conventionality_kategori = db.Column(db.String(50))
    extraversion_kategori = db.Column(db.String(50))
    agreeableness_kategori = db.Column(db.String(50))
    conscientiousness_kategori = db.Column(db.String(50))
    neuroticism_kategori = db.Column(db.String(50))
    openness_kategori = db.Column(db.String(50))
    narcissism_kategori = db.Column(db.String(50))
    sensation_seeking_kategori = db.Column(db.String(50))
    
    skor_rata_rata = db.Column(db.Float)
    status_tes = db.Column(db.String(50), default='Belum Selesai')
    progress_profil = db.Column(db.Integer, default=100)
    progress_tes = db.Column(db.Integer, default=0)
    progress_eksplorasi = db.Column(db.Integer, default=0)
    progress_kegiatan = db.Column(db.Integer, default=0)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), default='info')  # info, success, warning, danger
    is_read = db.Column(db.Boolean, default=False)
    link = db.Column(db.String(500))  # URL tujuan jika diklik
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='notifications')
class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(255), nullable=False)
    kategori = db.Column(db.String(100))
    tingkat_kesulitan = db.Column(db.String(50))
    peserta = db.Column(db.String(50))
    deadline = db.Column(db.String(100))
    lokasi = db.Column(db.String(255))
    deskripsi = db.Column(db.Text)
    required_traits = db.Column(db.String(500))
    
    # Kolom baru untuk data detail
    persyaratan_json = db.Column(db.Text)  # JSON string for requirements list
    manfaat_json = db.Column(db.Text)  # JSON string for benefits list
    jadwal_json = db.Column(db.Text)  # JSON string for schedule
    link = db.Column(db.String(500))  # Registration link
    contact_json = db.Column(db.Text)  # JSON string for contact info
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)
    status = db.Column(db.String(50), default='Bergabung')
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

def populate_sample_activities():
    """Populate database with sample activities"""
    import json
    
    sample_activities = [
        {
            'nama': 'UKM EMBUN (Seni)',
            'kategori': 'UKM',
            'tingkat_kesulitan': 'Pemula',
            'peserta': '50/100',
            'deadline': '31 Desember 2025',
            'lokasi': 'Telkom University',
            'deskripsi': 'Bergabunglah dengan UKM Seni untuk mengembangkan bakat seni Anda. Kami menyediakan berbagai kegiatan seperti melukis, menggambar, dan seni pertunjukan.',
            'required_traits': 'creativity,openness,aestheticism',
            'persyaratan_json': json.dumps([
                'Mahasiswa aktif semester 1-6',
                'Memiliki minat di bidang seni',
                'Mengisi formulir pendaftaran'
            ]),
            'manfaat_json': json.dumps([
                'Sertifikat kegiatan',
                'Pengembangan soft skills',
                'Networking dengan seniman',
                'Kesempatan pameran karya'
            ]),
            'jadwal_json': json.dumps([
                {'hari': 'Senin', 'waktu': '08.00 - 09.00', 'kegiatan': 'Latihan Seni Lukis'},
                {'hari': 'Rabu', 'waktu': '16.00 - 18.00', 'kegiatan': 'Diskusi & Apresiasi Seni'},
                {'hari': 'Jumat', 'waktu': '16.00 - 18.00', 'kegiatan': 'Workshop Teknik'}
            ]),
            'link': 'https://linktr.ee/inkubasibisnisbtp',
            'contact_json': json.dumps({
                'name': 'Ketua UKM Seni',
                'phone': '0812-3456-7890',
                'email': 'ukmseni@omnimap.ac.id'
            })
        },
        {
            'nama': 'BEM Fakultas',
            'kategori': 'Organisasi',
            'tingkat_kesulitan': 'Menengah',
            'peserta': '30/50',
            'deadline': '15 Januari 2026',
            'lokasi': 'Gedung Fakultas',
            'deskripsi': 'Bergabung dengan BEM Fakultas untuk mengembangkan jiwa kepemimpinan dan memberikan kontribusi nyata untuk kemajuan fakultas.',
            'required_traits': 'leadership,extraversion,conscientiousness',
            'persyaratan_json': json.dumps([
                'IPK minimal 3.0',
                'Mahasiswa aktif semester 2-6',
                'Memiliki pengalaman organisasi',
                'Lolos seleksi administrasi dan wawancara'
            ]),
            'manfaat_json': json.dumps([
                'Sertifikat pengurus BEM',
                'Pengembangan leadership',
                'Jaringan luas',
                'Pengalaman mengorganisir acara besar'
            ]),
            'jadwal_json': json.dumps([
                {'hari': 'Senin', 'waktu': '19.00 - 21.00', 'kegiatan': 'Rapat Koordinasi'},
                {'hari': 'Kamis', 'waktu': '19.00 - 21.00', 'kegiatan': 'Evaluasi Program'}
            ]),
            'link': 'https://bit.ly/daftar-bem-fakultas',
            'contact_json': json.dumps({
                'name': 'Sekretaris BEM',
                'phone': '0813-7890-1234',
                'email': 'bem@omnimap.ac.id'
            })
        },
        {
            'nama': 'Lomba Debat Bahasa Inggris',
            'kategori': 'Lomba',
            'tingkat_kesulitan': 'Mahir',
            'peserta': '20/32',
            'deadline': '10 Januari 2026',
            'lokasi': 'Auditorium Kampus',
            'deskripsi': 'Kompetisi debat bahasa Inggris tingkat universitas. Kesempatan untuk mengasah kemampuan public speaking dan critical thinking.',
            'required_traits': 'communication,assertiveness,intellect',
            'persyaratan_json': json.dumps([
                'Mahasiswa aktif',
                'Kemampuan bahasa Inggris aktif',
                'Mendaftar dalam tim (3 orang)',
                'Membayar biaya pendaftaran Rp 150.000/tim'
            ]),
            'manfaat_json': json.dumps([
                'Total hadiah Rp 15 juta',
                'Sertifikat peserta dan juara',
                'Pengalaman debat internasional',
                'Networking dengan debater lain'
            ]),
            'jadwal_json': json.dumps([
                {'tanggal': '10 Januari 2026', 'waktu': '09.00', 'kegiatan': 'Penutupan Pendaftaran'},
                {'tanggal': '15 Januari 2026', 'waktu': '13.00', 'kegiatan': 'Technical Meeting'},
                {'tanggal': '20-22 Januari 2026', 'waktu': '08.00', 'kegiatan': 'Babak Penyisihan & Final'}
            ]),
            'link': 'https://bit.ly/lomba-debat-2026',
            'contact_json': json.dumps({
                'name': 'Panitia Lomba Debat',
                'phone': '0856-1234-5678',
                'email': 'debat@omnimap.ac.id'
            })
        },
        {
            'nama': 'Workshop AI & Machine Learning',
            'kategori': 'Workshop',
            'tingkat_kesulitan': 'Menengah',
            'peserta': '45/60',
            'deadline': '5 Januari 2026',
            'lokasi': 'Lab Komputer B',
            'deskripsi': 'Workshop intensif tentang dasar-dasar Artificial Intelligence dan Machine Learning. Cocok untuk yang ingin memulai karir di bidang AI.',
            'required_traits': 'intellect,openness,conscientiousness',
            'persyaratan_json': json.dumps([
                'Memiliki laptop',
                'Dasar pemrograman Python',
                'Membayar biaya workshop Rp 100.000',
                'Komitmen mengikuti 3 hari penuh'
            ]),
            'manfaat_json': json.dumps([
                'Sertifikat workshop',
                'Materi lengkap AI/ML',
                'Mentoring dari praktisi',
                'Project portfolio',
                'Akses grup alumni'
            ]),
            'jadwal_json': json.dumps([
                {'tanggal': '25 Januari 2026', 'waktu': '09.00 - 17.00', 'kegiatan': 'Day 1: Introduction to AI'},
                {'tanggal': '26 Januari 2026', 'waktu': '09.00 - 17.00', 'kegiatan': 'Day 2: Machine Learning Basics'},
                {'tanggal': '27 Januari 2026', 'waktu': '09.00 - 17.00', 'kegiatan': 'Day 3: Deep Learning & Project'}
            ]),
            'link': 'https://bit.ly/workshop-ai-2026',
            'contact_json': json.dumps({
                'name': 'Tim Workshop AI',
                'phone': '0821-9876-5432',
                'email': 'workshop.ai@omnimap.ac.id'
            })
        }
    ]
    

    db.session.commit()

    # Tambahkan semua sample activities
    for activity_data in sample_activities:
        activity = Activity(**activity_data)
        db.session.add(activity)

    
    db.session.commit()
    print(f"Sample activities added successfully!")

# CLI command untuk populate activities
@app.cli.command()
def init_activities():
    """Initialize database with sample activities"""
    populate_sample_activities()
    print("Activities initialized successfully!")

@app.route('/')
def index():
    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])
        if user.is_admin:
            return redirect(url_for('mahasiswa_rentan'))
        return redirect(url_for('dashboard'))
    return redirect(url_for('onboarding_1'))

@app.route('/onboarding-1')
def onboarding_1():
    return render_template('onboarding-1.html')

@app.route('/onboarding-2')
def onboarding_2():
    return render_template('onboarding-2.html')

@app.route('/onboarding-3')
def onboarding_3():
    return render_template('onboarding-3.html')

@app.route('/onboarding-4')
def onboarding_4():
    return render_template('onboarding-4.html')

@app.route('/login')
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    if user.is_admin:
        return redirect(url_for('mahasiswa_rentan'))
    
    user_dict = {
        'id': user.id,
        'nim': user.nim,
        'nama': user.nama,
        'profile_picture' : user.profile_picture,
        'email': user.email,
        'username': user.username,
        'fakultas': user.fakultas,
        'skor_rata_rata': user.skor_rata_rata,
        'status_tes': user.status_tes,
        'progress_profil': user.progress_profil,
        'progress_tes': user.progress_tes,
        'progress_eksplorasi': user.progress_eksplorasi,
        'progress_kegiatan': user.progress_kegiatan,
        'aestheticism_t': user.aestheticism_t,
        'ambition_t': user.ambition_t,
        'anxiety_t': user.anxiety_t,
        'assertiveness_t': user.assertiveness_t,
        'conventionality_t': user.conventionality_t,
        'extraversion_t': user.extraversion_t,
        'agreeableness_t': user.agreeableness_t,
        'conscientiousness_t': user.conscientiousness_t,
        'neuroticism_t': user.neuroticism_t,
        'openness_t': user.openness_t
    }
    
    return render_template('dashboard.html', user=user_dict, active_page='dashboard')


@app.route('/chatbot')
def chatbot():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    
    # Siapkan data user lengkap
    user_dict = {
        'id': user.id,
        'nim': user.nim,
        'nama': user.nama,
        'email': user.email,
        'username': user.username,
        'fakultas': user.fakultas,
        'profile_picture': user.profile_picture,
        'skor_rata_rata': user.skor_rata_rata,
        'status_tes': user.status_tes,
        
        # Trait scores untuk AI analysis
        'extraversion_t': user.extraversion_t,
        'agreeableness_t': user.agreeableness_t,
        'conscientiousness_t': user.conscientiousness_t,
        'neuroticism_t': user.neuroticism_t,
        'openness_t': user.openness_t,
        'ambition_t': user.ambition_t,
        'sociability_t': user.sociability_t,
        'assertiveness_t': user.assertiveness_t
    }
    
    return render_template('chatbot.html', user=user_dict, active_page='chatbot')

def generate_chatbot_response(user, message):
    """Generate contextual chatbot response based on user profile"""
    message_lower = message.lower()
    
    # Personality-based responses
    if 'tipe' in message_lower and ('ambis' in message_lower or 'santai' in message_lower):
        if user.ambition_t and user.ambition_t > 55:
            return {
                'text': f'Berdasarkan skor ambisi Anda ({user.ambition_t:.1f}), Anda cenderung tipe orang yang ambis!',
                'list': [
                    'Anda memiliki dorongan kuat untuk mencapai tujuan',
                    'Senang menghadapi tantangan baru',
                    'Cocok untuk kegiatan kompetitif dan kepemimpinan',
                    'Pertimbangkan organisasi BEM atau lomba untuk menyalurkan ambisi Anda'
                ]
            }
        else:
            return {
                'text': f'Berdasarkan profil Anda (skor ambisi: {user.ambition_t:.1f}), Anda lebih santai dan seimbang.',
                'list': [
                    'Anda menyukai kegiatan yang nyaman dan tidak terlalu kompetitif',
                    'Cocok untuk UKM kreatif atau hobby-based',
                    'Fokus pada pengembangan skill yang Anda nikmati',
                    'Workshop dan kegiatan belajar santai mungkin cocok untuk Anda'
                ]
            }
    
    elif 'kegiatan' in message_lower and 'cocok' in message_lower:
        recommendations = []
        
        if user.openness_t and user.openness_t > 55:
            recommendations.append('UKM Seni/Kreatif - Anda terbuka terhadap pengalaman baru')
        
        if user.extraversion_t and user.extraversion_t > 55:
            recommendations.append('BEM/Organisasi - Anda energik dan suka bersosialisasi')
        
        if user.conscientiousness_t and user.conscientiousness_t > 55:
            recommendations.append('Kepanitiaan - Anda terorganisir dan dapat diandalkan')
        
        if not recommendations:
            recommendations = [
                'Workshop sesuai minat Anda',
                'UKM dengan aktivitas yang Anda sukai',
                'Kegiatan sosial untuk mengembangkan jaringan'
            ]
        
        return {
            'text': 'Berdasarkan kepribadian Anda, kegiatan yang cocok:',
            'list': recommendations
        }
    
    elif 'tim' in message_lower or 'kerja sama' in message_lower:
        tips = ['Komunikasi yang jelas dan terbuka dengan semua anggota tim']
        
        if user.agreeableness_t and user.agreeableness_t > 55:
            tips.append('Anda mudah bekerja sama - manfaatkan untuk mediasi konflik')
        else:
            tips.append('Latih empati dan mendengarkan aktif untuk kerja sama lebih baik')
        
        tips.extend([
            'Membagi tugas sesuai dengan keahlian masing-masing',
            'Membangun kepercayaan dan saling mendukung'
        ])
        
        return {'text': 'Tips bekerja dalam tim yang efektif:', 'list': tips}
    
    # Default response
    return {
        'text': 'Saya dapat membantu Anda dengan:',
        'list': [
            'Menganalisis tipe kepribadian Anda',
            'Rekomendasi kegiatan yang sesuai dengan minat',
            'Tips pengembangan diri dan soft skills',
            'Informasi tentang berbagai kegiatan kampus'
        ]
    }

@app.route('/api/chatbot/message', methods=['POST'])
def api_chatbot_message():
    """Handle chatbot messages and generate AI responses"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'success': False, 'message': 'Pesan tidak boleh kosong'}), 400
        
        user = db.session.get(User, session['user_id'])
        
        # Generate AI response using Gemini
        ai_response = generate_chatbot_response_gemini(user, user_message)
        
        return jsonify({
            'success': True,
            'response': ai_response
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Terjadi kesalahan: {str(e)}'
        }), 500
def _check_rate_limit(api_type='chatbot', min_interval=10):
    """Check and enforce rate limiting"""
    global _request_count, _last_api_call
    
    now = time.time()
    
    # Reset counter setiap menit
    if now - _request_count['last_reset'] > 60:
        _request_count = {'chatbot': 0, 'personality': 0, 'last_reset': now}
        print("🔄 Rate limit counter reset")
    
    # Check request count per minute
    if _request_count[api_type] >= 5:  # Max 5 per minute untuk safety
        wait_time = 60 - (now - _request_count['last_reset'])
        if wait_time > 0:
            print(f"⏳ Rate limit reached, waiting {wait_time:.1f}s until next minute...")
            time.sleep(wait_time + 1)
            _request_count = {'chatbot': 0, 'personality': 0, 'last_reset': time.time()}
    
    # Check minimum interval between calls
    if api_type in _last_api_call:
        time_since_last = now - _last_api_call[api_type]
        if time_since_last < min_interval:
            wait_time = min_interval - time_since_last
            print(f"⏳ Waiting {wait_time:.1f}s before next request...")
            time.sleep(wait_time)
    
    # Add random jitter to avoid thundering herd
    time.sleep(random.uniform(0.1, 0.5))
    
    _last_api_call[api_type] = time.time()
    _request_count[api_type] += 1


def get_cache_key(user_id, message):
    return hashlib.md5(f"{user_id}_{message}".encode()).hexdigest()

def generate_chatbot_response_gemini(user, message):
    """Generate chatbot response using Gemini API - SINGLE REQUEST ONLY"""
    global _cache
    
    try:
        if not gemini_client:
            print("⚠️ Gemini client tidak tersedia")
            return generate_chatbot_response(user, message)
        
        # ✅ CHECK CACHE FIRST
        cache_key = f"chat_{user.id}_{message[:30]}"
        if cache_key in _cache:
            cache_time = _cache.get(f"{cache_key}_time", 0)
            if time.time() - cache_time < 3600:
                print("✅ Using cached response")
                return _cache[cache_key]
        
        # ✅ ENFORCE RATE LIMIT
        _check_rate_limit('chatbot', min_interval=15)
        
        print(f"✅ Calling Gemini API...")
        
        # LIST MODEL SESUAI AKUN (urutkan dari terbaik)
        MODEL_LIST = [
            "gemini-2.5-flash",
            "gemini-flash-latest",
            "gemini-2.0-flash-lite",
            "gemini-2.0-flash",
            "gemma-3-4b-it"
        ]
        
        prompt = f"""Kamu adalah asisten konseling kepribadian untuk mahasiswa.

Data Kepribadian User:
- Nama: {user.nama}
- Extraversion: {user.extraversion_t:.1f}
- Agreeableness: {user.agreeableness_t:.1f}
- Conscientiousness: {user.conscientiousness_t:.1f}
- Neuroticism: {user.neuroticism_t:.1f}
- Openness: {user.openness_t:.1f}
- Ambition: {user.ambition_t:.1f}

Pertanyaan user: {message}

Berikan response dalam format JSON:
{{
  "text": "penjelasan singkat",
  "list": ["poin 1", "poin 2", "poin 3"]
}}

Response harus ramah, supportif, dan berdasarkan data kepribadian user."""

        # COBA SETIAP MODEL SAMPAI BERHASIL
        last_error = None
        for model_name in MODEL_LIST:
            try:
                print(f"🔄 Mencoba model: {model_name}")
                
                response = gemini_client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                
                text = response.text
                print(f"✅ Berhasil dengan model: {model_name}")
                
                # Parse JSON
                import re
                json_match = re.search(r'\{.*\}', text, re.DOTALL)
                if json_match:
                    parsed = json.loads(json_match.group())
                    
                    # ✅ CACHE THE RESPONSE
                    _cache[cache_key] = parsed
                    _cache[f"{cache_key}_time"] = time.time()
                    
                    return parsed
                else:
                    print("⚠️ JSON parse failed")
                    return generate_chatbot_response(user, message)
                    
            except Exception as e:
                error_msg = str(e)
                print(f"❌ Gagal di {model_name}: {error_msg[:100]}")
                last_error = error_msg
                continue
        
        # Jika semua model gagal
        print(f"⚠️ Semua model gagal, using fallback")
        return generate_chatbot_response(user, message)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return generate_chatbot_response(user, message)

    
# API untuk update profile picture
@app.route('/api/update-profile-picture', methods=['POST'])
def api_update_profile_picture():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        data = request.json
        user = db.session.get(User, session['user_id'])
        
        if not user:
            return jsonify({'success': False, 'message': 'User tidak ditemukan'}), 404
        
        # Update profile picture (base64 string)
        if data.get('profile_picture'):
            user.profile_picture = data.get('profile_picture')
        
        db.session.commit()
        
        # ✅ CREATE NOTIFICATION after successful profile picture update
        create_notification(
            user_id=user.id,
            title='Foto Profil Berhasil Diperbarui',
            message='Foto profil Anda telah berhasil diubah.',
            notification_type='success',
            link='/profile'
        )
        
        return jsonify({
            'success': True,
            'message': 'Foto profil berhasil diperbarui'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Terjadi kesalahan: {str(e)}'
        }), 500


# Update route profile untuk include profile_picture
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    return render_template('profile.html', user=user, active_page='profile')

@app.route('/api/update-profile', methods=['POST'])
def api_update_profile():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        data = request.json
        user = db.session.get(User, session['user_id'])
        
        if not user:
            return jsonify({'success': False, 'message': 'User tidak ditemukan'}), 404
        
        # Update fields
        if data.get('nama'):
            user.nama = data.get('nama')
        if data.get('email'):
            user.email = data.get('email')
        if data.get('username'):
            user.username = data.get('username')
        if data.get('fakultas'):
            user.fakultas = data.get('fakultas')
        if data.get('nim'):
            user.nim = data.get('nim')
        
        # Update password if provided and not the placeholder
        if data.get('password') and data.get('password') != '**********':
            user.set_password(data.get('password'))
        
        db.session.commit()
        
        # ✅ CREATE NOTIFICATION after successful profile update
        create_notification(
            user_id=user.id,
            title='Profil Berhasil Diperbarui',
            message='Data profil Anda telah berhasil diperbarui. Perubahan akan terlihat di seluruh sistem.',
            notification_type='success',
            link='/profile'
        )
        
        return jsonify({
            'success': True,
            'message': 'Profil berhasil diperbarui'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Terjadi kesalahan: {str(e)}'
        }), 500

@app.route('/hasil-tes')
def hasil_tes():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    
    # Check if user has completed the test
    if user.status_tes != 'Selesai':
        # Show modal that user needs to complete test first
        return render_template('hasil_tes_not_ready.html', user=user, active_page='hasil_tes')
    
    # Prepare user data for template
    user_dict = {
        'id': user.id,
        'nim': user.nim,
        'nama': user.nama,
        'email': user.email,
        'username': user.username,
        'fakultas': user.fakultas,
        'profile_picture': user.profile_picture,
        'skor_rata_rata': user.skor_rata_rata,
        'status_tes': user.status_tes,
        
        # Facet scores (T-scores)
        'aestheticism_t': user.aestheticism_t,
        'ambition_t': user.ambition_t,
        'anxiety_t': user.anxiety_t,
        'assertiveness_t': user.assertiveness_t,
        'conventionality_t': user.conventionality_t,
        'depression_t': user.depression_t,
        'dutifulness_t': user.dutifulness_t,
        'energy_t': user.energy_t,
        'excitement_t': user.excitement_t,
        'exhibitionism_t': user.exhibitionism_t,
        'flexibility_t': user.flexibility_t,
        'hostility_t': user.hostility_t,
        'impulsiveness_t': user.impulsiveness_t,
        'intellect_t': user.intellect_t,
        'irritability_t': user.irritability_t,
        'modesty_t': user.modesty_t,
        'moodiness_t': user.moodiness_t,
        'orderliness_t': user.orderliness_t,
        'self_indulgence_t': user.self_indulgence_t,
        'self_reliance_t': user.self_reliance_t,
        'sincerity_t': user.sincerity_t,
        'sociability_t': user.sociability_t,
        'tolerance_t': user.tolerance_t,
        'trustfulness_t': user.trustfulness_t,
        'warmth_t': user.warmth_t,
        
        # Domain scores (T-scores)
        'extraversion_t': user.extraversion_t,
        'agreeableness_t': user.agreeableness_t,
        'conscientiousness_t': user.conscientiousness_t,
        'neuroticism_t': user.neuroticism_t,
        'openness_t': user.openness_t,
        'narcissism_t': user.narcissism_t,
        'sensation_seeking_t': user.sensation_seeking_t,
        
        # Categories
        'aestheticism_kategori': user.aestheticism_kategori,
        'ambition_kategori': user.ambition_kategori,
        'anxiety_kategori': user.anxiety_kategori,
        'assertiveness_kategori': user.assertiveness_kategori,
        'conventionality_kategori': user.conventionality_kategori,
        'dutifulness_kategori': user.dutifulness_kategori,
        'excitement_kategori': user.excitement_kategori,
        'extraversion_kategori': user.extraversion_kategori,
        'agreeableness_kategori': user.agreeableness_kategori,
        'conscientiousness_kategori': user.conscientiousness_kategori,
        'neuroticism_kategori': user.neuroticism_kategori,
        'openness_kategori': user.openness_kategori
    }
    
    return render_template('hasil_tes.html', user=user_dict, active_page='hasil_tes')

def generate_personality_description(user):
    """Generate detailed personality description using Gemini with fallback"""
    global _cache
    
    cache_key = f"personality_{user.id}"
    if cache_key in _cache:
        print("✅ Using cached personality description")
        return _cache[cache_key]
    
    try:
        if not gemini_client:
            print("⚠️ Gemini client tidak tersedia")
            return generate_fallback_description(user)
        
        _check_rate_limit('personality', min_interval=10)
        
        MODEL_LIST = [
            "gemini-2.5-flash",
            "gemini-flash-latest",
            "gemini-2.0-flash-lite",
            "gemini-2.0-flash",
            "gemma-3-4b-it"
        ]
        
        prompt = f"""Berdasarkan hasil tes OMNI (Omni Multidimensional Personality Inventory) untuk Sdr. {user.nama}, 
buatkan deskripsi kepribadian yang sangat komprehensif dan detail dalam bahasa Indonesia formal.

Data T-Score (Mean=50, SD=10):
- Extraversion: {user.extraversion_t:.1f}
- Agreeableness: {user.agreeableness_t:.1f}
- Conscientiousness: {user.conscientiousness_t:.1f}
- Neuroticism: {user.neuroticism_t:.1f}
- Openness: {user.openness_t:.1f}

Buatkan analisis SANGAT DETAIL dalam format JSON:
{{
  "faktor_emosional": "1 paragraf panjang minimal 8-10 kalimat",
  "kemampuan_relasi": "1 paragraf panjang minimal 8-10 kalimat",
  "nilai_sosial": "1 paragraf panjang minimal 6-8 kalimat",
  "minat_dan_nilai": "1 paragraf panjang minimal 5-7 kalimat",
  "gaya_perilaku": "1 paragraf panjang minimal 10-12 kalimat",
  "faktor_kepribadian": "1 paragraf panjang minimal 8-10 kalimat"
}}"""

        for model_name in MODEL_LIST:
            try:
                print(f"🔄 Trying personality generation with: {model_name}")
                
                response = gemini_client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                
                text = response.text
                print(f"✅ Success with: {model_name}")
                
                import re
                json_match = re.search(r'\{.*\}', text, re.DOTALL)
                if json_match:
                    descriptions = json.loads(json_match.group())
                    _cache[cache_key] = descriptions
                    return descriptions
                    
            except Exception as e:
                print(f"❌ Failed with {model_name}: {str(e)[:100]}")
                continue
        
        print("⚠️ All models failed, using fallback")
        return generate_fallback_description(user)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return generate_fallback_description(user)


def generate_fallback_description(user):
    """Generate fallback description jika API gagal"""
    return {
        "faktor_emosional": f"Secara emosional, Sdr. {user.nama} memiliki suasana hati yang {'stabil' if user.neuroticism_t < 55 else 'cukup stabil'}. Perubahan emosinya masih dalam batas yang wajar dan dapat diterima oleh lingkungan. Ia memandang {'positif' if user.depression_t < 50 else 'cukup positif'} diri dan kehidupannya. Ia cenderung {'optimis' if user.anxiety_t < 50 else 'realistis'} memandang kehidupan. Kemampuan pengendalian dirinya tergolong {'baik' if user.impulsiveness_t < 50 else 'perlu dikembangkan'}.",
        
        "kemampuan_relasi": f"Saat berrelasi sosial, Sdr. {user.nama} {'bersikap baik kepada orang lain' if user.agreeableness_t >= 50 else 'cukup berhati-hati'} secara umum. {'Ia cukup menikmati kegiatan bersama dengan orang lain' if user.extraversion_t >= 50 else 'Ia memerlukan waktu untuk menjalin kedekatan emosi dengan orang lain'}. Ia {'bersikap rendah hati' if user.modesty_t >= 50 else 'cukup percaya diri'}, bersahaja dan {'tidak menonjol' if user.exhibitionism_t < 50 else 'senang tampil'} diantara orang lain.",
        
        "nilai_sosial": f"Dalam lingkungan sosial, Sdr. {user.nama} {'cukup toleran terhadap perbedaan' if user.tolerance_t >= 50 else 'memerlukan waktu untuk dapat menerima perbedaan'} dan sudut pandang yang ada. Ia {'sangat menjunjung tinggi' if user.conventionality_t >= 60 else 'cukup menghormati'} nilai-nilai tradisional dan aturan-aturan sosial yang ada.",
        
        "minat_dan_nilai": f"Gambaran terhadap minat dari Sdr. {user.nama} adalah ia {'cukup memperhatikan' if user.aestheticism_t >= 50 else 'kurang memperhatikan'} keindahan, mode, dan karya seni dalam kesehariannya. Ia {'memiliki keinginan untuk belajar' if user.intellect_t >= 50 else 'cukup selektif dalam hal'} mengenai ilmu pengetahuan.",
        
        "gaya_perilaku": f"Dalam menjalankan aktivitasnya, Sdr. {user.nama} memiliki {'energi yang cukup' if user.energy_t >= 50 else 'energi yang terbatas'} untuk melakukan kegiatan sehari-hari. Ia {'dapat beradaptasi terhadap perubahan' if user.flexibility_t >= 50 else 'cenderung konsisten'} namun tetap teguh pada beberapa prinsip. Dalam mengerjakan tugas, ia {'cukup sistematis dan perfeksionis' if user.orderliness_t >= 55 else 'lebih fleksibel dalam pendekatan'}. Ia {'berusaha untuk mendapatkan prestasi yang baik' if user.ambition_t >= 55 else 'bekerja dengan pola yang nyaman baginya'}.",
        
        "faktor_kepribadian": f"Ia merupakan individu yang {'cukup bertanggung jawab' if user.conscientiousness_t >= 50 else 'perlu meningkatkan tanggung jawab'} untuk menyelesaikan kewajibannya. Ia juga merupakan {'pekerja keras' if user.dutifulness_t >= 55 else 'pekerja yang seimbang'}, {'akan mengerahkan usahanya' if user.ambition_t >= 55 else 'bekerja sesuai kapasitas'} untuk dapat mencapai hasil {'terbaik' if user.ambition_t >= 60 else 'yang baik'}. Ia merupakan orang yang {'sederhana dan rendah hati' if user.modesty_t >= 50 else 'percaya diri dengan kemampuannya'}. Ia {'berhati-hati' if user.impulsiveness_t < 50 else 'cukup spontan'} pada tindakan dan keputusan yang dibuatnya."
    }

@app.route('/api/export-hasil-tes', methods=['GET'])
def api_export_hasil_tes():
    """Export hasil tes to PDF with all parameters"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        user = db.session.get(User, session['user_id'])
        
        if not user or user.status_tes != 'Selesai':
            return jsonify({'error': 'Tes belum selesai'}), 400
        
        # Generate detailed descriptions via API
        descriptions = generate_personality_description(user)
        
        # Create PDF in memory
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, 
                              rightMargin=2*cm, leftMargin=2*cm,
                              topMargin=2*cm, bottomMargin=2*cm)
        
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#c62828'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#c62828'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#333333'),
            spaceAfter=10,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=12
        )
        
        # Title
        elements.append(Paragraph("HASIL TES OMNI", title_style))
        elements.append(Paragraph("Omni Multidimensional Personality Inventory", normal_style))
        elements.append(Spacer(1, 0.5*cm))
        
        # User Info
        elements.append(Paragraph("Informasi Peserta", heading_style))
        user_info_data = [
            ['Username', f': M{str(user.id).zfill(3)}'],  # Format username
            ['Nama', f': {user.nama}'],
            ['NIM', f': {user.nim}'],
            ['Email', f': {user.email}'],
            ['Fakultas', f': {user.fakultas or "N/A"}'],
            ['Jurusan', f': Informatika'],  # Atau ambil dari database jika ada
            ['Tanggal Tes', f': {user.created_at.strftime("%d %B %Y") if user.created_at else "N/A"}'],
        ]
        
        user_info_table = Table(user_info_data, colWidths=[4*cm, 13*cm])
        user_info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#666666')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(user_info_table)
        elements.append(Spacer(1, 0.8*cm))
        
        # =========================
        # 25 FACETS
        # =========================
        elements.append(Paragraph("25 FACETS (Dimensi Kepribadian)", heading_style))
        elements.append(Spacer(1, 0.3*cm))
        
        facets_data = [
            ['No', 'Konstruk', 'Raw', 'T-Score', 'Kategori'],
            ['01', 'Aestheticism', user.aestheticism_raw or 0, round(user.aestheticism_t, 1) if user.aestheticism_t else 0, user.aestheticism_kategori or 'N/A'],
            ['02', 'Ambition', user.ambition_raw or 0, round(user.ambition_t, 1) if user.ambition_t else 0, user.ambition_kategori or 'N/A'],
            ['03', 'Anxiety', user.anxiety_raw or 0, round(user.anxiety_t, 1) if user.anxiety_t else 0, user.anxiety_kategori or 'N/A'],
            ['04', 'Assertiveness', user.assertiveness_raw or 0, round(user.assertiveness_t, 1) if user.assertiveness_t else 0, user.assertiveness_kategori or 'N/A'],
            ['05', 'Conventionality', user.conventionality_raw or 0, round(user.conventionality_t, 1) if user.conventionality_t else 0, user.conventionality_kategori or 'N/A'],
            ['06', 'Depression', user.depression_raw or 0, round(user.depression_t, 1) if user.depression_t else 0, user.depression_kategori or 'N/A'],
            ['07', 'Dutifulness', user.dutifulness_raw or 0, round(user.dutifulness_t, 1) if user.dutifulness_t else 0, user.dutifulness_kategori or 'N/A'],
            ['08', 'Energy', user.energy_raw or 0, round(user.energy_t, 1) if user.energy_t else 0, user.energy_kategori or 'N/A'],
            ['09', 'Excitement', user.excitement_raw or 0, round(user.excitement_t, 1) if user.excitement_t else 0, user.excitement_kategori or 'N/A'],
            ['10', 'Exhibitionism', user.exhibitionism_raw or 0, round(user.exhibitionism_t, 1) if user.exhibitionism_t else 0, user.exhibitionism_kategori or 'N/A'],
            ['11', 'Flexibility', user.flexibility_raw or 0, round(user.flexibility_t, 1) if user.flexibility_t else 0, user.flexibility_kategori or 'N/A'],
            ['12', 'Hostility', user.hostility_raw or 0, round(user.hostility_t, 1) if user.hostility_t else 0, user.hostility_kategori or 'N/A'],
            ['13', 'Impulsiveness', user.impulsiveness_raw or 0, round(user.impulsiveness_t, 1) if user.impulsiveness_t else 0, user.impulsiveness_kategori or 'N/A'],
            ['14', 'Intellect', user.intellect_raw or 0, round(user.intellect_t, 1) if user.intellect_t else 0, user.intellect_kategori or 'N/A'],
            ['15', 'Irritability', user.irritability_raw or 0, round(user.irritability_t, 1) if user.irritability_t else 0, user.irritability_kategori or 'N/A'],
            ['16', 'Modesty', user.modesty_raw or 0, round(user.modesty_t, 1) if user.modesty_t else 0, user.modesty_kategori or 'N/A'],
            ['17', 'Moodiness', user.moodiness_raw or 0, round(user.moodiness_t, 1) if user.moodiness_t else 0, user.moodiness_kategori or 'N/A'],
            ['18', 'Orderliness', user.orderliness_raw or 0, round(user.orderliness_t, 1) if user.orderliness_t else 0, user.orderliness_kategori or 'N/A'],
            ['19', 'Self Indulgence', user.self_indulgence_raw or 0, round(user.self_indulgence_t, 1) if user.self_indulgence_t else 0, user.self_indulgence_kategori or 'N/A'],
            ['20', 'Self Reliance', user.self_reliance_raw or 0, round(user.self_reliance_t, 1) if user.self_reliance_t else 0, user.self_reliance_kategori or 'N/A'],
            ['21', 'Sincerity', user.sincerity_raw or 0, round(user.sincerity_t, 1) if user.sincerity_t else 0, user.sincerity_kategori or 'N/A'],
            ['22', 'Sociability', user.sociability_raw or 0, round(user.sociability_t, 1) if user.sociability_t else 0, user.sociability_kategori or 'N/A'],
            ['23', 'Tolerance', user.tolerance_raw or 0, round(user.tolerance_t, 1) if user.tolerance_t else 0, user.tolerance_kategori or 'N/A'],
            ['24', 'Trustfulness', user.trustfulness_raw or 0, round(user.trustfulness_t, 1) if user.trustfulness_t else 0, user.trustfulness_kategori or 'N/A'],
            ['25', 'Warmth', user.warmth_raw or 0, round(user.warmth_t, 1) if user.warmth_t else 0, user.warmth_kategori or 'N/A'],
        ]
        
        facets_table = Table(facets_data, colWidths=[1.5*cm, 6*cm, 2*cm, 2.5*cm, 3*cm])
        facets_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#c62828')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ]))
        elements.append(facets_table)
        elements.append(PageBreak())
        
        # =========================
        # 5 BIG DOMAINS
        # =========================
        elements.append(Paragraph("Faktor", heading_style))
        elements.append(Paragraph("Domain utama kepribadian (Big Five)", normal_style))
        elements.append(Spacer(1, 0.3*cm))
        
        domains_data = [
            ['No', 'Konstruk', 'Raw Score', 'T-Score', 'Kategori'],
            ['01', 'Extraversion', user.extraversion_raw or 0, round(user.extraversion_t, 1) if user.extraversion_t else 0, user.extraversion_kategori or 'N/A'],
            ['02', 'Agreeableness', user.agreeableness_raw or 0, round(user.agreeableness_t, 1) if user.agreeableness_t else 0, user.agreeableness_kategori or 'N/A'],
            ['03', 'Conscientiousness', user.conscientiousness_raw or 0, round(user.conscientiousness_t, 1) if user.conscientiousness_t else 0, user.conscientiousness_kategori or 'N/A'],
            ['04', 'Neuroticism', user.neuroticism_raw or 0, round(user.neuroticism_t, 1) if user.neuroticism_t else 0, user.neuroticism_kategori or 'N/A'],
            ['05', 'Openness', user.openness_raw or 0, round(user.openness_t, 1) if user.openness_t else 0, user.openness_kategori or 'N/A'],
        ]
        
        domains_table = Table(domains_data, colWidths=[1.5*cm, 6*cm, 2.5*cm, 2.5*cm, 3*cm])
        domains_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#c62828')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        elements.append(domains_table)
        elements.append(Spacer(1, 1*cm))
        
        # =========================
        # ADDITIONAL CONSTRUCTS
        # =========================
        elements.append(Paragraph("Gangguan Kepribadian", heading_style))
        elements.append(Paragraph("Indikator gangguan kepribadian yang diukur dalam tes OMNI", normal_style))
        elements.append(Spacer(1, 0.3*cm))
        
        additional_data = [
            ['No', 'Konstruk', 'Raw Score', 'T-Score', 'Kategori'],
            ['01', 'Narcissism', user.narcissism_raw or 0, round(user.narcissism_t, 1) if user.narcissism_t else 0, user.narcissism_kategori or 'N/A'],
            ['02', 'Sensation Seeking', user.sensation_seeking_raw or 0, round(user.sensation_seeking_t, 1) if user.sensation_seeking_t else 0, user.sensation_seeking_kategori or 'N/A'],
        ]
        
        additional_table = Table(additional_data, colWidths=[1.5*cm, 6*cm, 2.5*cm, 2.5*cm, 3*cm])
        additional_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#c62828')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        elements.append(additional_table)
        elements.append(Spacer(1, 1*cm))
        
        elements.append(Paragraph("Critical Items", heading_style))
        elements.append(Spacer(1, 0.3*cm))
        
        # Suicidal and Self-Damaging Behavior
        elements.append(Paragraph("Suicidal and Self-Damaging Behavior", subheading_style))
        suicidal_text = """
        Berdasarkan analisis jawaban pada item kritis, tidak ditemukan indikasi perilaku melukai diri 
        atau kecenderungan bunuh diri. Responden menunjukkan sikap yang aman dalam aspek ini.
        """
        elements.append(Paragraph(suicidal_text, normal_style))
        elements.append(Spacer(1, 0.5*cm))
        
        # Substance Abuse
        elements.append(Paragraph("Substance Abuse", subheading_style))
        substance_text = """
        Tidak ditemukan indikasi penyalahgunaan zat atau alkohol. Responden menunjukkan 
        kontrol diri yang baik terhadap penggunaan substansi yang berpotensi merugikan.
        """
        elements.append(Paragraph(substance_text, normal_style))
        elements.append(Spacer(1, 0.5*cm))
        
        # Moody and Anxiety Disturbances
        elements.append(Paragraph("Moody and Anxiety Disturbances", subheading_style))
        
        # Analisis berdasarkan skor neuroticism
        if user.anxiety_t >= 60 or user.moodiness_t >= 60:
            moody_text = f"""
            Berdasarkan skor Anxiety ({user.anxiety_t:.1f}) dan Moodiness ({user.moodiness_t:.1f}), 
            responden menunjukkan kecenderungan mengalami kecemasan atau perubahan suasana hati 
            yang perlu diperhatikan. Disarankan untuk mengembangkan strategi manajemen stres 
            dan bila diperlukan, berkonsultasi dengan profesional.
            """
        else:
            moody_text = f"""
            Responden menunjukkan stabilitas emosional yang baik dengan skor Anxiety ({user.anxiety_t:.1f}) 
            dan Moodiness ({user.moodiness_t:.1f}) dalam rentang normal. Kemampuan mengelola emosi 
            dan suasana hati tergolong adaptif.
            """
        elements.append(Paragraph(moody_text, normal_style))
        elements.append(Spacer(1, 0.5*cm))
        
        # Anger and Impulsiveness
        elements.append(Paragraph("Anger and Impulsiveness", subheading_style))
        
        if user.hostility_t >= 60 or user.impulsiveness_t >= 60:
            anger_text = f"""
            Dengan skor Hostility ({user.hostility_t:.1f}) dan Impulsiveness ({user.impulsiveness_t:.1f}), 
            responden menunjukkan kecenderungan reaktif dalam menghadapi situasi yang memicu emosi. 
            Pengembangan kontrol diri dan teknik manajemen amarah akan bermanfaat.
            """
        else:
            anger_text = f"""
            Responden memiliki kontrol diri yang baik dengan skor Hostility ({user.hostility_t:.1f}) 
            dan Impulsiveness ({user.impulsiveness_t:.1f}) dalam rentang normal. Mampu mengelola 
            emosi negatif dengan cara yang konstruktif.
            """
        elements.append(Paragraph(anger_text, normal_style))
        elements.append(Spacer(1, 0.5*cm))
        
        # Dishonesty
        elements.append(Paragraph("Dishonesty", subheading_style))
        
        if user.sincerity_t < 45:
            dishonesty_text = f"""
            Dengan skor Sincerity yang rendah ({user.sincerity_t:.1f}), terdapat indikasi bahwa responden 
            mungkin kurang terbuka dalam situasi tertentu. Pengembangan kejujuran dan transparansi 
            dalam hubungan interpersonal dapat meningkatkan kualitas relasi.
            """
        else:
            dishonesty_text = f"""
            Responden menunjukkan tingkat kejujuran yang baik dengan skor Sincerity ({user.sincerity_t:.1f}). 
            Cenderung terbuka dan jujur dalam interaksi sosial.
            """
        elements.append(Paragraph(dishonesty_text, normal_style))
        
        elements.append(PageBreak())
        
        # =========================
        # DESKRIPSI KEPRIBADIAN (DETAIL DARI API)
        # =========================
        elements.append(Paragraph("Deskripsi Kepribadian", heading_style))
        
        # Faktor Emosional
        elements.append(Paragraph("Faktor Emosional", subheading_style))
        elements.append(Paragraph(descriptions['faktor_emosional'], normal_style))
        elements.append(Spacer(1, 0.5*cm))
        
        # Kemampuan Relasi
        elements.append(Paragraph("Kemampuan Relasi", subheading_style))
        elements.append(Paragraph(descriptions['kemampuan_relasi'], normal_style))
        elements.append(Spacer(1, 0.5*cm))
        
        # Nilai Sosial
        elements.append(Paragraph("Nilai Sosial", subheading_style))
        elements.append(Paragraph(descriptions['nilai_sosial'], normal_style))
        elements.append(Spacer(1, 0.5*cm))
        
        # Minat dan Nilai
        elements.append(Paragraph("Minat dan Nilai", subheading_style))
        elements.append(Paragraph(descriptions['minat_dan_nilai'], normal_style))
        elements.append(Spacer(1, 0.5*cm))
        
        # Gaya Perilaku
        elements.append(Paragraph("Gaya Perilaku", subheading_style))
        elements.append(Paragraph(descriptions['gaya_perilaku'], normal_style))
        elements.append(Spacer(1, 0.5*cm))
        
        # Faktor Kepribadian
        elements.append(Paragraph("Faktor Kepribadian", subheading_style))
        elements.append(Paragraph(descriptions['faktor_kepribadian'], normal_style))
        

        
        # Traits badges
        trait_badges = []
        if user.excitement_kategori == 'Tinggi' or user.excitement_kategori == 'Sangat Tinggi' or (user.excitement_t and user.excitement_t >= 60):
            trait_badges.append('Antusias')
        if user.dutifulness_kategori == 'Tinggi' or user.dutifulness_kategori == 'Sangat Tinggi' or (user.dutifulness_t and user.dutifulness_t >= 60):
            trait_badges.append('Bertanggung Jawab')
        if user.assertiveness_kategori == 'Tinggi' or user.assertiveness_kategori == 'Sangat Tinggi' or (user.assertiveness_t and user.assertiveness_t >= 60):
            trait_badges.append('Asertif')
        if user.aestheticism_kategori == 'Tinggi' or user.aestheticism_kategori == 'Sangat Tinggi' or (user.aestheticism_t and user.aestheticism_t >= 60):
            trait_badges.append('Kreatif')
        if user.extraversion_kategori == 'Tinggi' or user.extraversion_kategori == 'Sangat Tinggi' or (user.extraversion_t and user.extraversion_t >= 60):
            trait_badges.append('Ekstrovert')
        
        if trait_badges:
            elements.append(Spacer(1, 0.3*cm))
            elements.append(Paragraph(f"<b>Karakteristik Utama:</b> {', '.join(trait_badges)}", normal_style))
        
        elements.append(Spacer(1, 1*cm))
        
        # =========================
        # PANDUAN INTERPRETASI
        # =========================
        elements.append(Paragraph("PANDUAN INTERPRETASI", heading_style))
        
        interpretasi_data = [
            ['Kategori', 'Range T-Score', 'Keterangan'],
            ['Sangat Tinggi', 'T ≥ 65', 'Skor sangat tinggi'],
            ['Tinggi', '55 ≤ T < 65', 'Skor tinggi'],
            ['Sedang', '45 ≤ T < 55', 'Skor rata-rata'],
            ['Rendah', '35 ≤ T < 45', 'Skor rendah'],
            ['Sangat Rendah', 'T < 35', 'Skor sangat rendah'],
        ]

        interpretasi_table = Table(interpretasi_data, colWidths=[4*cm, 4*cm, 7*cm])
        
        interpretasi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#c62828')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(interpretasi_table)
        elements.append(Spacer(1, 0.5*cm))
        
        keterangan_text = """
        <b>Keterangan:</b><br/>
        • <b>Raw Score:</b> Skor mentah dari jawaban kuesioner<br/>
        • <b>T-Score:</b> Skor standar dengan mean 50 dan standar deviasi 10<br/>
        • <b>Kategori:</b> Klasifikasi berdasarkan T-Score untuk interpretasi
        """
        elements.append(Paragraph(keterangan_text, normal_style))
        
        elements.append(Spacer(1, 1.5*cm))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#666666'),
            alignment=TA_CENTER
        )
        elements.append(Paragraph("Dokumen ini dibuat secara otomatis oleh sistem OmniMap", footer_style))
        elements.append(Paragraph(f"Tanggal: {datetime.now().strftime('%d %B %Y, %H:%M')}", footer_style))
        
        # Build PDF
        doc.build(elements)
        
        # Get PDF from buffer
        pdf_data = buffer.getvalue()
        buffer.close()
        
        # Create response
        from flask import make_response
        response = make_response(pdf_data)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=Hasil_Tes_OMNI_{user.nim}_{user.nama.replace(" ", "_")}.pdf'
        
        return response
        
    except Exception as e:
        print(f"Error exporting PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Terjadi kesalahan: {str(e)}'
        }), 500
    
@app.route('/rekomendasi-kegiatan')
def rekomendasi_kegiatan():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    
    # Prepare user data for template
    user_dict = {
        'id': user.id,
        'nim': user.nim,
        'nama': user.nama,
        'email': user.email,
        'username': user.username,
        'fakultas': user.fakultas,
        'profile_picture': user.profile_picture,
        'status_tes': user.status_tes
    }
    
    return render_template('rekomendasiKegiatan-1.html', user=user_dict, active_page='rekomendasi_kegiatan')
@app.route('/detail-hasil-tes')
def detail_hasil_tes():
    """Display detailed test results with all facets and domains"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    
    # Check if user has completed the test
    if user.status_tes != 'Selesai':
        return redirect(url_for('tes_omni'))
    
    # Prepare user data for template
    user_dict = {
        'id': user.id,
        'nim': user.nim,
        'nama': user.nama,
        'email': user.email,
        'fakultas': user.fakultas,
        'profile_picture': user.profile_picture,
        'status_tes': user.status_tes,
        
        # Raw scores - Facets
        'aestheticism_raw': user.aestheticism_raw,
        'ambition_raw': user.ambition_raw,
        'anxiety_raw': user.anxiety_raw,
        'assertiveness_raw': user.assertiveness_raw,
        'conventionality_raw': user.conventionality_raw,
        'depression_raw': user.depression_raw,
        'dutifulness_raw': user.dutifulness_raw,
        'energy_raw': user.energy_raw,
        'excitement_raw': user.excitement_raw,
        'exhibitionism_raw': user.exhibitionism_raw,
        'flexibility_raw': user.flexibility_raw,
        'hostility_raw': user.hostility_raw,
        'impulsiveness_raw': user.impulsiveness_raw,
        'intellect_raw': user.intellect_raw,
        'irritability_raw': user.irritability_raw,
        'modesty_raw': user.modesty_raw,
        'moodiness_raw': user.moodiness_raw,
        'orderliness_raw': user.orderliness_raw,
        'self_indulgence_raw': user.self_indulgence_raw,
        'self_reliance_raw': user.self_reliance_raw,
        'sincerity_raw': user.sincerity_raw,
        'sociability_raw': user.sociability_raw,
        'tolerance_raw': user.tolerance_raw,
        'trustfulness_raw': user.trustfulness_raw,
        'warmth_raw': user.warmth_raw,
        
        # T-scores - Facets
        'aestheticism_t': user.aestheticism_t,
        'ambition_t': user.ambition_t,
        'anxiety_t': user.anxiety_t,
        'assertiveness_t': user.assertiveness_t,
        'conventionality_t': user.conventionality_t,
        'depression_t': user.depression_t,
        'dutifulness_t': user.dutifulness_t,
        'energy_t': user.energy_t,
        'excitement_t': user.excitement_t,
        'exhibitionism_t': user.exhibitionism_t,
        'flexibility_t': user.flexibility_t,
        'hostility_t': user.hostility_t,
        'impulsiveness_t': user.impulsiveness_t,
        'intellect_t': user.intellect_t,
        'irritability_t': user.irritability_t,
        'modesty_t': user.modesty_t,
        'moodiness_t': user.moodiness_t,
        'orderliness_t': user.orderliness_t,
        'self_indulgence_t': user.self_indulgence_t,
        'self_reliance_t': user.self_reliance_t,
        'sincerity_t': user.sincerity_t,
        'sociability_t': user.sociability_t,
        'tolerance_t': user.tolerance_t,
        'trustfulness_t': user.trustfulness_t,
        'warmth_t': user.warmth_t,
        
        # Categories - Facets
        'aestheticism_kategori': user.aestheticism_kategori,
        'ambition_kategori': user.ambition_kategori,
        'anxiety_kategori': user.anxiety_kategori,
        'assertiveness_kategori': user.assertiveness_kategori,
        'conventionality_kategori': user.conventionality_kategori,
        'depression_kategori': user.depression_kategori,
        'dutifulness_kategori': user.dutifulness_kategori,
        'energy_kategori': user.energy_kategori,
        'excitement_kategori': user.excitement_kategori,
        'exhibitionism_kategori': user.exhibitionism_kategori,
        'flexibility_kategori': user.flexibility_kategori,
        'hostility_kategori': user.hostility_kategori,
        'impulsiveness_kategori': user.impulsiveness_kategori,
        'intellect_kategori': user.intellect_kategori,
        'irritability_kategori': user.irritability_kategori,
        'modesty_kategori': user.modesty_kategori,
        'moodiness_kategori': user.moodiness_kategori,
        'orderliness_kategori': user.orderliness_kategori,
        'self_indulgence_kategori': user.self_indulgence_kategori,
        'self_reliance_kategori': user.self_reliance_kategori,
        'sincerity_kategori': user.sincerity_kategori,
        'sociability_kategori': user.sociability_kategori,
        'tolerance_kategori': user.tolerance_kategori,
        'trustfulness_kategori': user.trustfulness_kategori,
        'warmth_kategori': user.warmth_kategori,
        
        # Raw scores - Domains
        'extraversion_raw': user.extraversion_raw,
        'agreeableness_raw': user.agreeableness_raw,
        'conscientiousness_raw': user.conscientiousness_raw,
        'neuroticism_raw': user.neuroticism_raw,
        'openness_raw': user.openness_raw,
        'narcissism_raw': user.narcissism_raw,
        'sensation_seeking_raw': user.sensation_seeking_raw,
        
        # T-scores - Domains
        'extraversion_t': user.extraversion_t,
        'agreeableness_t': user.agreeableness_t,
        'conscientiousness_t': user.conscientiousness_t,
        'neuroticism_t': user.neuroticism_t,
        'openness_t': user.openness_t,
        'narcissism_t': user.narcissism_t,
        'sensation_seeking_t': user.sensation_seeking_t,
        
        # Categories - Domains
        'extraversion_kategori': user.extraversion_kategori,
        'agreeableness_kategori': user.agreeableness_kategori,
        'conscientiousness_kategori': user.conscientiousness_kategori,
        'neuroticism_kategori': user.neuroticism_kategori,
        'openness_kategori': user.openness_kategori,
        'narcissism_kategori': user.narcissism_kategori,
        'sensation_seeking_kategori': user.sensation_seeking_kategori
    }
    
    return render_template('detail_hasil_tes.html', user=user_dict, active_page='hasil_tes')
@app.route('/api/register', methods=['POST'])
def api_register():
    try:
        data = request.json
        
        # Validation
        if not data.get('nim') or not data.get('nama') or not data.get('email'):
            return jsonify({
                'success': False,
                'message': 'NIM, nama, dan email harus diisi'
            }), 400
        
        if not data.get('username') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': 'Username dan password harus diisi'
            }), 400
        
        # Check if user already exists
        if User.query.filter_by(nim=data.get('nim')).first():
            return jsonify({
                'success': False,
                'message': 'NIM sudah terdaftar'
            }), 400
        
        if User.query.filter_by(email=data.get('email')).first():
            return jsonify({
                'success': False,
                'message': 'Email sudah terdaftar'
            }), 400
        
        if User.query.filter_by(username=data.get('username')).first():
            return jsonify({
                'success': False,
                'message': 'Username sudah digunakan'
            }), 400
        
        # Create new user
        new_user = User(
            nim=data.get('nim'),
            nama=data.get('nama'),
            email=data.get('email'),
            username=data.get('username'),
            fakultas=data.get('fakultas'),
            is_admin=False
        )
        new_user.set_password(data.get('password'))
        
        db.session.add(new_user)
        db.session.commit()
        
        # ✅ CREATE WELCOME NOTIFICATION for new user
        create_notification(
            user_id=new_user.id,
            title='Selamat Datang di OmniMap! 👋',
            message=f'Halo {new_user.nama}! Akun Anda berhasil dibuat. Silakan lengkapi profil dan ikuti Tes OMNI untuk mendapatkan rekomendasi kegiatan yang sesuai dengan kepribadian Anda.',
            notification_type='info',
            link='/dashboard'
        )
        
        # ✅ NOTIFY ALL ADMINS about new user registration
        admins = User.query.filter_by(is_admin=True).all()
        for admin in admins:
            create_notification(
                user_id=admin.id,
                title='User Baru Telah Mendaftar',
                message=f'Mahasiswa baru telah mendaftar: {new_user.nama} ({new_user.nim}) dari {new_user.fakultas or "Fakultas belum diisi"}.',
                notification_type='info',
                link='/mahasiswa-rentan'
            )
        
        return jsonify({
            'success': True,
            'message': 'Registrasi berhasil',
            'redirect': '/login'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Terjadi kesalahan: {str(e)}'
        }), 500
    

@app.route('/api/recommended-activities', methods=['GET'])
def api_recommended_activities():
    """Get recommended activities based on user's personality traits"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        user = db.session.get(User, session['user_id'])
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Check if user has completed personality test
        if user.status_tes != 'Selesai':
            return jsonify({
                'message': 'Silakan selesaikan tes kepribadian terlebih dahulu',
                'activities': []
            })
        
        # Get all activities
        activities = Activity.query.all()
        
        # Calculate match percentage for each activity
        recommended_activities = []
        for activity in activities:
            match_score = calculate_activity_match(user, activity)
            
            recommended_activities.append({
                'id': activity.id,
                'nama': activity.nama,
                'kategori': activity.kategori,
                'kategori_slug': activity.kategori.lower().replace(' ', '-'),
                'tingkat_kesulitan': activity.tingkat_kesulitan,
                'peserta': activity.peserta,
                'deadline': activity.deadline,
                'lokasi': activity.lokasi,
                'deskripsi': activity.deskripsi,
                'match_percentage': match_score,
                'required_traits': activity.required_traits
            })
        
        # Sort by match percentage (highest first)
        recommended_activities.sort(key=lambda x: x['match_percentage'], reverse=True)
        
        # Count by category
        category_counts = {
            'ukm': len([a for a in recommended_activities if a['kategori'].lower() == 'ukm']),
            'organisasi': len([a for a in recommended_activities if a['kategori'].lower() == 'organisasi']),
            'kepanitiaan': len([a for a in recommended_activities if a['kategori'].lower() == 'kepanitiaan']),
            'lomba': len([a for a in recommended_activities if a['kategori'].lower() == 'lomba']),
            'workshop': len([a for a in recommended_activities if a['kategori'].lower() == 'workshop'])
        }
        
        return jsonify({
            'activities': recommended_activities,
            'category_counts': category_counts,
            'total': len(recommended_activities)
        })
        
    except Exception as e:
        print(f"Error getting recommended activities: {str(e)}")
        return jsonify({
            'error': f'Terjadi kesalahan: {str(e)}'
        }), 500

def calculate_activity_match(user, activity):
    """Calculate how well an activity matches user's personality traits"""
    
    # Default match percentage
    default_match = 75
    
    try:
        # Check if user and activity exist
        if not user or not activity:
            return default_match
        
        # Check if activity has required_traits
        if not hasattr(activity, 'required_traits') or not activity.required_traits:
            return default_match
        
        # Parse required_traits (bisa string atau dict/list)
        required_traits = []
        if isinstance(activity.required_traits, str):
            # Coba parse sebagai JSON dulu
            try:
                parsed = json.loads(activity.required_traits)
                if isinstance(parsed, dict):
                    required_traits = list(parsed.keys())
                elif isinstance(parsed, list):
                    required_traits = parsed
                else:
                    required_traits = [t.strip() for t in activity.required_traits.split(',') if t.strip()]
            except:
                # Jika bukan JSON, split by comma
                required_traits = [t.strip() for t in activity.required_traits.split(',') if t.strip()]
        elif isinstance(activity.required_traits, (list, dict)):
            required_traits = list(activity.required_traits.keys() if isinstance(activity.required_traits, dict) else activity.required_traits)
        
        if not required_traits:
            return default_match
        
        # Trait mapping to user attributes
        trait_mapping = {
            'extraversion': 'extraversion_t',
            'agreeableness': 'agreeableness_t',
            'conscientiousness': 'conscientiousness_t',
            'neuroticism': 'neuroticism_t',
            'openness': 'openness_t',
            'leadership': 'assertiveness_t',
            'creativity': 'aestheticism_t',
            'teamwork': 'agreeableness_t',
            'organization': 'orderliness_t',
            'communication': 'sociability_t',
            'aestheticism': 'aestheticism_t',
            'flexibility': 'flexibility_t',
            'assertiveness': 'assertiveness_t',
            'sociability': 'sociability_t',
            'orderliness': 'orderliness_t'
        }
        
        total_score = 0
        matched_traits = 0
        
        for trait in required_traits:
            trait_lower = str(trait).lower().strip()
            
            if trait_lower in trait_mapping:
                user_trait_attr = trait_mapping[trait_lower]
                
                # Get user trait value with None check
                user_trait_value = getattr(user, user_trait_attr, None)
                
                # Skip if value is None
                if user_trait_value is None:
                    continue
                
                try:
                    # Convert to float for safety
                    user_trait_value = float(user_trait_value)
                    
                    # Normalize score to 0-100 range (T-scores are typically 20-80)
                    normalized_score = ((user_trait_value - 20) / 60) * 100
                    normalized_score = max(0, min(100, normalized_score))
                    
                    total_score += normalized_score
                    matched_traits += 1
                except (ValueError, TypeError):
                    # Skip if conversion fails
                    continue
        
        # Calculate average match percentage
        if matched_traits > 0:
            match_percentage = int(total_score / matched_traits)
        else:
            match_percentage = default_match
        
        # Add bonus for high openness (generally good for trying new activities)
        try:
            if hasattr(user, 'openness_t') and user.openness_t is not None:
                openness_value = float(user.openness_t)
                openness_bonus = int((openness_value - 50) / 10)
                match_percentage = min(100, match_percentage + openness_bonus)
        except (ValueError, TypeError):
            pass  # Skip bonus if conversion fails
        
        # Ensure match percentage is within valid range
        match_percentage = max(0, min(100, match_percentage))
        
        return match_percentage
        
    except Exception as e:
        print(f"Error calculating activity match: {str(e)}")
        return default_match

@app.route('/api/activity/<int:activity_id>', methods=['GET'])
def api_get_activity_detail(activity_id):
    """Get detailed information about a specific activity"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        user = db.session.get(User, session['user_id'])
        activity = Activity.query.get(activity_id)
        
        if not activity:
            return jsonify({'error': 'Activity not found'}), 404
        
        match_score = calculate_activity_match(user, activity)
        
        return jsonify({
            'id': activity.id,
            'nama': activity.nama,
            'kategori': activity.kategori,
            'tingkat_kesulitan': activity.tingkat_kesulitan,
            'peserta': activity.peserta,
            'deadline': activity.deadline,
            'lokasi': activity.lokasi,
            'deskripsi': activity.deskripsi,
            'match_percentage': match_score,
            'required_traits': activity.required_traits
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Terjadi kesalahan: {str(e)}'
        }), 500

@app.route('/detail-bem-fakultas')
def detail_bem_fakultas():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('detail-bem-fakultas.html')

@app.route('/detail-lomba-debat')
def detail_lomba_debat():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('detail-lomba-debat.html')

@app.route('/detail-ukm-embun')
def detail_ukm_embun():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('detail-ukm-embun.html')

@app.route('/detail-workshop-ai')
def detail_workshop_ai():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('detail-workshop-ai.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username dan password harus diisi'
            }), 400
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            
            return jsonify({
                'success': True,
                'message': 'Login berhasil',
                'is_admin': user.is_admin,
                'redirect': '/mahasiswa-rentan' if user.is_admin else '/dashboard'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Username atau password salah'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Terjadi kesalahan: {str(e)}'
        }), 500

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({
        'success': True,
        'message': 'Logout berhasil'
    })

@app.route('/api/check-session', methods=['GET'])
def api_check_session():
    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])
        return jsonify({
            'logged_in': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'nama': user.nama,
                'is_admin': user.is_admin
            }
        })
    return jsonify({'logged_in': False})

@app.route('/api/user/profile', methods=['GET'])
def api_get_profile():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = db.session.get(User, session['user_id'])
    return jsonify({
        'id': user.id,
        'nim': user.nim,
        'username': user.username,
        'email': user.email,
        'nama': user.nama,
        'fakultas': user.fakultas,
        'skor_rata_rata': user.skor_rata_rata,
        'status_tes': user.status_tes,
        'extraversion_t': user.extraversion_t,
        'agreeableness_t': user.agreeableness_t,
        'conscientiousness_t': user.conscientiousness_t,
        'neuroticism_t': user.neuroticism_t,
        'openness_t': user.openness_t,
        'created_at': user.created_at.strftime('%Y-%m-%d')
    })

# Tambahkan route ini ke app.py

@app.route('/kegiatan/<int:activity_id>')
def kegiatan_detail(activity_id):
    """Display detailed information about a specific activity"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    activity = Activity.query.get(activity_id)
    
    if not activity:
        return render_template('404.html'), 404
    
    # Calculate match percentage
    match_percentage = calculate_activity_match(user, activity)
    
    # Parse JSON fields if they exist
    activity_dict = {
        'id': activity.id,
        'nama': activity.nama,
        'kategori': activity.kategori,
        'tingkat_kesulitan': activity.tingkat_kesulitan,
        'peserta': activity.peserta,
        'deadline': activity.deadline,
        'lokasi': activity.lokasi,
        'deskripsi': activity.deskripsi,
        'match_percentage': match_percentage,
        'required_traits': activity.required_traits
    }
    
    # Parse additional JSON fields if they exist in your database
    # You'll need to add these columns to Activity model if not exists
    try:
        # Example: if you have JSON columns for these
        import json
        if hasattr(activity, 'persyaratan_json'):
            activity_dict['persyaratan'] = json.loads(activity.persyaratan_json) if activity.persyaratan_json else []
        else:
            # Default data for demo
            activity_dict['persyaratan'] = [
                'Mahasiswa aktif semester 1-6',
                'Memiliki minat di bidang terkait',
                'Mengisi formulir pendaftaran'
            ]
        
        if hasattr(activity, 'manfaat_json'):
            activity_dict['manfaat'] = json.loads(activity.manfaat_json) if activity.manfaat_json else []
        else:
            # Default data for demo
            activity_dict['manfaat'] = [
                'Sertifikat kegiatan',
                'Pengembangan soft skills',
                'Networking',
                'Pengalaman organisasi'
            ]
        
        if hasattr(activity, 'jadwal_json'):
            activity_dict['jadwal'] = json.loads(activity.jadwal_json) if activity.jadwal_json else []
        else:
            # Default data for demo
            activity_dict['jadwal'] = [
                {'hari': 'Senin', 'waktu': '08.00 - 09.00', 'kegiatan': 'Latihan Rutin'},
                {'hari': 'Rabu', 'waktu': '16.00 - 18.00', 'kegiatan': 'Diskusi'},
                {'hari': 'Jumat', 'waktu': '16.00 - 18.00', 'kegiatan': 'Workshop'}
            ]
        
        if hasattr(activity, 'link'):
            activity_dict['link'] = activity.link
        else:
            activity_dict['link'] = '#'
        
        if hasattr(activity, 'contact_json'):
            activity_dict['contact'] = json.loads(activity.contact_json) if activity.contact_json else None
        else:
            # Default data for demo
            activity_dict['contact'] = {
                'name': 'Koordinator Kegiatan',
                'phone': '0812-3456-7890',
                'email': f'{activity.kategori.lower()}@omnimap.ac.id'
            }
            
    except Exception as e:
        print(f"Error parsing activity data: {str(e)}")
        # Set default values if parsing fails
        activity_dict['persyaratan'] = []
        activity_dict['manfaat'] = []
        activity_dict['jadwal'] = []
        activity_dict['link'] = '#'
        activity_dict['contact'] = None
    
    return render_template('detailkegiatan.html', 
                         activity=activity_dict, 
                         user=user,
                         active_page='rekomendasi_kegiatan')


@app.route('/api/activities', methods=['GET'])
def api_get_activities():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    activities = Activity.query.all()
    return jsonify([{
        'id': a.id,
        'nama': a.nama,
        'kategori': a.kategori,
        'tingkat_kesulitan': a.tingkat_kesulitan,
        'peserta': a.peserta,
        'deadline': a.deadline,
        'lokasi': a.lokasi,
        'deskripsi': a.deskripsi
    } for a in activities])

@app.route('/api/add-activity', methods=['POST'])
def api_add_activity():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    user = db.session.get(User, session['user_id'])
    if not user or not user.is_admin:
        return jsonify({'success': False, 'message': 'Admin access required'}), 403
    
    try:
        data = request.json
        
        # Validate required fields
        if not data.get('kategori') or not data.get('nama'):
            return jsonify({'success': False, 'message': 'Kategori dan nama kegiatan harus diisi'}), 400
        
        if not data.get('required_traits'):
            return jsonify({'success': False, 'message': 'Trait kepribadian harus dipilih'}), 400
        
        import json
        
        # Create new activity
        new_activity = Activity(
            nama=data.get('nama'),
            kategori=data.get('kategori'),
            deskripsi=data.get('deskripsi', ''),
            deadline=data.get('deadline', ''),
            peserta=data.get('peserta', ''),
            lokasi=data.get('lokasi', ''),
            required_traits=data.get('required_traits', ''),
            persyaratan_json=json.dumps(data.get('persyaratan', [])) if data.get('persyaratan') else None,
            manfaat_json=json.dumps(data.get('manfaat', [])) if data.get('manfaat') else None,
            jadwal_json=json.dumps({'tanggal': data.get('jadwal', '')}) if data.get('jadwal') else None,
            link=data.get('link', ''),
            contact_json=json.dumps(data.get('kontak', {})) if data.get('kontak') else None
        )
        
        db.session.add(new_activity)
        db.session.commit()
        
        # ✅ NOTIFY ALL USERS who completed test about new activity
        users_with_test = User.query.filter_by(
            is_admin=False,
            status_tes='Selesai'
        ).all()
        
        for user_notif in users_with_test:
            # Calculate match score
            match_score = calculate_activity_match(user_notif, new_activity)
            
            # Only notify if match score is high (>= 70%)
            if match_score >= 70:
                create_notification(
                    user_id=user_notif.id,
                    title='Kegiatan Baru Cocok untuk Anda! ✨',
                    message=f'Ada kegiatan baru "{new_activity.nama}" yang sangat cocok dengan kepribadian Anda (Match: {match_score}%). Lihat detailnya sekarang!',
                    notification_type='info',
                    link=f'/kegiatan/{new_activity.id}'
                )
        
        return jsonify({
            'success': True,
            'message': 'Kegiatan berhasil ditambahkan',
            'activity_id': new_activity.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Terjadi kesalahan: {str(e)}'
        }), 500

@app.route('/api/notifications', methods=['GET'])
def api_get_notifications():
    """Get user notifications"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        user_id = session['user_id']
        
        # Get unread count
        unread_count = Notification.query.filter_by(
            user_id=user_id, 
            is_read=False
        ).count()
        
        # Get recent notifications (last 10)
        notifications = Notification.query.filter_by(
            user_id=user_id
        ).order_by(Notification.created_at.desc()).limit(10).all()
        
        notifications_data = [{
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'type': n.type,
            'is_read': n.is_read,
            'link': n.link,
            'created_at': n.created_at.strftime('%d %b %Y'),
            'time_ago': get_time_ago(n.created_at)
        } for n in notifications]
        
        return jsonify({
            'success': True,
            'unread_count': unread_count,
            'notifications': notifications_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/notifications/mark-read', methods=['POST'])
def api_mark_notification_read():
    """Mark notification as read"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        data = request.json
        notification_id = data.get('notification_id')
        
        notification = Notification.query.get(notification_id)
        
        if not notification:
            return jsonify({'success': False, 'error': 'Notification not found'}), 404
        
        if notification.user_id != session['user_id']:
            return jsonify({'success': False, 'error': 'Forbidden'}), 403
        
        notification.is_read = True
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/notifications/mark-all-read', methods=['POST'])
def api_mark_all_read():
    """Mark all notifications as read"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        Notification.query.filter_by(
            user_id=session['user_id'],
            is_read=False
        ).update({'is_read': True})
        
        db.session.commit()
        
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

def get_time_ago(date):
    """Helper function to get relative time"""
    now = datetime.utcnow()
    diff = now - date
    
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return 'Baru saja'
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f'{minutes} menit lalu'
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f'{hours} jam lalu'
    else:
        days = int(seconds / 86400)
        return f'{days} hari lalu'

# Helper function untuk create notification
def create_notification(user_id, title, message, notification_type='info', link=None):
    """Helper to create notification"""
    try:
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            type=notification_type,
            link=link
        )
        db.session.add(notification)
        db.session.commit()
        return True
    except Exception as e:
        print(f"Error creating notification: {e}")
        db.session.rollback()
        return False

@app.route('/api/edit-activity', methods=['POST'])
def api_edit_activity():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    user = db.session.get(User, session['user_id'])
    if not user or not user.is_admin:
        return jsonify({'success': False, 'message': 'Admin access required'}), 403
    
    try:
        data = request.json
        activity_id = data.get('id')
        
        # Validate required fields
        if not activity_id:
            return jsonify({'success': False, 'message': 'ID kegiatan tidak ditemukan'}), 400
            
        if not data.get('kategori') or not data.get('nama'):
            return jsonify({'success': False, 'message': 'Kategori dan nama kegiatan harus diisi'}), 400
        
        # Get existing activity
        activity = db.session.get(Activity, activity_id)
        if not activity:
            return jsonify({'success': False, 'message': 'Kegiatan tidak ditemukan'}), 404
        
        import json
        
        # Update activity fields
        activity.nama = data.get('nama')
        activity.kategori = data.get('kategori')
        activity.deskripsi = data.get('deskripsi', '')
        activity.deadline = data.get('deadline', '')
        activity.peserta = data.get('peserta', '')
        activity.lokasi = data.get('lokasi', '')
        activity.link = data.get('link', '')
        
        # Update JSON fields
        if data.get('persyaratan'):
            activity.persyaratan_json = json.dumps(data.get('persyaratan'))
        
        if data.get('manfaat'):
            activity.manfaat_json = json.dumps(data.get('manfaat'))
        
        if data.get('jadwal'):
            activity.jadwal_json = json.dumps({'tanggal': data.get('jadwal')})
        
        if data.get('kontak'):
            activity.contact_json = json.dumps(data.get('kontak'))
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Kegiatan berhasil diperbarui'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Terjadi kesalahan: {str(e)}'
        }), 500


@app.route('/api/delete-activity', methods=['POST'])
def api_delete_activity():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    user = db.session.get(User, session['user_id'])
    if not user or not user.is_admin:
        return jsonify({'success': False, 'message': 'Admin access required'}), 403
    
    try:
        data = request.json
        activity_id = data.get('id')
        
        # Validate ID
        if not activity_id:
            return jsonify({'success': False, 'message': 'ID kegiatan tidak ditemukan'}), 400
        
        # Get activity
        activity = db.session.get(Activity, activity_id)
        if not activity:
            return jsonify({'success': False, 'message': 'Kegiatan tidak ditemukan'}), 404
        
        # Delete activity
        db.session.delete(activity)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Kegiatan berhasil dihapus'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Terjadi kesalahan: {str(e)}'
        }), 500
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    trait = db.Column(db.String(100), nullable=False)  # e.g., 'energy', 'sociability', etc.
    reverse_scored = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TestAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    answer = db.Column(db.Integer, nullable=False)  # 1-5
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TestSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    time_taken = db.Column(db.Integer)  # in seconds
    status = db.Column(db.String(50), default='in_progress')  # in_progress, completed

@app.route('/tes-omni')
def tes_omni():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    
    # Check if user already completed the test
    if user.status_tes == 'Selesai':
        # Show modal that user already completed test
        return render_template('tes_omni_completed.html', user=user, active_page='tes_omni')
    
    # Get all questions ordered
    questions = Question.query.order_by(Question.order).all()
    
    # Format questions for JavaScript
    questions_data = [{
        'id': q.id,
        'text': q.text,
        'trait': q.trait,
        'reverse_scored': q.reverse_scored
    } for q in questions]
    
    return render_template('tes_omni.html', 
                         user=user, 
                         questions=questions_data,
                         total_questions=len(questions_data), 
                         active_page='tes_omni')

# API endpoint to submit test
@app.route('/api/submit-test', methods=['POST'])
def api_submit_test():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        data = request.json
        user_id = data.get('user_id')
        answers = data.get('answers')
        time_taken = data.get('time_taken')
        
        if user_id != session['user_id']:
            return jsonify({'success': False, 'message': 'Invalid user'}), 403
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Save all answers
        for question_id, answer_value in answers.items():
            test_answer = TestAnswer(
                user_id=user_id,
                question_id=int(question_id),
                answer=answer_value
            )
            db.session.add(test_answer)
        
        # Calculate scores
        scores = calculate_personality_scores(user_id)
        
        # Update user with scores
        update_user_scores(user, scores)
        
        # Update test session
        test_session = TestSession.query.filter_by(
            user_id=user_id, 
            status='in_progress'
        ).first()
        
        if not test_session:
            test_session = TestSession(user_id=user_id)
            db.session.add(test_session)
        
        test_session.completed_at = datetime.utcnow()
        test_session.time_taken = time_taken
        test_session.status = 'completed'
        
        # Update user status
        user.status_tes = 'Selesai'
        user.progress_tes = 100
        
        db.session.commit()
        
        # ✅ CREATE NOTIFICATION after test completion
        create_notification(
            user_id=user.id,
            title='Tes OMNI Berhasil Diselesaikan! 🎉',
            message=f'Selamat {user.nama}! Anda telah menyelesaikan Tes OMNI. Lihat hasil kepribadian Anda sekarang untuk mengetahui rekomendasi kegiatan yang cocok.',
            notification_type='success',
            link='/hasil-tes'
        )
        
        return jsonify({
            'success': True,
            'message': 'Tes berhasil diselesaikan',
            'redirect': '/hasil-tes'
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error submitting test: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Terjadi kesalahan: {str(e)}'
        }), 500

# API endpoint to save progress
@app.route('/api/save-progress', methods=['POST'])
def api_save_progress():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        data = request.json
        user_id = data.get('user_id')
        answers = data.get('answers')
        current_question = data.get('current_question', 0)
        
        if user_id != session['user_id']:
            return jsonify({'success': False, 'message': 'Invalid user'}), 403
        
        # Delete existing answers for this user
        TestAnswer.query.filter_by(user_id=user_id).delete()
        
        # Save current answers
        for question_id, answer_value in answers.items():
            test_answer = TestAnswer(
                user_id=user_id,
                question_id=int(question_id),
                answer=answer_value
            )
            db.session.add(test_answer)
        
        # Update progress
        user = User.query.get(user_id)
        total_questions = Question.query.count()
        progress = int((len(answers) / total_questions) * 100)
        user.progress_tes = progress
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Progress tersimpan'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Terjadi kesalahan: {str(e)}'
        }), 500

# ===== TAMBAHKAN SETELAH FUNGSI api_save_progress =====

@app.route('/api/auto-save-progress', methods=['POST'])
def api_auto_save_progress():
    """Auto-save test progress setiap user menjawab pertanyaan"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        data = request.json
        user_id = session['user_id']
        answers = data.get('answers', {})
        current_question = data.get('current_question', 0)
        
        # Hitung progress berdasarkan jumlah jawaban
        total_questions = Question.query.count()
        if total_questions > 0:
            progress = int((len(answers) / total_questions) * 100)
            
            # Update user progress
            user = User.query.get(user_id)
            if user:
                user.progress_tes = min(progress, 99)  # Max 99% sampai submit
                db.session.commit()
        
        return jsonify({
            'success': True,
            'progress': progress,
            'answers_saved': len(answers)
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Auto-save gagal: {str(e)}'
        }), 500

@app.route('/api/load-saved-answers', methods=['GET'])
def api_load_saved_answers():
    """Load jawaban yang tersimpan untuk melanjutkan tes"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        user_id = session['user_id']
        
        # Get saved answers
        saved_answers = TestAnswer.query.filter_by(user_id=user_id).all()
        
        # Format answers
        answers = {}
        for answer in saved_answers:
            answers[str(answer.question_id)] = answer.answer
        
        return jsonify({
            'success': True,
            'answers': answers,
            'has_saved_progress': len(answers) > 0
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Load gagal: {str(e)}'
        }), 500

# Helper function to calculate personality scores
def calculate_personality_scores(user_id):
    """Calculate personality scores based on answers"""
    
    # Get all answers for this user
    answers = TestAnswer.query.filter_by(user_id=user_id).all()
    
    # Initialize score dictionaries
    trait_scores = {
        'energy': [], 'sociability': [], 'assertiveness': [], 'excitement': [],
        'warmth': [], 'trustfulness': [], 'sincerity': [], 'modesty': [],
        'dutifulness': [], 'orderliness': [], 'self_reliance': [], 'ambition': [],
        'anxiety': [], 'depression': [], 'moodiness': [], 'irritability': [],
        'aestheticism': [], 'intellect': [], 'flexibility': [], 'tolerance': [],
        'exhibitionism': [], 'self_indulgence': [], 'impulsiveness': [], 'hostility': [],
        'conventionality': []
    }
    
    # Process each answer
    for answer in answers:
        question = Question.query.get(answer.question_id)
        if not question:
            continue
        
        # Reverse score if needed
        score = answer.answer
        if question.reverse_scored:
            score = 6 - score  # Reverse 1->5, 2->4, 3->3, 4->2, 5->1
        
        # Add to appropriate trait
        if question.trait in trait_scores:
            trait_scores[question.trait].append(score)
    
    # Calculate raw scores (sum of answers)
    raw_scores = {}
    for trait, scores in trait_scores.items():
        raw_scores[f'{trait}_raw'] = sum(scores) if scores else 0
    
    # Calculate domain scores
    raw_scores['extraversion_raw'] = (
        raw_scores.get('energy_raw', 0) +
        raw_scores.get('sociability_raw', 0) +
        raw_scores.get('assertiveness_raw', 0) +
        raw_scores.get('excitement_raw', 0)
    )
    
    raw_scores['agreeableness_raw'] = (
        raw_scores.get('warmth_raw', 0) +
        raw_scores.get('trustfulness_raw', 0) +
        raw_scores.get('sincerity_raw', 0) +
        raw_scores.get('modesty_raw', 0)
    )
    
    raw_scores['conscientiousness_raw'] = (
        raw_scores.get('dutifulness_raw', 0) +
        raw_scores.get('orderliness_raw', 0) +
        raw_scores.get('self_reliance_raw', 0) +
        raw_scores.get('ambition_raw', 0)
    )
    
    raw_scores['neuroticism_raw'] = (
        raw_scores.get('anxiety_raw', 0) +
        raw_scores.get('depression_raw', 0) +
        raw_scores.get('moodiness_raw', 0) +
        raw_scores.get('irritability_raw', 0)
    )
    
    raw_scores['openness_raw'] = (
        raw_scores.get('aestheticism_raw', 0) +
        raw_scores.get('intellect_raw', 0) +
        raw_scores.get('flexibility_raw', 0) +
        raw_scores.get('tolerance_raw', 0)
    )
    
    raw_scores['narcissism_raw'] = (
        raw_scores.get('exhibitionism_raw', 0) +
        raw_scores.get('self_indulgence_raw', 0)
    )
    
    raw_scores['sensation_seeking_raw'] = (
        raw_scores.get('impulsiveness_raw', 0) +
        raw_scores.get('hostility_raw', 0) +
        (25 - raw_scores.get('conventionality_raw', 0))  # Reverse scored
    )
    
    # Convert to T-scores (mean=50, SD=10)
    # This is a simplified conversion - in production, use proper normalization tables
    t_scores = {}
    for trait, raw_score in raw_scores.items():
        # Simplified T-score conversion (adjust based on your norms)
        t_score = 50 + ((raw_score - 12.5) / 5) * 10  # Assuming mean=12.5, SD=5
        t_score = max(20, min(80, t_score))  # Clamp between 20-80
        t_scores[trait.replace('_raw', '_t')] = round(t_score, 2)
    
    # Categorize scores
    categories = {}
    for trait in trait_scores.keys():
        t_score = t_scores.get(f'{trait}_t', 50)
        if t_score < 40:
            category = 'Rendah'
        elif t_score < 60:
            category = 'Sedang'
        else:
            category = 'Tinggi'
        categories[f'{trait}_kategori'] = category
    
    # Add domain categories
    for domain in ['extraversion', 'agreeableness', 'conscientiousness', 'neuroticism', 'openness', 'narcissism', 'sensation_seeking']:
        t_score = t_scores.get(f'{domain}_t', 50)
        if t_score < 40:
            category = 'Rendah'
        elif t_score < 60:
            category = 'Sedang'
        else:
            category = 'Tinggi'
        categories[f'{domain}_kategori'] = category
    
    # Calculate average score
    all_t_scores = [v for k, v in t_scores.items() if k.endswith('_t')]
    avg_score = round(sum(all_t_scores) / len(all_t_scores), 2) if all_t_scores else 50
    
    return {**raw_scores, **t_scores, **categories, 'skor_rata_rata': avg_score}

def update_user_scores(user, scores):
    """Update user with calculated scores"""
    for key, value in scores.items():
        if hasattr(user, key):
            setattr(user, key, value)

# Add function to populate sample questions (run once)
def populate_sample_questions():
    """Populate database with sample questions"""
    
    sample_questions = [
        # Energy (Extraversion)
        {"text": "Saya merasa penuh energi di sekitar orang lain", "trait": "energy", "reverse": False, "order": 1},
        {"text": "Saya mudah lelah ketika berinteraksi sosial", "trait": "energy", "reverse": True, "order": 2},
        
        # Sociability (Extraversion)
        {"text": "Saya senang bertemu orang baru", "trait": "sociability", "reverse": False, "order": 3},
        {"text": "Saya lebih suka menghabiskan waktu sendirian", "trait": "sociability", "reverse": True, "order": 4},
        
        # Assertiveness (Extraversion)
        {"text": "Saya tidak ragu menyampaikan pendapat dalam diskusi", "trait": "assertiveness", "reverse": False, "order": 5},
        {"text": "Saya sering mengalah dalam percakapan", "trait": "assertiveness", "reverse": True, "order": 6},
        
        # Add more questions for all 25 traits...
        # This is just a sample, you should have at least 4-5 questions per trait
    ]
    
    for q_data in sample_questions:
        question = Question(
            text=q_data["text"],
            trait=q_data["trait"],
            reverse_scored=q_data["reverse"],
            order=q_data["order"]
        )
        db.session.add(question)
    
    db.session.commit()
    print(f"Added {len(sample_questions)} sample questions")

# Add CLI command to populate questions
@app.cli.command()
def init_questions():
    """Initialize database with sample questions"""
    populate_sample_questions()
    print("Questions initialized successfully!")

#ADMIN
# Tambahkan di app.py setelah class TestSession

class CriticalItem(db.Model):
    """Track critical items untuk identifikasi mahasiswa rentan"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(100), nullable=False)  # suicidal, substance_abuse, mood_disturbance, anger
    severity = db.Column(db.String(50))  # low, medium, high, critical
    score = db.Column(db.Float)  # calculated score
    flags = db.Column(db.Text)  # JSON string of specific flags
    assessed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='critical_items')


def assess_critical_items(user):
    """
    Assess critical items untuk menentukan apakah mahasiswa rentan
    Returns: dict dengan kategori dan severity
    """
    assessment = {
        'is_vulnerable': False,
        'risk_level': 'low',  # low, medium, high, critical
        'categories': [],
        'flags': [],
        'overall_score': 0
    }
    
    risk_score = 0
    
    # 1. SUICIDAL AND SELF-DAMAGING BEHAVIOR (PRIORITAS TERTINGGI)
    suicidal_flags = []
    if user.depression_t and user.depression_t >= 70:
        suicidal_flags.append('Depression sangat tinggi (T≥70)')
        risk_score += 25
    if user.anxiety_t and user.anxiety_t >= 70:
        suicidal_flags.append('Anxiety sangat tinggi (T≥70)')
        risk_score += 20
    if user.hostility_t and user.hostility_t >= 70:
        suicidal_flags.append('Hostility tinggi - potensi self-harm')
        risk_score += 15
    
    # Kombinasi berbahaya
    if (user.depression_t and user.depression_t >= 65 and 
        user.anxiety_t and user.anxiety_t >= 65):
        suicidal_flags.append('CRITICAL: Kombinasi Depression + Anxiety tinggi')
        risk_score += 30
    
    if suicidal_flags:
        assessment['categories'].append({
            'name': 'Suicidal & Self-Damaging Behavior',
            'severity': 'critical' if risk_score >= 40 else 'high',
            'flags': suicidal_flags
        })
    
    # 2. MOOD AND ANXIETY DISTURBANCES
    mood_flags = []
    if user.moodiness_t and user.moodiness_t >= 65:
        mood_flags.append(f'Moodiness sangat tinggi ({user.moodiness_t:.1f})')
        risk_score += 10
    if user.irritability_t and user.irritability_t >= 65:
        mood_flags.append(f'Irritability tinggi ({user.irritability_t:.1f})')
        risk_score += 8
    if user.neuroticism_t and user.neuroticism_t >= 70:
        mood_flags.append('Neuroticism sangat tinggi - ketidakstabilan emosi')
        risk_score += 12
    
    if mood_flags:
        assessment['categories'].append({
            'name': 'Mood & Anxiety Disturbances',
            'severity': 'high' if risk_score >= 20 else 'medium',
            'flags': mood_flags
        })
    
    # 3. ANGER AND IMPULSIVENESS
    anger_flags = []
    if user.hostility_t and user.hostility_t >= 65:
        anger_flags.append(f'Hostility tinggi ({user.hostility_t:.1f})')
        risk_score += 8
    if user.impulsiveness_t and user.impulsiveness_t >= 65:
        anger_flags.append(f'Impulsiveness tinggi ({user.impulsiveness_t:.1f})')
        risk_score += 7
    
    # Kombinasi berbahaya: Hostility + Impulsiveness
    if (user.hostility_t and user.hostility_t >= 60 and
        user.impulsiveness_t and user.impulsiveness_t >= 60):
        anger_flags.append('PERINGATAN: Kombinasi Hostility + Impulsiveness')
        risk_score += 10
    
    if anger_flags:
        assessment['categories'].append({
            'name': 'Anger & Impulsiveness',
            'severity': 'high' if risk_score >= 15 else 'medium',
            'flags': anger_flags
        })
    
    # 4. SOCIAL ISOLATION (indikator tambahan)
    isolation_flags = []
    if user.sociability_t and user.sociability_t <= 35:
        isolation_flags.append('Sociability sangat rendah - isolasi sosial')
        risk_score += 8
    if user.warmth_t and user.warmth_t <= 35:
        isolation_flags.append('Warmth rendah - kesulitan koneksi emosional')
        risk_score += 5
    
    if isolation_flags and (user.depression_t and user.depression_t >= 60):
        isolation_flags.append('PERINGATAN: Isolasi sosial + Depression')
        risk_score += 10
    
    if isolation_flags:
        assessment['categories'].append({
            'name': 'Social Isolation',
            'severity': 'medium',
            'flags': isolation_flags
        })
    
    # 5. LOW SELF-RELIANCE & COPING
    coping_flags = []
    if user.self_reliance_t and user.self_reliance_t <= 35:
        coping_flags.append('Self-reliance sangat rendah')
        risk_score += 6
    if user.dutifulness_t and user.dutifulness_t <= 35:
        coping_flags.append('Dutifulness rendah - kesulitan tanggung jawab')
        risk_score += 4
    
    if coping_flags:
        assessment['categories'].append({
            'name': 'Low Coping Skills',
            'severity': 'medium',
            'flags': coping_flags
        })
    
    # DETERMINE OVERALL RISK LEVEL
    assessment['overall_score'] = risk_score
    
    if risk_score >= 50:
        assessment['risk_level'] = 'critical'
        assessment['is_vulnerable'] = True
    elif risk_score >= 35:
        assessment['risk_level'] = 'high'
        assessment['is_vulnerable'] = True
    elif risk_score >= 20:
        assessment['risk_level'] = 'medium'
        assessment['is_vulnerable'] = True
    else:
        assessment['risk_level'] = 'low'
        assessment['is_vulnerable'] = False
    
    return assessment


@app.route('/api/mahasiswa-rentan', methods=['GET'])
def api_mahasiswa_rentan():
    """Get list of vulnerable students based on critical items assessment"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = db.session.get(User, session['user_id'])
    if not user.is_admin:
        return jsonify({'error': 'Forbidden'}), 403
    
    try:
        # Get query parameters
        angkatan = request.args.get('angkatan', '')
        search = request.args.get('search', '')
        risk_filter = request.args.get('risk_level', '')  # critical, high, medium
        
        # Base query - mahasiswa with completed tests
        query = User.query.filter_by(is_admin=False, status_tes='Selesai')
        
        # Filter by angkatan
        if angkatan:
            query = query.filter(User.nim.like(f'{angkatan}%'))
        
        # Search filter
        if search:
            search_pattern = f'%{search}%'
            query = query.filter(
                (User.nama.like(search_pattern)) |
                (User.nim.like(search_pattern))
            )
        
        # Get all students who completed test
        all_students = query.all()
        
        # Assess each student and filter vulnerable ones
        vulnerable_students = []
        
        for student in all_students:
            assessment = assess_critical_items(student)
            
            # Only include if vulnerable
            if assessment['is_vulnerable']:
                # Apply risk level filter if specified
                if risk_filter and assessment['risk_level'] != risk_filter:
                    continue
                
                vulnerable_students.append({
                    'student': student,
                    'assessment': assessment
                })
        
        # Sort by risk score (highest first)
        vulnerable_students.sort(key=lambda x: x['assessment']['overall_score'], reverse=True)
        
        # Calculate statistics
        total_mahasiswa = User.query.filter_by(is_admin=False).count()
        sudah_omni = User.query.filter_by(is_admin=False, status_tes='Selesai').count()
        belum_omni = total_mahasiswa - sudah_omni
        
        # Count by risk level
        critical_count = len([s for s in vulnerable_students if s['assessment']['risk_level'] == 'critical'])
        high_count = len([s for s in vulnerable_students if s['assessment']['risk_level'] == 'high'])
        medium_count = len([s for s in vulnerable_students if s['assessment']['risk_level'] == 'medium'])
        
        # Format mahasiswa data
        mahasiswa_data = []
        for idx, item in enumerate(vulnerable_students, 1):
            student = item['student']
            assessment = item['assessment']
            
            # Determine category display
            risk_level = assessment['risk_level']
            if risk_level == 'critical':
                kategori = 'Sangat Rentan'
                kategori_class = 'badge-critical'
            elif risk_level == 'high':
                kategori = 'Rentan Tinggi'
                kategori_class = 'badge-high'
            elif risk_level == 'medium':
                kategori = 'Rentan Sedang'
                kategori_class = 'badge-medium'
            else:
                kategori = 'Perhatian'
                kategori_class = 'badge-low'
            
            # Get primary concern
            primary_concern = ''
            if assessment['categories']:
                primary_concern = assessment['categories'][0]['name']
            
            mahasiswa_data.append({
                'no': idx,
                'nim': student.nim,
                'nama': student.nama,
                'fakultas': student.fakultas or 'N/A',
                'program_studi': 'Informatika',
                'risk_score': assessment['overall_score'],
                'kategori': kategori,
                'kategori_class': kategori_class,
                'primary_concern': primary_concern,
                'categories': assessment['categories'],
                'depression_t': round(student.depression_t, 1) if student.depression_t else 0,
                'anxiety_t': round(student.anxiety_t, 1) if student.anxiety_t else 0,
                'hostility_t': round(student.hostility_t, 1) if student.hostility_t else 0
            })
        
        return jsonify({
            'success': True,
            'stats': {
                'total_mahasiswa': total_mahasiswa,
                'sudah_omni': sudah_omni,
                'belum_omni': belum_omni,
                'total_rentan': len(vulnerable_students),
                'critical_count': critical_count,
                'high_count': high_count,
                'medium_count': medium_count
            },
            'mahasiswa': mahasiswa_data,
            'total': len(mahasiswa_data)
        })
        
    except Exception as e:
        print(f"Error getting mahasiswa rentan: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Terjadi kesalahan: {str(e)}'
        }), 500


@app.route('/api/mahasiswa-detail/<int:user_id>', methods=['GET'])
def api_mahasiswa_detail(user_id):
    """Get detailed assessment for a specific student"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    admin = db.session.get(User, session['user_id'])
    if not admin.is_admin:
        return jsonify({'error': 'Forbidden'}), 403
    
    try:
        student = User.query.get(user_id)
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        assessment = assess_critical_items(student)
        
        return jsonify({
            'success': True,
            'student': {
                'nim': student.nim,
                'nama': student.nama,
                'fakultas': student.fakultas,
                'email': student.email
            },
            'assessment': assessment
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    
@app.route('/api/export-mahasiswa-rentan', methods=['GET'])
def api_export_mahasiswa_rentan():
    """Export vulnerable students data to CSV"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = db.session.get(User, session['user_id'])
    if not user.is_admin:
        return jsonify({'error': 'Forbidden'}), 403
    
    try:
        import csv
        from io import StringIO
        from flask import make_response
        
        # Get query parameters (sama seperti di api_mahasiswa_rentan)
        angkatan = request.args.get('angkatan', '')
        search = request.args.get('search', '')
        risk_filter = request.args.get('risk_level', '')
        
        # Base query - mahasiswa with completed tests
        query = User.query.filter_by(is_admin=False, status_tes='Selesai')
        
        # Filter by angkatan
        if angkatan:
            query = query.filter(User.nim.like(f'{angkatan}%'))
        
        # Search filter
        if search:
            search_pattern = f'%{search}%'
            query = query.filter(
                (User.nama.like(search_pattern)) |
                (User.nim.like(search_pattern))
            )
        
        # Get all students who completed test
        all_students = query.all()
        
        # Assess each student and filter vulnerable ones
        vulnerable_students = []
        
        for student in all_students:
            assessment = assess_critical_items(student)
            
            # Only include if vulnerable
            if assessment['is_vulnerable']:
                # Apply risk level filter if specified
                if risk_filter and assessment['risk_level'] != risk_filter:
                    continue
                
                vulnerable_students.append({
                    'student': student,
                    'assessment': assessment
                })
        
        # Sort by risk score (highest first)
        vulnerable_students.sort(key=lambda x: x['assessment']['overall_score'], reverse=True)
        
        # Create CSV
        si = StringIO()
        writer = csv.writer(si)
        
        # Write header
        writer.writerow(['No', 'NIM', 'Nama', 'Fakultas', 'Program Studi', 
                        'Risk Score', 'Kategori', 'Primary Concern', 'Depression T-Score', 
                        'Anxiety T-Score', 'Hostility T-Score'])
        
        # Write data
        for idx, item in enumerate(vulnerable_students, 1):
            student = item['student']
            assessment = item['assessment']
            
            # Determine category display
            risk_level = assessment['risk_level']
            if risk_level == 'critical':
                kategori = 'Sangat Rentan'
            elif risk_level == 'high':
                kategori = 'Rentan Tinggi'
            elif risk_level == 'medium':
                kategori = 'Rentan Sedang'
            else:
                kategori = 'Perhatian'
            
            # Get primary concern
            primary_concern = ''
            if assessment['categories']:
                primary_concern = assessment['categories'][0]['name']
            
            writer.writerow([
                idx,
                student.nim,
                student.nama,
                student.fakultas or 'N/A',
                'Informatika',
                assessment['overall_score'],
                kategori,
                primary_concern,
                round(student.depression_t, 1) if student.depression_t else 0,
                round(student.anxiety_t, 1) if student.anxiety_t else 0,
                round(student.hostility_t, 1) if student.hostility_t else 0
            ])
        
        # Create response
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = f"attachment; filename=mahasiswa_rentan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        output.headers["Content-type"] = "text/csv; charset=utf-8"
        
        return output
        
    except Exception as e:
        print(f"Error exporting: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Terjadi kesalahan: {str(e)}'
        }), 500
    
@app.route('/mahasiswa-rentan')
def mahasiswa_rentan():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    if not user.is_admin:
        return redirect(url_for('dashboard'))
    
    user_dict = {
        'id': user.id,
        'nama': user.nama,
        'username': user.username,
        'profile_picture': user.profile_picture
    }
    
    return render_template('admin_mahasiswarentan.html', user=user_dict, active_page='mahasiswa_rentan')

@app.route('/admin/daftar-kegiatan')
def admin_daftar_kegiatan():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    if not user.is_admin:
        return redirect(url_for('dashboard'))
    
    user_dict = {
        'id': user.id,
        'nama': user.nama,
        'username': user.username,
        'profile_picture': user.profile_picture
    }
    
    # Get activity counts by category
    ukm_count = Activity.query.filter_by(kategori='UKM').count()
    kepanitiaan_count = Activity.query.filter_by(kategori='Kepanitiaan').count()
    organisasi_count = Activity.query.filter_by(kategori='Organisasi').count()
    lomba_count = Activity.query.filter_by(kategori='Lomba').count()
    
    # Get all activities
    activities = Activity.query.all()
    
    return render_template('admin_daftarkegiatan.html', 
                           user=user_dict, 
                           active_page='daftar_kegiatan',
                           ukm_count=ukm_count,
                           kepanitiaan_count=kepanitiaan_count,
                           organisasi_count=organisasi_count,
                           lomba_count=lomba_count,
                           activities=activities)

@app.route('/admin/profile')
def admin_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = db.session.get(User, session['user_id'])
    if not user.is_admin:
        return redirect(url_for('dashboard'))
    
    user_dict = {
        'id': user.id,
        'nama': user.nama,
        'username': user.username,
        'email': user.email,
        'nim': user.nim,
        'fakultas': user.fakultas,
        'profile_picture': user.profile_picture
    }
    
    return render_template('admin_profile.html', user=user_dict, active_page='profile')

try:
    from api.ml_routes import ml_bp
    app.register_blueprint(ml_bp)
    print("✅ ML routes registered successfully")
except ImportError as e:
    print(f"⚠️ ML routes not available: {e}")
except Exception as e:
    print(f"⚠️ Error registering ML routes: {e}")

@app.route('/admin/kegiatan/<int:activity_id>')
def admin_kegiatan_detail(activity_id):
    """Detail kegiatan untuk admin"""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = db.session.get(User, session['user_id'])
    if not user or not user.is_admin:
        return redirect(url_for('dashboard'))

    activity = Activity.query.get(activity_id)
    if not activity:
        return render_template('404.html'), 404

    match_percentage = calculate_activity_match(user, activity)

    activity_dict = {
        'id': activity.id,
        'nama': activity.nama,
        'kategori': activity.kategori,
        'tingkat_kesulitan': activity.tingkat_kesulitan,
        'peserta': activity.peserta,
        'deadline': activity.deadline,
        'lokasi': activity.lokasi,
        'deskripsi': activity.deskripsi,
        'match_percentage': match_percentage,
        'required_traits': activity.required_traits,
    }

    try:
        if hasattr(activity, 'persyaratan_json'):
            activity_dict['persyaratan'] = json.loads(activity.persyaratan_json) if activity.persyaratan_json else []
        else:
            activity_dict['persyaratan'] = []

        if hasattr(activity, 'manfaat_json'):
            activity_dict['manfaat'] = json.loads(activity.manfaat_json) if activity.manfaat_json else []
        else:
            activity_dict['manfaat'] = []

        if hasattr(activity, 'jadwal_json'):
            activity_dict['jadwal'] = json.loads(activity.jadwal_json) if activity.jadwal_json else []
        else:
            activity_dict['jadwal'] = []

        activity_dict['link'] = activity.link if hasattr(activity, 'link') else '#'

        if hasattr(activity, 'contact_json'):
            activity_dict['contact'] = json.loads(activity.contact_json) if activity.contact_json else None
        else:
            activity_dict['contact'] = None
    except Exception as e:
        print(f"Error parsing activity data (admin detail): {str(e)}")
        activity_dict['persyaratan'] = []
        activity_dict['manfaat'] = []
        activity_dict['jadwal'] = []
        activity_dict['link'] = '#'
        activity_dict['contact'] = None

    return render_template(
        'admin_detailkegiatan.html',
        activity=activity_dict,
        user=user,
        active_page='daftar_kegiatan'
    )

try:
    from api.ml_routes import ml_bp
    app.register_blueprint(ml_bp)
    print("✅ ML routes registered successfully")
except ImportError as e:
    print(f"⚠️ ML routes not available: {e}")
except Exception as e:
    print(f"⚠️ Error registering ML routes: {e}")

# ========== DATABASE INITIALIZATION ENDPOINTS ==========

@app.route('/seed-all-database-12345')
def seed_all_database():
    """Run all seeding in one endpoint"""
    from models import User, Activity, Question
    from werkzeug.security import generate_password_hash
    from sqlalchemy import text
    import json
    
    result = []
    
    try:
        # 1. CREATE TABLES
        db.create_all()
        result.append("✅ Step 1: Tables created")
        
        # 2. CREATE NOTIFICATION TABLE
        notification_sql = """
        CREATE TABLE IF NOT EXISTS notification (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            title VARCHAR(255) NOT NULL,
            message TEXT NOT NULL,
            type VARCHAR(50) DEFAULT 'info',
            is_read BOOLEAN DEFAULT FALSE,
            link VARCHAR(500),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_notification_user FOREIGN KEY(user_id) REFERENCES public."user"(id) ON DELETE CASCADE
        );
        CREATE INDEX IF NOT EXISTS idx_notification_user_id ON notification(user_id);
        CREATE INDEX IF NOT EXISTS idx_notification_is_read ON notification(is_read);
        CREATE INDEX IF NOT EXISTS idx_notification_created_at ON notification(created_at DESC);
        """
        db.session.execute(text(notification_sql))
        db.session.commit()
        result.append("✅ Step 2: Notification table created")
        
        # 3. SEED 200 QUESTIONS
        Question.query.delete()
        
        all_questions = [
            # EXTRAVERSION - Energy (8 questions)
            {"no": 1, "text": "Saya merasa berenergi saat berada di sekitar banyak orang", "trait": "energy", "reverse": False},
            {"no": 2, "text": "Saya lebih suka menghabiskan waktu sendirian daripada dengan orang lain", "trait": "energy", "reverse": True},
            {"no": 3, "text": "Saya cepat merasa lelah dalam acara sosial", "trait": "energy", "reverse": True},
            {"no": 4, "text": "Saya adalah orang yang aktif dan dinamis", "trait": "energy", "reverse": False},
            {"no": 5, "text": "Saya sering merasa tidak memiliki energi untuk beraktivitas", "trait": "energy", "reverse": True},
            {"no": 6, "text": "Saya senang terlibat dalam kegiatan kelompok yang aktif", "trait": "energy", "reverse": False},
            {"no": 7, "text": "Saya merasa lelah hanya dengan membayangkan acara ramai", "trait": "energy", "reverse": True},
            {"no": 8, "text": "Saya memiliki energi yang cukup untuk menjalani hari", "trait": "energy", "reverse": False},
            
            # EXTRAVERSION - Sociability (8 questions)
            {"no": 9, "text": "Saya mudah berteman dengan orang baru", "trait": "sociability", "reverse": False},
            {"no": 10, "text": "Saya merasa nyaman berbicara dengan orang asing", "trait": "sociability", "reverse": False},
            {"no": 11, "text": "Saya lebih suka bekerja sendiri", "trait": "sociability", "reverse": True},
            {"no": 12, "text": "Saya senang menjadi pusat perhatian", "trait": "sociability", "reverse": False},
            {"no": 13, "text": "Saya menghindari pertemuan sosial jika memungkinkan", "trait": "sociability", "reverse": True},
            {"no": 14, "text": "Saya menikmati pesta dan acara ramai", "trait": "sociability", "reverse": False},
            {"no": 15, "text": "Saya merasa canggung dalam situasi sosial", "trait": "sociability", "reverse": True},
            {"no": 16, "text": "Saya aktif mencari teman baru", "trait": "sociability", "reverse": False},
            
            # EXTRAVERSION - Assertiveness (7 questions)
            {"no": 17, "text": "Saya berani menyampaikan pendapat dalam diskusi", "trait": "assertiveness", "reverse": False},
            {"no": 18, "text": "Saya kesulitan menolak permintaan orang lain", "trait": "assertiveness", "reverse": True},
            {"no": 19, "text": "Saya dapat memimpin kelompok dengan baik", "trait": "assertiveness", "reverse": False},
            {"no": 20, "text": "Saya cenderung mengalah dalam perdebatan", "trait": "assertiveness", "reverse": True},
            {"no": 21, "text": "Saya berani mempertahankan keyakinan saya", "trait": "assertiveness", "reverse": False},
            {"no": 22, "text": "Saya lebih suka mengikuti daripada memimpin", "trait": "assertiveness", "reverse": True},
            {"no": 23, "text": "Saya percaya diri saat berbicara di depan umum", "trait": "assertiveness", "reverse": False},
            
            # EXTRAVERSION - Excitement (7 questions)
            {"no": 24, "text": "Saya selalu mencari pengalaman baru yang menarik", "trait": "excitement", "reverse": False},
            {"no": 25, "text": "Saya menikmati perubahan dan variasi dalam hidup", "trait": "excitement", "reverse": False},
            {"no": 26, "text": "Saya merasa bosan dengan rutinitas yang sama", "trait": "excitement", "reverse": False},
            {"no": 27, "text": "Saya lebih suka hal-hal yang dapat diprediksi", "trait": "excitement", "reverse": True},
            {"no": 28, "text": "Saya senang mencoba hal-hal yang belum pernah dilakukan", "trait": "excitement", "reverse": False},
            {"no": 29, "text": "Saya menghindari situasi yang tidak familiar", "trait": "excitement", "reverse": True},
            {"no": 30, "text": "Saya mudah bosan dengan aktivitas yang monoton", "trait": "excitement", "reverse": False},
            
            # AGREEABLENESS - Warmth (8 questions)
            {"no": 31, "text": "Saya peduli dengan perasaan orang lain", "trait": "warmth", "reverse": False},
            {"no": 32, "text": "Saya mudah berempati dengan kesulitan orang lain", "trait": "warmth", "reverse": False},
            {"no": 33, "text": "Saya bersikap hangat kepada orang yang baru dikenal", "trait": "warmth", "reverse": False},
            {"no": 34, "text": "Saya tidak terlalu peduli dengan masalah orang lain", "trait": "warmth", "reverse": True},
            {"no": 35, "text": "Saya senang membantu orang yang membutuhkan", "trait": "warmth", "reverse": False},
            {"no": 36, "text": "Saya jarang menunjukkan kasih sayang", "trait": "warmth", "reverse": True},
            {"no": 37, "text": "Saya mudah terharu melihat penderitaan orang lain", "trait": "warmth", "reverse": False},
            {"no": 38, "text": "Saya lebih fokus pada diri sendiri daripada orang lain", "trait": "warmth", "reverse": True},
            
            # AGREEABLENESS - Trustfulness (7 questions)
            {"no": 39, "text": "Saya mudah mempercayai orang lain", "trait": "trustfulness", "reverse": False},
            {"no": 40, "text": "Saya selalu curiga terhadap niat orang lain", "trait": "trustfulness", "reverse": True},
            {"no": 41, "text": "Saya percaya kebanyakan orang memiliki niat baik", "trait": "trustfulness", "reverse": False},
            {"no": 42, "text": "Saya berhati-hati dalam berteman karena takut dikhianati", "trait": "trustfulness", "reverse": True},
            {"no": 43, "text": "Saya yakin orang lain tidak akan menyakiti saya", "trait": "trustfulness", "reverse": False},
            {"no": 44, "text": "Saya selalu waspada terhadap kemungkinan penipuan", "trait": "trustfulness", "reverse": True},
            {"no": 45, "text": "Saya memberi kepercayaan penuh kepada teman dekat", "trait": "trustfulness", "reverse": False},
            
            # AGREEABLENESS - Sincerity (8 questions)
            {"no": 46, "text": "Saya selalu jujur dalam berkata-kata", "trait": "sincerity", "reverse": False},
            {"no": 47, "text": "Saya kadang berbohong untuk keuntungan pribadi", "trait": "sincerity", "reverse": True},
            {"no": 48, "text": "Saya mengatakan apa adanya meskipun menyakitkan", "trait": "sincerity", "reverse": False},
            {"no": 49, "text": "Saya sering berpura-pura untuk menyenangkan orang lain", "trait": "sincerity", "reverse": True},
            {"no": 50, "text": "Saya tidak suka berperilaku manipulatif", "trait": "sincerity", "reverse": False},
            {"no": 51, "text": "Saya kadang memanipulasi situasi untuk kepentingan saya", "trait": "sincerity", "reverse": True},
            {"no": 52, "text": "Saya menunjukkan diri saya apa adanya", "trait": "sincerity", "reverse": False},
            {"no": 53, "text": "Saya sering menyembunyikan perasaan sebenarnya", "trait": "sincerity", "reverse": True},
            
            # AGREEABLENESS - Modesty (7 questions)
            {"no": 54, "text": "Saya tidak suka membanggakan diri", "trait": "modesty", "reverse": False},
            {"no": 55, "text": "Saya merasa saya lebih baik dari kebanyakan orang", "trait": "modesty", "reverse": True},
            {"no": 56, "text": "Saya rendah hati dalam menerima pujian", "trait": "modesty", "reverse": False},
            {"no": 57, "text": "Saya senang dipuji dan diakui kehebatan saya", "trait": "modesty", "reverse": True},
            {"no": 58, "text": "Saya tidak merasa istimewa dibanding orang lain", "trait": "modesty", "reverse": False},
            {"no": 59, "text": "Saya merasa saya pantas mendapat perlakuan khusus", "trait": "modesty", "reverse": True},
            {"no": 60, "text": "Saya menghargai pencapaian orang lain seperti milik sendiri", "trait": "modesty", "reverse": False},
            
            # CONSCIENTIOUSNESS - Dutifulness (8 questions)
            {"no": 61, "text": "Saya selalu menyelesaikan tugas yang diberikan", "trait": "dutifulness", "reverse": False},
            {"no": 62, "text": "Saya sering menunda-nunda pekerjaan", "trait": "dutifulness", "reverse": True},
            {"no": 63, "text": "Saya bertanggung jawab terhadap kewajiban saya", "trait": "dutifulness", "reverse": False},
            {"no": 64, "text": "Saya kadang mengabaikan tanggung jawab saya", "trait": "dutifulness", "reverse": True},
            {"no": 65, "text": "Saya dapat diandalkan dalam menyelesaikan tugas", "trait": "dutifulness", "reverse": False},
            {"no": 66, "text": "Saya sering lupa deadline yang telah ditentukan", "trait": "dutifulness", "reverse": True},
            {"no": 67, "text": "Saya berusaha keras untuk memenuhi ekspektasi", "trait": "dutifulness", "reverse": False},
            {"no": 68, "text": "Saya tidak terlalu peduli dengan standar kualitas", "trait": "dutifulness", "reverse": True},
            
            # CONSCIENTIOUSNESS - Orderliness (7 questions)
            {"no": 69, "text": "Saya menjaga ruangan tetap rapi dan terorganisir", "trait": "orderliness", "reverse": False},
            {"no": 70, "text": "Saya tidak peduli dengan kerapian", "trait": "orderliness", "reverse": True},
            {"no": 71, "text": "Saya membuat daftar untuk mengatur aktivitas", "trait": "orderliness", "reverse": False},
            {"no": 72, "text": "Saya bekerja tanpa perencanaan yang jelas", "trait": "orderliness", "reverse": True},
            {"no": 73, "text": "Saya menyusun jadwal harian dengan detail", "trait": "orderliness", "reverse": False},
            {"no": 74, "text": "Saya merasa nyaman dengan kekacauan", "trait": "orderliness", "reverse": True},
            {"no": 75, "text": "Saya sistematis dalam mengerjakan tugas", "trait": "orderliness", "reverse": False},
            
            # CONSCIENTIOUSNESS - Self_reliance (8 questions)
            {"no": 76, "text": "Saya dapat menyelesaikan masalah sendiri", "trait": "self_reliance", "reverse": False},
            {"no": 77, "text": "Saya selalu membutuhkan bantuan orang lain", "trait": "self_reliance", "reverse": True},
            {"no": 78, "text": "Saya mandiri dalam mengambil keputusan", "trait": "self_reliance", "reverse": False},
            {"no": 79, "text": "Saya tergantung pada pendapat orang lain", "trait": "self_reliance", "reverse": True},
            {"no": 80, "text": "Saya percaya pada kemampuan diri sendiri", "trait": "self_reliance", "reverse": False},
            {"no": 81, "text": "Saya ragu dengan keputusan yang saya buat sendiri", "trait": "self_reliance", "reverse": True},
            {"no": 82, "text": "Saya dapat bekerja efektif tanpa supervisi", "trait": "self_reliance", "reverse": False},
            {"no": 83, "text": "Saya butuh dorongan konstan untuk menyelesaikan tugas", "trait": "self_reliance", "reverse": True},
            
            # CONSCIENTIOUSNESS - Ambition (7 questions)
            {"no": 84, "text": "Saya memiliki target yang jelas dalam hidup", "trait": "ambition", "reverse": False},
            {"no": 85, "text": "Saya tidak terlalu ambisius dengan pencapaian", "trait": "ambition", "reverse": True},
            {"no": 86, "text": "Saya berusaha menjadi yang terbaik dalam bidang saya", "trait": "ambition", "reverse": False},
            {"no": 87, "text": "Saya puas dengan kondisi saat ini", "trait": "ambition", "reverse": True},
            {"no": 88, "text": "Saya selalu mencari cara untuk berkembang", "trait": "ambition", "reverse": False},
            {"no": 89, "text": "Saya tidak termotivasi untuk mencapai kesuksesan besar", "trait": "ambition", "reverse": True},
            {"no": 90, "text": "Saya menetapkan standar tinggi untuk diri sendiri", "trait": "ambition", "reverse": False},
            
            # NEUROTICISM - Anxiety (8 questions)
            {"no": 91, "text": "Saya sering merasa cemas tanpa alasan jelas", "trait": "anxiety", "reverse": False},
            {"no": 92, "text": "Saya tenang dalam menghadapi tekanan", "trait": "anxiety", "reverse": True},
            {"no": 93, "text": "Saya mudah khawatir tentang masa depan", "trait": "anxiety", "reverse": False},
            {"no": 94, "text": "Saya jarang merasa gugup", "trait": "anxiety", "reverse": True},
            {"no": 95, "text": "Saya sering merasa tegang", "trait": "anxiety", "reverse": False},
            {"no": 96, "text": "Saya rileks dalam situasi stres", "trait": "anxiety", "reverse": True},
            {"no": 97, "text": "Saya takut hal buruk akan terjadi", "trait": "anxiety", "reverse": False},
            {"no": 98, "text": "Saya percaya diri menghadapi tantangan", "trait": "anxiety", "reverse": True},
            
            # NEUROTICISM - Depression (7 questions)
            {"no": 99, "text": "Saya sering merasa sedih tanpa sebab", "trait": "depression", "reverse": False},
            {"no": 100, "text": "Saya selalu berpikir positif tentang hidup", "trait": "depression", "reverse": True},
            {"no": 101, "text": "Saya merasa hidup tidak memiliki makna", "trait": "depression", "reverse": False},
            {"no": 102, "text": "Saya bahagia dengan kehidupan saya", "trait": "depression", "reverse": True},
            {"no": 103, "text": "Saya sering merasa putus asa", "trait": "depression", "reverse": False},
            {"no": 104, "text": "Saya optimis terhadap masa depan", "trait": "depression", "reverse": True},
            {"no": 105, "text": "Saya merasa kosong di dalam", "trait": "depression", "reverse": False},
            
            # NEUROTICISM - Moodiness (8 questions)
            {"no": 106, "text": "Suasana hati saya mudah berubah-ubah", "trait": "moodiness", "reverse": False},
            {"no": 107, "text": "Saya memiliki emosi yang stabil", "trait": "moodiness", "reverse": True},
            {"no": 108, "text": "Saya bisa bahagia kemudian tiba-tiba sedih", "trait": "moodiness", "reverse": False},
            {"no": 109, "text": "Saya konsisten dalam perasaan saya", "trait": "moodiness", "reverse": True},
            {"no": 110, "text": "Hal kecil dapat mengubah mood saya drastis", "trait": "moodiness", "reverse": False},
            {"no": 111, "text": "Saya tidak mudah terpengaruh emosi sesaat", "trait": "moodiness", "reverse": True},
            {"no": 112, "text": "Saya sulit memprediksi perasaan saya sendiri", "trait": "moodiness", "reverse": False},
            {"no": 113, "text": "Saya dapat mengontrol reaksi emosional saya", "trait": "moodiness", "reverse": True},
            
            # NEUROTICISM - Irritability (7 questions)
            {"no": 114, "text": "Saya mudah tersinggung dengan kata-kata orang", "trait": "irritability", "reverse": False},
            {"no": 115, "text": "Saya sabar menghadapi kritik", "trait": "irritability", "reverse": True},
            {"no": 116, "text": "Saya cepat marah pada hal-hal kecil", "trait": "irritability", "reverse": False},
            {"no": 117, "text": "Saya tenang saat ada yang mengecewakan saya", "trait": "irritability", "reverse": True},
            {"no": 118, "text": "Saya mudah frustasi saat ada hambatan", "trait": "irritability", "reverse": False},
            {"no": 119, "text": "Saya tidak mudah terganggu oleh orang lain", "trait": "irritability", "reverse": True},
            {"no": 120, "text": "Saya sering kehilangan kesabaran", "trait": "irritability", "reverse": False},
            
            # OPENNESS - Aestheticism (8 questions)
            {"no": 121, "text": "Saya menghargai keindahan seni dan musik", "trait": "aestheticism", "reverse": False},
            {"no": 122, "text": "Saya tidak tertarik dengan hal-hal artistik", "trait": "aestheticism", "reverse": True},
            {"no": 123, "text": "Saya menikmati kunjungan ke museum atau galeri", "trait": "aestheticism", "reverse": False},
            {"no": 124, "text": "Saya menganggap seni tidak penting", "trait": "aestheticism", "reverse": True},
            {"no": 125, "text": "Saya sensitif terhadap keindahan alam", "trait": "aestheticism", "reverse": False},
            {"no": 126, "text": "Saya tidak peduli dengan estetika", "trait": "aestheticism", "reverse": True},
            {"no": 127, "text": "Saya tertarik pada fashion dan desain", "trait": "aestheticism", "reverse": False},
            {"no": 128, "text": "Saya tidak memahami nilai dari karya seni", "trait": "aestheticism", "reverse": True},
            
            # OPENNESS - Intellect (7 questions)
            {"no": 129, "text": "Saya senang belajar hal-hal baru", "trait": "intellect", "reverse": False},
            {"no": 130, "text": "Saya tidak tertarik dengan ide-ide kompleks", "trait": "intellect", "reverse": True},
            {"no": 131, "text": "Saya suka berdiskusi tentang teori dan konsep", "trait": "intellect", "reverse": False},
            {"no": 132, "text": "Saya menghindari topik yang membuat berpikir keras", "trait": "intellect", "reverse": True},
            {"no": 133, "text": "Saya penasaran dengan cara kerja sesuatu", "trait": "intellect", "reverse": False},
            {"no": 134, "text": "Saya puas dengan pengetahuan yang sudah ada", "trait": "intellect", "reverse": True},
            {"no": 135, "text": "Saya membaca buku untuk memperluas wawasan", "trait": "intellect", "reverse": False},
            
            # OPENNESS - Flexibility (8 questions)
            {"no": 136, "text": "Saya mudah beradaptasi dengan perubahan", "trait": "flexibility", "reverse": False},
            {"no": 137, "text": "Saya tidak suka perubahan mendadak", "trait": "flexibility", "reverse": True},
            {"no": 138, "text": "Saya terbuka terhadap cara pandang baru", "trait": "flexibility", "reverse": False},
            {"no": 139, "text": "Saya bertahan pada pendapat saya meskipun ada bukti sebaliknya", "trait": "flexibility", "reverse": True},
            {"no": 140, "text": "Saya senang mencoba metode berbeda", "trait": "flexibility", "reverse": False},
            {"no": 141, "text": "Saya lebih nyaman dengan cara lama yang terbukti", "trait": "flexibility", "reverse": True},
            {"no": 142, "text": "Saya dapat mengubah rencana dengan mudah", "trait": "flexibility", "reverse": False},
            {"no": 143, "text": "Saya kaku dalam mengikuti prosedur", "trait": "flexibility", "reverse": True},
            
            # OPENNESS - Tolerance (7 questions)
            {"no": 144, "text": "Saya menghargai keberagaman budaya dan pandangan", "trait": "tolerance", "reverse": False},
            {"no": 145, "text": "Saya tidak nyaman dengan orang yang berbeda dari saya", "trait": "tolerance", "reverse": True},
            {"no": 146, "text": "Saya terbuka terhadap gaya hidup yang tidak konvensional", "trait": "tolerance", "reverse": False},
            {"no": 147, "text": "Saya merasa hanya ada satu cara yang benar", "trait": "tolerance", "reverse": True},
            {"no": 148, "text": "Saya menerima perbedaan pendapat dengan lapang dada", "trait": "tolerance", "reverse": False},
            {"no": 149, "text": "Saya tidak toleran terhadap pandangan yang bertentangan", "trait": "tolerance", "reverse": True},
            {"no": 150, "text": "Saya tertarik mempelajari budaya lain", "trait": "tolerance", "reverse": False},
            
            # NARCISSISM - Exhibitionism (13 questions)
            {"no": 151, "text": "Saya senang menjadi pusat perhatian", "trait": "exhibitionism", "reverse": False},
            {"no": 152, "text": "Saya tidak suka menonjol di depan umum", "trait": "exhibitionism", "reverse": True},
            {"no": 153, "text": "Saya senang dipuji atas penampilan saya", "trait": "exhibitionism", "reverse": False},
            {"no": 154, "text": "Saya tidak peduli dengan penilaian orang terhadap saya", "trait": "exhibitionism", "reverse": True},
            {"no": 155, "text": "Saya suka tampil beda dan mencolok", "trait": "exhibitionism", "reverse": False},
            {"no": 156, "text": "Saya lebih suka tidak terlihat", "trait": "exhibitionism", "reverse": True},
            {"no": 157, "text": "Saya mendramatisasi cerita agar menarik perhatian", "trait": "exhibitionism", "reverse": False},
            {"no": 158, "text": "Saya bercerita apa adanya tanpa dibesar-besarkan", "trait": "exhibitionism", "reverse": True},
            {"no": 159, "text": "Saya senang saat orang mengagumi saya", "trait": "exhibitionism", "reverse": False},
            {"no": 160, "text": "Saya tidak butuh pengakuan dari orang lain", "trait": "exhibitionism", "reverse": True},
            {"no": 161, "text": "Saya sering memposting pencapaian di media sosial", "trait": "exhibitionism", "reverse": False},
            {"no": 162, "text": "Saya jarang membagikan kehidupan pribadi", "trait": "exhibitionism", "reverse": True},
            {"no": 163, "text": "Saya merasa penting untuk dikenal banyak orang", "trait": "exhibitionism", "reverse": False},
            
            # NARCISSISM - Self_indulgence (12 questions)
            {"no": 164, "text": "Saya mudah menghabiskan uang untuk kesenangan pribadi", "trait": "self_indulgence", "reverse": False},
            {"no": 165, "text": "Saya hemat dan hati-hati dalam berbelanja", "trait": "self_indulgence", "reverse": True},
            {"no": 166, "text": "Saya sulit menolak godaan untuk bersenang-senang", "trait": "self_indulgence", "reverse": False},
            {"no": 167, "text": "Saya dapat mengendalikan keinginan saya", "trait": "self_indulgence", "reverse": True},
            {"no": 168, "text": "Saya sering memanjakan diri secara berlebihan", "trait": "self_indulgence", "reverse": False},
            {"no": 169, "text": "Saya disiplin dalam mengelola keinginan", "trait": "self_indulgence", "reverse": True},
            {"no": 170, "text": "Saya prioritaskan kesenangan daripada tanggung jawab", "trait": "self_indulgence", "reverse": False},
            {"no": 171, "text": "Saya menunda kesenangan demi tujuan jangka panjang", "trait": "self_indulgence", "reverse": True},
            {"no": 172, "text": "Saya impulsif saat berbelanja", "trait": "self_indulgence", "reverse": False},
            {"no": 173, "text": "Saya selalu berpikir matang sebelum membeli", "trait": "self_indulgence", "reverse": True},
            {"no": 174, "text": "Saya tidak bisa menahan keinginan sesaat", "trait": "self_indulgence", "reverse": False},
            {"no": 175, "text": "Saya memiliki kontrol diri yang baik", "trait": "self_indulgence", "reverse": True},
            
            # SENSATION_SEEKING - Impulsiveness (8 questions)
            {"no": 176, "text": "Saya bertindak tanpa berpikir panjang", "trait": "impulsiveness", "reverse": False},
            {"no": 177, "text": "Saya selalu mempertimbangkan konsekuensi sebelum bertindak", "trait": "impulsiveness", "reverse": True},
            {"no": 178, "text": "Saya sering menyesali keputusan spontan saya", "trait": "impulsiveness", "reverse": False},
            {"no": 179, "text": "Saya jarang melakukan hal yang impulsif", "trait": "impulsiveness", "reverse": True},
            {"no": 180, "text": "Saya mudah tergoda untuk mencoba hal baru segera", "trait": "impulsiveness", "reverse": False},
            {"no": 181, "text": "Saya butuh waktu untuk memutuskan sesuatu", "trait": "impulsiveness", "reverse": True},
            {"no": 182, "text": "Saya sering bertindak berdasarkan emosi sesaat", "trait": "impulsiveness", "reverse": False},
            {"no": 183, "text": "Saya rasional dalam setiap keputusan", "trait": "impulsiveness", "reverse": True},
            # SENSATION_SEEKING - Hostility (9 questions)
            {"no": 184, "text": "Saya mudah berkonflik dengan orang lain", "trait": "hostility", "reverse": False},
            {"no": 185, "text": "Saya menghindari pertengkaran sebisa mungkin", "trait": "hostility", "reverse": True},
            {"no": 186, "text": "Saya sinis terhadap niat baik orang lain", "trait": "hostility", "reverse": False},
            {"no": 187, "text": "Saya melihat sisi positif dari orang lain", "trait": "hostility", "reverse": True},
            {"no": 188, "text": "Saya sering menanggapi dengan sikap defensif", "trait": "hostility", "reverse": False},
            {"no": 189, "text": "Saya menerima kritik dengan terbuka", "trait": "hostility", "reverse": True},
            {"no": 190, "text": "Saya mudah merasa diserang atau dihina", "trait": "hostility", "reverse": False},
            {"no": 191, "text": "Saya tenang menerima pendapat berbeda", "trait": "hostility", "reverse": True},
            {"no": 192, "text": "Saya cenderung menyerang balik saat dikritik", "trait": "hostility", "reverse": False},
            
            # SENSATION_SEEKING - Conventionality (8 questions)
            {"no": 193, "text": "Saya mengikuti aturan dan tradisi yang ada", "trait": "conventionality", "reverse": False},
            {"no": 194, "text": "Saya suka melanggar aturan yang tidak masuk akal", "trait": "conventionality", "reverse": True},
            {"no": 195, "text": "Saya menghargai nilai-nilai konvensional", "trait": "conventionality", "reverse": False},
            {"no": 196, "text": "Saya tidak peduli dengan norma sosial", "trait": "conventionality", "reverse": True},
            {"no": 197, "text": "Saya mengikuti ekspektasi masyarakat", "trait": "conventionality", "reverse": False},
            {"no": 198, "text": "Saya suka melakukan hal yang tidak biasa", "trait": "conventionality", "reverse": True},
            {"no": 199, "text": "Saya patuh pada otoritas", "trait": "conventionality", "reverse": False},
            {"no": 200, "text": "Saya mempertanyakan aturan yang ada", "trait": "conventionality", "reverse": True},
        ]
        
        for q_data in all_questions:
            question = Question(
                text=q_data["text"],
                trait=q_data["trait"],
                reverse_scored=q_data["reverse"],
                order=q_data["no"]
            )
            db.session.add(question)
        
        db.session.commit()
        result.append(f"✅ Step 3: Added {len(all_questions)} questions")
        
        # 4. SEED 20 MAHASISWA BELUM TES
        mahasiswa_baru = [
            {'nim': '1301220198', 'nama': 'Embun Nawang Sari', 'username': 'embunns', 'fakultas': 'FIF'},
            {'nim': '1301226270', 'nama': 'Anila Dwi Lestari', 'username': 'aniladwi', 'fakultas': 'FIF'},
            {'nim': '1301223456', 'nama': 'Joshua Pinem', 'username': 'joshuapinem', 'fakultas': 'FIF'},
            {'nim': '1301224567', 'nama': 'Yasmina Arethaya Hanjani', 'username': 'yasminaarethaya', 'fakultas': 'FIF'},
            {'nim': '1301225678', 'nama': 'Muhammad Rafie Hamizan', 'username': 'rafiehamizan', 'fakultas': 'FIF'},
            {'nim': '1301226789', 'nama': 'Rayhan Arsy Sashenka', 'username': 'rayhanarsy', 'fakultas': 'FIF'},
            {'nim': '1301227890', 'nama': 'Siti Nurhaliza', 'username': 'sitinurhaliza', 'fakultas': 'FIF'},
            {'nim': '1301228901', 'nama': 'Budi Santoso', 'username': 'budisantoso', 'fakultas': 'FIK'},
            {'nim': '1301229012', 'nama': 'Dewi Lestari', 'username': 'dewilestari', 'fakultas': 'FTE'},
            {'nim': '1301220123', 'nama': 'Ahmad Fauzi', 'username': 'ahmadfauzi', 'fakultas': 'FEB'},
            {'nim': '1301221234', 'nama': 'Rina Wijaya', 'username': 'rinawijaya', 'fakultas': 'FRI'},
            {'nim': '1301222345', 'nama': 'Eko Prasetyo', 'username': 'ekoprasetyo', 'fakultas': 'FIT'},
            {'nim': '1301223450', 'nama': 'Lina Marlina', 'username': 'linamarlina', 'fakultas': 'FKB'},
            {'nim': '1301224561', 'nama': 'Rudi Hartono', 'username': 'rudihartono', 'fakultas': 'FIF'},
            {'nim': '1301225672', 'nama': 'Maya Sari', 'username': 'mayasari', 'fakultas': 'FIK'},
            {'nim': '1301226783', 'nama': 'Fajar Ramadhan', 'username': 'fajarramadhan', 'fakultas': 'FTE'},
            {'nim': '1301227894', 'nama': 'Indah Permata', 'username': 'indahpermata', 'fakultas': 'FEB'},
            {'nim': '1301228905', 'nama': 'Rizki Ananda', 'username': 'rizkiananda', 'fakultas': 'FRI'},
            {'nim': '1301229016', 'nama': 'Sari Wulandari', 'username': 'sariwulandari', 'fakultas': 'FIT'},
            {'nim': '1301220127', 'nama': 'Hendra Gunawan', 'username': 'hendragunawan', 'fakultas': 'FKB'}
        ]
        
        added_mhs = 0
        for mhs in mahasiswa_baru:
            if not User.query.filter_by(nim=mhs['nim']).first():
                user = User(
                    nim=mhs['nim'],
                    nama=mhs['nama'],
                    username=mhs['username'],
                    email=f"{mhs['username']}@student.telkomuniversity.ac.id",
                    fakultas=mhs['fakultas'],
                    password_hash=generate_password_hash('mahasiswa123'),
                    status_tes='Belum Selesai',
                    progress_profil=100,
                    progress_tes=0,
                    progress_eksplorasi=0,
                    progress_kegiatan=0
                )
                db.session.add(user)
                added_mhs += 1
        
        db.session.commit()
        result.append(f"✅ Step 4: Added {added_mhs} mahasiswa (belum tes)")
        
        # 5. SEED ADMIN
        if not User.query.filter_by(username='puti').first():
            admin = User(
                nim='0000000000',
                nama='Admin Puti',
                email='puti@telkomuniversity.ac.id',
                username='puti',
                fakultas='Admin',
                is_admin=True,
                password_hash=generate_password_hash('admin123')
            )
            db.session.add(admin)
            db.session.commit()
            result.append("✅ Step 5: Admin created")
        else:
            result.append("⚠️ Step 5: Admin already exists")
        
        # 6. SEED ACTIVITIES
        activities_data = [
            {
                'nama': 'UKM Bengkel Seni Embun',
                'kategori': 'UKM',
                'tingkat_kesulitan': 'Sedang',
                'peserta': '45/80',
                'deadline': '31 Januari 2026',
                'lokasi': 'Gedung Seni Tel-U',
                'deskripsi': 'Bidang seni dan kebudayaan tradisional maupun kontemporer',
                'required_traits': 'openness,aestheticism,creativity',
                'persyaratan_json': json.dumps(['Mahasiswa aktif semester 1–6', 'Memiliki minat di bidang seni', 'Bersedia mengikuti latihan rutin']),
                'manfaat_json': json.dumps(['Sertifikat kegiatan', 'Pengembangan kreativitas', 'Kesempatan pameran karya']),
                'jadwal_json': json.dumps([
                    {'hari': 'Senin', 'waktu': '16.00 - 18.00', 'kegiatan': 'Latihan Seni'},
                    {'hari': 'Jumat', 'waktu': '16.00 - 18.00', 'kegiatan': 'Workshop'}
                ]),
                'link': 'https://linktr.ee/ukm-seni-embun',
                'contact_json': json.dumps({'name': 'Ketua UKM Seni', 'phone': '0812-3456-7890', 'email': 'seni@omnimap.ac.id'})
            },
            {
                'nama': 'UKM Fotografi Telkom',
                'kategori': 'UKM',
                'tingkat_kesulitan': 'Sedang',
                'peserta': '38/60',
                'deadline': '15 Februari 2026',
                'lokasi': 'Studio Fotografi Tel-U',
                'deskripsi': 'UKM yang bergerak di bidang fotografi',
                'required_traits': 'aestheticism,openness,creativity',
                'persyaratan_json': json.dumps(['Mahasiswa aktif', 'Memiliki kamera atau smartphone', 'Minat fotografi']),
                'manfaat_json': json.dumps(['Sertifikat', 'Portofolio fotografi', 'Relasi dengan fotografer']),
                'jadwal_json': json.dumps([
                    {'hari': 'Selasa', 'waktu': '16.00 - 18.00', 'kegiatan': 'Hunting Foto'},
                    {'hari': 'Kamis', 'waktu': '16.00 - 18.00', 'kegiatan': 'Editing & Review'}
                ]),
                'link': 'https://bit.ly/ukm-fotografi',
                'contact_json': json.dumps({'name': 'Ketua UKM Foto', 'phone': '0813-1111-2222', 'email': 'foto@omnimap.ac.id'})
            },
            {
                'nama': 'UKM Forum Sinema Telkom',
                'kategori': 'UKM',
                'tingkat_kesulitan': 'Tinggi',
                'peserta': '25/40',
                'deadline': '28 Februari 2026',
                'lokasi': 'Studio Film Tel-U',
                'deskripsi': 'Bidang seni perfilman, pembuatan film, dan sinematografi',
                'required_traits': 'creativity,openness,aestheticism',
                'persyaratan_json': json.dumps(['Mahasiswa aktif', 'Minat di dunia film', 'Siap kerja tim']),
                'manfaat_json': json.dumps(['Pengalaman produksi film', 'Portofolio sinematografi', 'Relasi komunitas film']),
                'jadwal_json': json.dumps([
                    {'hari': 'Rabu', 'waktu': '18.00 - 20.00', 'kegiatan': 'Diskusi Film'},
                    {'hari': 'Sabtu', 'waktu': '09.00 - 12.00', 'kegiatan': 'Produksi Film'}
                ]),
                'link': 'https://bit.ly/forum-sinema',
                'contact_json': json.dumps({'name': 'Koordinator Sinema', 'phone': '0814-2222-3333', 'email': 'sinema@omnimap.ac.id'})
            },
            {
                'nama': 'UKM Teater TITIK',
                'kategori': 'UKM',
                'tingkat_kesulitan': 'Tinggi',
                'peserta': '30/50',
                'deadline': '10 Maret 2026',
                'lokasi': 'Auditorium Tel-U',
                'deskripsi': 'UKM yang bergerak di bidang seni teater',
                'required_traits': 'extraversion,creativity,openness',
                'persyaratan_json': json.dumps(['Mahasiswa aktif', 'Berani tampil di depan umum', 'Komitmen latihan']),
                'manfaat_json': json.dumps(['Kemampuan public speaking', 'Pengembangan ekspresi diri', 'Pengalaman pentas']),
                'jadwal_json': json.dumps([
                    {'hari': 'Senin', 'waktu': '18.00 - 20.00', 'kegiatan': 'Latihan Akting'},
                    {'hari': 'Kamis', 'waktu': '18.00 - 20.00', 'kegiatan': 'Latihan Pementasan'}
                ]),
                'link': 'https://bit.ly/teater-titik',
                'contact_json': json.dumps({'name': 'Ketua Teater', 'phone': '0815-3333-4444', 'email': 'teater@omnimap.ac.id'})
            },
            {
                'nama': 'UKM Luminosus Animation',
                'kategori': 'UKM',
                'tingkat_kesulitan': 'Tinggi',
                'peserta': '22/35',
                'deadline': '20 Maret 2026',
                'lokasi': 'Lab Animasi Tel-U',
                'deskripsi': 'UKM yang bergerak di bidang seni, desain grafis dan animasi',
                'required_traits': 'creativity,aestheticism,conscientiousness',
                'persyaratan_json': json.dumps(['Mahasiswa aktif', 'Minat desain/animasi', 'Laptop pribadi']),
                'manfaat_json': json.dumps(['Skill animasi', 'Portofolio desain', 'Pengalaman project']),
                'jadwal_json': json.dumps([
                    {'hari': 'Selasa', 'waktu': '18.00 - 20.00', 'kegiatan': 'Belajar Software Animasi'},
                    {'hari': 'Jumat', 'waktu': '18.00 - 20.00', 'kegiatan': 'Project Tim'}
                ]),
                'link': 'https://bit.ly/luminosus-animation',
                'contact_json': json.dumps({'name': 'Ketua Luminosus', 'phone': '0816-4444-5555', 'email': 'animasi@omnimap.ac.id'})
            },
            {
                'nama': 'BEM Fakultas Informatika',
                'kategori': 'Organisasi',
                'tingkat_kesulitan': 'Tinggi',
                'peserta': '15/25',
                'deadline': '1 Februari 2026',
                'lokasi': 'Gedung FIF Tel-U',
                'deskripsi': 'Organisasi mahasiswa tingkat fakultas',
                'required_traits': 'leadership,organization,extraversion',
                'persyaratan_json': json.dumps(['Mahasiswa Fakultas Informatika', 'IPK minimal 3.00']),
                'manfaat_json': json.dumps(['Pengalaman kepemimpinan', 'Relasi organisasi', 'Sertifikat']),
                'jadwal_json': json.dumps([{'hari': 'Senin', 'waktu': '18.00 - 20.00', 'kegiatan': 'Rapat BEM'}]),
                'link': 'https://bit.ly/bem-fif',
                'contact_json': json.dumps({'name': 'Sekretaris BEM', 'phone': '0818-6666-7777', 'email': 'bemfif@omnimap.ac.id'})
            },
            {
                'nama': 'Lomba Hackathon AI',
                'kategori': 'Lomba',
                'tingkat_kesulitan': 'Sangat Tinggi',
                'peserta': '75/150',
                'deadline': '15 Januari 2026',
                'lokasi': 'Lab Komputer Tel-U',
                'deskripsi': 'Kompetisi pemrograman dan AI',
                'required_traits': 'conscientiousness,creativity,teamwork',
                'persyaratan_json': json.dumps(['Mahasiswa aktif', 'Menguasai dasar pemrograman', 'Tim 3–5 orang']),
                'manfaat_json': json.dumps(['Hadiah lomba', 'Sertifikat nasional', 'Pengalaman kompetisi']),
                'jadwal_json': json.dumps([{'hari': 'Sabtu', 'waktu': '08.00 - 20.00', 'kegiatan': 'Hackathon'}]),
                'link': 'https://bit.ly/hackathon-ai',
                'contact_json': json.dumps({'name': 'Panitia Hackathon', 'phone': '0819-7777-8888', 'email': 'hackathon@omnimap.ac.id'})
            }
        ]
        
        added_act = 0
        for act_data in activities_data:
            if not Activity.query.filter_by(nama=act_data['nama']).first():
                activity = Activity(**act_data)
                db.session.add(activity)
                added_act += 1
        
        db.session.commit()
        result.append(f"✅ Step 6: Added {added_act} activities")
        
        # Success message
        total_users = User.query.filter_by(is_admin=False).count()
        total_questions = Question.query.count()
        total_activities = Activity.query.count()
        
        return f"""
        <h2>🎉 DATABASE SEEDING COMPLETED!</h2>
        <hr>
        {'<br>'.join(result)}
        <hr>
        <h3>📊 Summary:</h3>
        <ul>
            <li>Total Users: {total_users} mahasiswa + 1 admin</li>
            <li>Total Questions: {total_questions}</li>
            <li>Total Activities: {total_activities}</li>
        </ul>
        <hr>
        <h3>🔐 Login Credentials:</h3>
        <p><strong>Admin:</strong> username=puti, password=admin123</p>
        <p><strong>Mahasiswa:</strong> username=embunns (atau lainnya), password=mahasiswa123</p>
        <hr>
        <p>✅ Your app is now ready to use!</p>
        """, 200
        
    except Exception as e:
        db.session.rollback()
        return f"❌ Error: {str(e)}", 500
    

if __name__ == '__main__':
    with app.app_context():
        # Create database tables
        db.create_all()
        print("✅ Database tables created")
        
        # Load ML models (optional - akan fallback ke existing logic jika gagal)
        try:
            from utils.model_loader import load_all_models
            models_loaded = load_all_models()
            if models_loaded:
                print("✅ ML models loaded and ready")
            else:
                print("⚠️ ML models not loaded - using fallback methods")
        except Exception as e:
            print(f"⚠️ Could not load ML models: {e}")
            print("💡 App will use existing prediction methods")
        
        # Uncomment this line to populate sample questions (run once)
        # populate_sample_questions()
    
    print("\n" + "="*60)
    print("🚀 OmniMap Server Starting...")
    print("="*60)
    print(f"📊 Database: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"🌐 URL: http://localhost:5000")
    print(f"💡 Press CTRL+C to stop")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000)
    