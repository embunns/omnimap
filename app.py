from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import json
from datetime import timedelta

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your-secret-key-change-this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///omnimap.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
# Di terminal Python atau dalam app.py


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
        user = User.query.get(session['user_id'])
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
    
    user = User.query.get(session['user_id'])
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
    
    user = User.query.get(session['user_id'])
    
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
        
        user = User.query.get(session['user_id'])
        
        # Generate AI response based on user's personality data
        ai_response = generate_chatbot_response(user, user_message)
        
        return jsonify({
            'success': True,
            'response': ai_response
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Terjadi kesalahan: {str(e)}'
        }), 500

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

# API untuk update profile picture
@app.route('/api/update-profile-picture', methods=['POST'])
def api_update_profile_picture():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        data = request.json
        user = User.query.get(session['user_id'])
        
        if not user:
            return jsonify({'success': False, 'message': 'User tidak ditemukan'}), 404
        
        # Update profile picture (base64 string)
        if data.get('profile_picture'):
            user.profile_picture = data.get('profile_picture')
        
        db.session.commit()
        
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
    
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user, active_page='profile')

# API untuk update profile
@app.route('/api/update-profile', methods=['POST'])
def api_update_profile():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        data = request.json
        user = User.query.get(session['user_id'])
        
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
    
    user = User.query.get(session['user_id'])
    
    # Check if user has completed the test
    if user.status_tes != 'Selesai':
        # Redirect to test page if not completed
        return redirect(url_for('tes_omni'))
    
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

# Tambahkan routes ini ke app.py

@app.route('/rekomendasi-kegiatan')
def rekomendasi_kegiatan():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
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

@app.route('/api/recommended-activities', methods=['GET'])
def api_recommended_activities():
    """Get recommended activities based on user's personality traits"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        user = User.query.get(session['user_id'])
        
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
    
    if not activity.required_traits:
        return 50  # Default match if no traits specified
    
    required_traits = [t.strip() for t in activity.required_traits.split(',')]
    
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
        'flexibility': 'flexibility_t'
    }
    
    total_score = 0
    matched_traits = 0
    
    for trait in required_traits:
        trait_lower = trait.lower()
        if trait_lower in trait_mapping:
            user_trait_attr = trait_mapping[trait_lower]
            user_trait_value = getattr(user, user_trait_attr, 50)
            
            # Normalize score to 0-100 range (T-scores are typically 20-80)
            normalized_score = ((user_trait_value - 20) / 60) * 100
            normalized_score = max(0, min(100, normalized_score))
            
            total_score += normalized_score
            matched_traits += 1
    
    # Calculate average match percentage
    if matched_traits > 0:
        match_percentage = int(total_score / matched_traits)
    else:
        match_percentage = 50
    
    # Add bonus for high openness (generally good for trying new activities)
    if hasattr(user, 'openness_t') and user.openness_t:
        openness_bonus = int((user.openness_t - 50) / 10)
        match_percentage = min(100, match_percentage + openness_bonus)
    
    return match_percentage

@app.route('/api/activity/<int:activity_id>', methods=['GET'])
def api_get_activity_detail(activity_id):
    """Get detailed information about a specific activity"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        user = User.query.get(session['user_id'])
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
        user = User.query.get(session['user_id'])
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
    
    user = User.query.get(session['user_id'])
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
    
    user = User.query.get(session['user_id'])
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
    
    user = User.query.get(session['user_id'])
    if not user or not user.is_admin:
        return jsonify({'success': False, 'message': 'Admin access required'}), 403
    
    try:
        data = request.json
        
        # Validate required fields
        if not data.get('kategori') or not data.get('nama'):
            return jsonify({'success': False, 'message': 'Kategori dan nama kegiatan harus diisi'}), 400
        
        import json
        
        # Create new activity
        new_activity = Activity(
            nama=data.get('nama'),
            kategori=data.get('kategori'),
            deskripsi=data.get('deskripsi', ''),
            deadline=data.get('deadline', ''),
            peserta=data.get('peserta', ''),
            lokasi=data.get('lokasi', ''),
            persyaratan_json=json.dumps([data.get('persyaratan', '')]) if data.get('persyaratan') else None,
            manfaat_json=json.dumps([data.get('manfaat', '')]) if data.get('manfaat') else None,
            jadwal_json=json.dumps({'tanggal': data.get('jadwal', '')}) if data.get('jadwal') else None,
            link=data.get('link', ''),
            contact_json=json.dumps({'info': data.get('kontak', '')}) if data.get('kontak') else None
        )
        
        db.session.add(new_activity)
        db.session.commit()
        
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

# Update tes_omni route
@app.route('/tes-omni')
def tes_omni():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
    # Check if user already completed the test
    if user.status_tes == 'Selesai':
        return redirect(url_for('hasil_tes'))
    
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
                         total_questions=len(questions_data), active_page='tes_omni')

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
@app.route('/api/mahasiswa-rentan', methods=['GET'])
def api_mahasiswa_rentan():
    """Get list of vulnerable students for admin dashboard"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = User.query.get(session['user_id'])
    if not user.is_admin:
        return jsonify({'error': 'Forbidden'}), 403
    
    try:
        # Get query parameters
        angkatan = request.args.get('angkatan', '')
        search = request.args.get('search', '')
        
        # Base query - mahasiswa with completed tests
        query = User.query.filter_by(is_admin=False, status_tes='Selesai')
        
        # Filter by angkatan (assuming NIM starts with year)
        if angkatan:
            query = query.filter(User.nim.like(f'{angkatan}%'))
        
        # Search filter
        if search:
            search_pattern = f'%{search}%'
            query = query.filter(
                (User.nama.like(search_pattern)) |
                (User.nim.like(search_pattern))
            )
        
        # Get vulnerable students (high neuroticism or specific traits)
        mahasiswa = query.filter(
            (User.neuroticism_t >= 60) |  # High neuroticism
            (User.anxiety_t >= 60) |      # High anxiety
            (User.depression_t >= 60)     # High depression
        ).order_by(User.neuroticism_t.desc()).all()
        
        # Calculate statistics
        total_mahasiswa = User.query.filter_by(is_admin=False).count()
        sudah_omni = User.query.filter_by(is_admin=False, status_tes='Selesai').count()
        belum_omni = total_mahasiswa - sudah_omni
        
        # Format mahasiswa data
        mahasiswa_data = []
        for idx, m in enumerate(mahasiswa, 1):
            # Determine category based on neuroticism score
            if m.neuroticism_t >= 70:
                kategori = 'Tinggi'
                kategori_class = 'badge-high'
            elif m.neuroticism_t >= 60:
                kategori = 'Sedang'
                kategori_class = 'badge-medium'
            else:
                kategori = 'Rendah'
                kategori_class = 'badge-low'
            
            mahasiswa_data.append({
                'no': idx,
                'nim': m.nim,
                'nama': m.nama,
                'fakultas': m.fakultas or 'N/A',
                'program_studi': 'Informatika',  # Add this field to User model if needed
                'skor_omni': round(m.neuroticism_t, 0) if m.neuroticism_t else 0,
                'kategori': kategori,
                'kategori_class': kategori_class,
                'anxiety_t': round(m.anxiety_t, 1) if m.anxiety_t else 0,
                'depression_t': round(m.depression_t, 1) if m.depression_t else 0
            })
        
        return jsonify({
            'success': True,
            'stats': {
                'total_mahasiswa': total_mahasiswa,
                'sudah_omni': sudah_omni,
                'belum_omni': belum_omni
            },
            'mahasiswa': mahasiswa_data,
            'total': len(mahasiswa_data)
        })
        
    except Exception as e:
        print(f"Error getting mahasiswa rentan: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Terjadi kesalahan: {str(e)}'
        }), 500

@app.route('/api/export-mahasiswa-rentan', methods=['GET'])
def api_export_mahasiswa_rentan():
    """Export vulnerable students data to CSV"""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user = User.query.get(session['user_id'])
    if not user.is_admin:
        return jsonify({'error': 'Forbidden'}), 403
    
    try:
        import csv
        from io import StringIO
        from flask import make_response
        
        # Get vulnerable students
        mahasiswa = User.query.filter_by(is_admin=False, status_tes='Selesai').filter(
            (User.neuroticism_t >= 60) |
            (User.anxiety_t >= 60) |
            (User.depression_t >= 60)
        ).all()
        
        # Create CSV
        si = StringIO()
        writer = csv.writer(si)
        
        # Write header
        writer.writerow(['No', 'NIM', 'Nama', 'Fakultas', 'Program Studi', 
                        'Skor OMNI', 'Kategori', 'Anxiety', 'Depression'])
        
        # Write data
        for idx, m in enumerate(mahasiswa, 1):
            if m.neuroticism_t >= 70:
                kategori = 'Tinggi'
            elif m.neuroticism_t >= 60:
                kategori = 'Sedang'
            else:
                kategori = 'Rendah'
            
            writer.writerow([
                idx,
                m.nim,
                m.nama,
                m.fakultas or 'N/A',
                'Informatika',
                round(m.neuroticism_t, 0) if m.neuroticism_t else 0,
                kategori,
                round(m.anxiety_t, 1) if m.anxiety_t else 0,
                round(m.depression_t, 1) if m.depression_t else 0
            ])
        
        # Create response
        output = make_response(si.getvalue())
        output.headers["Content-Disposition"] = "attachment; filename=mahasiswa_rentan.csv"
        output.headers["Content-type"] = "text/csv"
        
        return output
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Terjadi kesalahan: {str(e)}'
        }), 500
    
@app.route('/mahasiswa-rentan')
def mahasiswa_rentan():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
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
    
    user = User.query.get(session['user_id'])
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
    
    user = User.query.get(session['user_id'])
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Uncomment this line to populate sample questions (run once)
        # populate_sample_questions()
    
    print("🚀 Server running on http://localhost:5000")
    print("💡 Run 'flask init-questions' to populate sample questions")
    app.run(debug=True, port=5000)