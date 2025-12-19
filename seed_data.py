import json
from app import app, db, User, Activity

def get_kategori(t_score):
    if t_score >= 65:
        return 'Sangat Tinggi'
    elif t_score >= 55:
        return 'Tinggi'
    elif t_score >= 45:
        return 'Sedang'
    elif t_score >= 35:
        return 'Rendah'
    else:
        return 'Sangat Rendah'

def seed_database():
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        admin = User(
            nim='0000000000',
            nama='Admin Puti',
            email='puti@telkomuniversity.ac.id',
            username='puti',
            fakultas='Admin',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        users_data = [
            {
                'nim': '17012046048', 'nama': 'Putri Kusuma', 'fakultas': 'FIK',
                'energy_raw': 30, 'sociability_raw': 31, 'assertiveness_raw': 28, 'excitement_raw': 31, 'warmth_raw': 23, 'trustfulness_raw': 22, 'sincerity_raw': 22, 'modesty_raw': 21, 'dutifulness_raw': 41, 'orderliness_raw': 32, 'self_reliance_raw': 37, 'ambition_raw': 33, 'anxiety_raw': 46, 'depression_raw': 40, 'moodiness_raw': 44, 'irritability_raw': 41, 'aestheticism_raw': 40, 'intellect_raw': 34, 'flexibility_raw': 36, 'tolerance_raw': 34, 'exhibitionism_raw': 51, 'self_indulgence_raw': 45, 'impulsiveness_raw': 44, 'hostility_raw': 51, 'conventionality_raw': 44, 'extraversion_raw': 120, 'agreeableness_raw': 88, 'conscientiousness_raw': 143, 'neuroticism_raw': 171, 'openness_raw': 144, 'narcissism_raw': 96, 'sensation_seeking_raw': 139,
                'energy_t': 53.04, 'sociability_t': 54.28, 'assertiveness_t': 55.55, 'excitement_t': 59.86, 'warmth_t': 45.41, 'trustfulness_t': 47.66, 'sincerity_t': 44.32, 'modesty_t': 46.52, 'dutifulness_t': 60.52, 'orderliness_t': 56.57, 'self_reliance_t': 56.9, 'ambition_t': 57.52, 'anxiety_t': 66.3, 'depression_t': 65.97, 'moodiness_t': 64.39, 'irritability_t': 67.02, 'aestheticism_t': 51.15, 'intellect_t': 50.26, 'flexibility_t': 48.01, 'tolerance_t': 50.26, 'exhibitionism_t': 48.78, 'self_indulgence_t': 47.49, 'impulsiveness_t': 64.65, 'hostility_t': 66.09, 'conventionality_t': 64.64, 'extraversion_t': 55.76, 'agreeableness_t': 45.81, 'conscientiousness_t': 58.06, 'neuroticism_t': 66.2, 'openness_t': 49.9, 'narcissism_t': 48.15, 'sensation_seeking_t': 65.47,
                'skor_rata_rata': 72, 'status_tes': 'Selesai', 'progress_tes': 100, 'progress_eksplorasi': 60
            },
            {
                'nim': '17012421395', 'nama': 'Nadia Bintang Wijaya', 'fakultas': 'FIK',
                'energy_raw': 28, 'sociability_raw': 31, 'assertiveness_raw': 26, 'excitement_raw': 29, 'warmth_raw': 30, 'trustfulness_raw': 29, 'sincerity_raw': 34, 'modesty_raw': 24, 'dutifulness_raw': 54, 'orderliness_raw': 49, 'self_reliance_raw': 54, 'ambition_raw': 47, 'anxiety_raw': 32, 'depression_raw': 30, 'moodiness_raw': 34, 'irritability_raw': 26, 'aestheticism_raw': 54, 'intellect_raw': 47, 'flexibility_raw': 54, 'tolerance_raw': 48, 'exhibitionism_raw': 76, 'self_indulgence_raw': 67, 'impulsiveness_raw': 38, 'hostility_raw': 42, 'conventionality_raw': 32, 'extraversion_raw': 114, 'agreeableness_raw': 117, 'conscientiousness_raw': 204, 'neuroticism_raw': 122, 'openness_raw': 203, 'narcissism_raw': 143, 'sensation_seeking_raw': 112,
                'energy_t': 50.52, 'sociability_t': 54.28, 'assertiveness_t': 52.68, 'excitement_t': 57.0, 'warmth_t': 52.76, 'trustfulness_t': 55.99, 'sincerity_t': 56.96, 'modesty_t': 50.08, 'dutifulness_t': 72.21, 'orderliness_t': 73.94, 'self_reliance_t': 72.13, 'ambition_t': 71.85, 'anxiety_t': 52.99, 'depression_t': 55.14, 'moodiness_t': 54.89, 'irritability_t': 50.78, 'aestheticism_t': 62.08, 'intellect_t': 61.83, 'flexibility_t': 62.13, 'tolerance_t': 62.73, 'exhibitionism_t': 63.25, 'self_indulgence_t': 61.19, 'impulsiveness_t': 58.37, 'hostility_t': 57.69, 'conventionality_t': 52.11, 'extraversion_t': 53.67, 'agreeableness_t': 54.1, 'conscientiousness_t': 72.9, 'neuroticism_t': 53.55, 'openness_t': 62.33, 'narcissism_t': 62.35, 'sensation_seeking_t': 56.24,
                'skor_rata_rata': 68, 'status_tes': 'Selesai', 'progress_tes': 100, 'progress_eksplorasi': 45
            },
            {
                'nim': '11012140495', 'nama': 'Irfan Eka Pratama', 'fakultas': 'FTE',
                'energy_raw': 30, 'sociability_raw': 31, 'assertiveness_raw': 28, 'excitement_raw': 27, 'warmth_raw': 21, 'trustfulness_raw': 15, 'sincerity_raw': 18, 'modesty_raw': 21, 'dutifulness_raw': 47, 'orderliness_raw': 42, 'self_reliance_raw': 45, 'ambition_raw': 43, 'anxiety_raw': 29, 'depression_raw': 27, 'moodiness_raw': 32, 'irritability_raw': 26, 'aestheticism_raw': 54, 'intellect_raw': 48, 'flexibility_raw': 54, 'tolerance_raw': 46, 'exhibitionism_raw': 59, 'self_indulgence_raw': 56, 'impulsiveness_raw': 51, 'hostility_raw': 53, 'conventionality_raw': 47, 'extraversion_raw': 116, 'agreeableness_raw': 75, 'conscientiousness_raw': 177, 'neuroticism_raw': 114, 'openness_raw': 202, 'narcissism_raw': 115, 'sensation_seeking_raw': 151,
                'energy_t': 53.04, 'sociability_t': 54.28, 'assertiveness_t': 55.55, 'excitement_t': 54.13, 'warmth_t': 43.31, 'trustfulness_t': 39.33, 'sincerity_t': 40.11, 'modesty_t': 46.52, 'dutifulness_t': 65.92, 'orderliness_t': 66.79, 'self_reliance_t': 64.07, 'ambition_t': 67.75, 'anxiety_t': 50.14, 'depression_t': 51.89, 'moodiness_t': 52.99, 'irritability_t': 50.78, 'aestheticism_t': 62.08, 'intellect_t': 62.72, 'flexibility_t': 62.13, 'tolerance_t': 60.95, 'exhibitionism_t': 53.41, 'self_indulgence_t': 54.34, 'impulsiveness_t': 71.98, 'hostility_t': 67.96, 'conventionality_t': 67.77, 'extraversion_t': 54.37, 'agreeableness_t': 42.1, 'conscientiousness_t': 66.33, 'neuroticism_t': 51.49, 'openness_t': 62.12, 'narcissism_t': 53.89, 'sensation_seeking_t': 69.57,
                'skor_rata_rata': 65, 'status_tes': 'Selesai', 'progress_tes': 100, 'progress_eksplorasi': 30
            },
            {
                'nim': '16012464987', 'nama': 'Omar Cahaya Maharani', 'fakultas': 'FEB',
                'energy_raw': 33, 'sociability_raw': 33, 'assertiveness_raw': 26, 'excitement_raw': 26, 'warmth_raw': 44, 'trustfulness_raw': 36, 'sincerity_raw': 47, 'modesty_raw': 41, 'dutifulness_raw': 43, 'orderliness_raw': 40, 'self_reliance_raw': 52, 'ambition_raw': 43, 'anxiety_raw': 46, 'depression_raw': 40, 'moodiness_raw': 43, 'irritability_raw': 37, 'aestheticism_raw': 28, 'intellect_raw': 30, 'flexibility_raw': 36, 'tolerance_raw': 29, 'exhibitionism_raw': 37, 'self_indulgence_raw': 32, 'impulsiveness_raw': 26, 'hostility_raw': 29, 'conventionality_raw': 28, 'extraversion_raw': 118, 'agreeableness_raw': 168, 'conscientiousness_raw': 178, 'neuroticism_raw': 166, 'openness_raw': 123, 'narcissism_raw': 69, 'sensation_seeking_raw': 83,
                'energy_t': 56.83, 'sociability_t': 56.8, 'assertiveness_t': 52.68, 'excitement_t': 52.69, 'warmth_t': 67.46, 'trustfulness_t': 64.32, 'sincerity_t': 70.64, 'modesty_t': 70.24, 'dutifulness_t': 62.32, 'orderliness_t': 64.74, 'self_reliance_t': 70.34, 'ambition_t': 67.75, 'anxiety_t': 66.3, 'depression_t': 65.97, 'moodiness_t': 63.44, 'irritability_t': 62.69, 'aestheticism_t': 41.78, 'intellect_t': 46.7, 'flexibility_t': 48.01, 'tolerance_t': 45.81, 'exhibitionism_t': 40.68, 'self_indulgence_t': 39.4, 'impulsiveness_t': 45.8, 'hostility_t': 45.56, 'conventionality_t': 47.94, 'extraversion_t': 55.07, 'agreeableness_t': 68.67, 'conscientiousness_t': 66.58, 'neuroticism_t': 64.91, 'openness_t': 45.48, 'narcissism_t': 39.99, 'sensation_seeking_t': 46.33,
                'skor_rata_rata': 70, 'status_tes': 'Selesai', 'progress_tes': 100, 'progress_eksplorasi': 55
            },
            {
                'nim': '14012165392', 'nama': 'Wawan Kusuma', 'fakultas': 'FRI',
                'energy_raw': 23, 'sociability_raw': 20, 'assertiveness_raw': 23, 'excitement_raw': 23, 'warmth_raw': 27, 'trustfulness_raw': 25, 'sincerity_raw': 27, 'modesty_raw': 23, 'dutifulness_raw': 12, 'orderliness_raw': 15, 'self_reliance_raw': 12, 'ambition_raw': 14, 'anxiety_raw': 21, 'depression_raw': 15, 'moodiness_raw': 20, 'irritability_raw': 12, 'aestheticism_raw': 24, 'intellect_raw': 22, 'flexibility_raw': 25, 'tolerance_raw': 17, 'exhibitionism_raw': 35, 'self_indulgence_raw': 36, 'impulsiveness_raw': 34, 'hostility_raw': 32, 'conventionality_raw': 27, 'extraversion_raw': 89, 'agreeableness_raw': 102, 'conscientiousness_raw': 53, 'neuroticism_raw': 68, 'openness_raw': 88, 'narcissism_raw': 71, 'sensation_seeking_raw': 93,
                'energy_t': 44.21, 'sociability_t': 40.43, 'assertiveness_t': 48.38, 'excitement_t': 48.39, 'warmth_t': 49.61, 'trustfulness_t': 51.23, 'sincerity_t': 49.59, 'modesty_t': 48.89, 'dutifulness_t': 34.43, 'orderliness_t': 39.19, 'self_reliance_t': 34.5, 'ambition_t': 38.07, 'anxiety_t': 42.53, 'depression_t': 38.88, 'moodiness_t': 41.59, 'irritability_t': 35.63, 'aestheticism_t': 38.66, 'intellect_t': 39.58, 'flexibility_t': 39.38, 'tolerance_t': 35.13, 'exhibitionism_t': 39.53, 'self_indulgence_t': 41.89, 'impulsiveness_t': 54.18, 'hostility_t': 48.36, 'conventionality_t': 46.9, 'extraversion_t': 44.97, 'agreeableness_t': 49.81, 'conscientiousness_t': 36.18, 'neuroticism_t': 39.61, 'openness_t': 38.1, 'narcissism_t': 40.59, 'sensation_seeking_t': 49.74,
                'skor_rata_rata': 48, 'status_tes': 'Selesai', 'progress_tes': 100, 'progress_eksplorasi': 20
            },
            {
                'nim': '13022022156', 'nama': 'Agus Wibowo', 'fakultas': 'FIF',
                'energy_raw': 40, 'sociability_raw': 39, 'assertiveness_raw': 40, 'excitement_raw': 34, 'warmth_raw': 14, 'trustfulness_raw': 10, 'sincerity_raw': 13, 'modesty_raw': 10, 'dutifulness_raw': 15, 'orderliness_raw': 11, 'self_reliance_raw': 10, 'ambition_raw': 10, 'anxiety_raw': 34, 'depression_raw': 26, 'moodiness_raw': 27, 'irritability_raw': 35, 'aestheticism_raw': 52, 'intellect_raw': 47, 'flexibility_raw': 53, 'tolerance_raw': 47, 'exhibitionism_raw': 89, 'self_indulgence_raw': 82, 'impulsiveness_raw': 32, 'hostility_raw': 33, 'conventionality_raw': 27, 'extraversion_raw': 153, 'agreeableness_raw': 47, 'conscientiousness_raw': 46, 'neuroticism_raw': 122, 'openness_raw': 199, 'narcissism_raw': 171, 'sensation_seeking_raw': 92,
                'energy_t': 65.66, 'sociability_t': 64.35, 'assertiveness_t': 72.77, 'excitement_t': 64.17, 'warmth_t': 35.96, 'trustfulness_t': 33.38, 'sincerity_t': 34.85, 'modesty_t': 33.47, 'dutifulness_t': 37.13, 'orderliness_t': 35.1, 'self_reliance_t': 32.71, 'ambition_t': 33.98, 'anxiety_t': 54.89, 'depression_t': 50.8, 'moodiness_t': 48.24, 'irritability_t': 60.53, 'aestheticism_t': 60.52, 'intellect_t': 61.83, 'flexibility_t': 61.35, 'tolerance_t': 61.84, 'exhibitionism_t': 70.77, 'self_indulgence_t': 70.53, 'impulsiveness_t': 52.08, 'hostility_t': 49.29, 'conventionality_t': 46.9, 'extraversion_t': 67.25, 'agreeableness_t': 34.09, 'conscientiousness_t': 34.48, 'neuroticism_t': 53.55, 'openness_t': 61.48, 'narcissism_t': 70.81, 'sensation_seeking_t': 49.4,
                'skor_rata_rata': 58, 'status_tes': 'Selesai', 'progress_tes': 100, 'progress_eksplorasi': 40
            },
            {
                'nim': '18022444671', 'nama': 'Citra Cahaya Firmansyah', 'fakultas': 'FIT',
                'energy_raw': 23, 'sociability_raw': 24, 'assertiveness_raw': 19, 'excitement_raw': 23, 'warmth_raw': 19, 'trustfulness_raw': 18, 'sincerity_raw': 19, 'modesty_raw': 18, 'dutifulness_raw': 23, 'orderliness_raw': 20, 'self_reliance_raw': 22, 'ambition_raw': 18, 'anxiety_raw': 17, 'depression_raw': 17, 'moodiness_raw': 17, 'irritability_raw': 17, 'aestheticism_raw': 39, 'intellect_raw': 32, 'flexibility_raw': 40, 'tolerance_raw': 37, 'exhibitionism_raw': 38, 'self_indulgence_raw': 33, 'impulsiveness_raw': 35, 'hostility_raw': 35, 'conventionality_raw': 30, 'extraversion_raw': 89, 'agreeableness_raw': 74, 'conscientiousness_raw': 83, 'neuroticism_raw': 68, 'openness_raw': 148, 'narcissism_raw': 71, 'sensation_seeking_raw': 100,
                'energy_t': 44.21, 'sociability_t': 45.46, 'assertiveness_t': 42.64, 'excitement_t': 48.39, 'warmth_t': 41.21, 'trustfulness_t': 42.9, 'sincerity_t': 41.16, 'modesty_t': 42.96, 'dutifulness_t': 44.32, 'orderliness_t': 44.3, 'self_reliance_t': 43.46, 'ambition_t': 42.17, 'anxiety_t': 38.73, 'depression_t': 41.05, 'moodiness_t': 38.74, 'irritability_t': 41.04, 'aestheticism_t': 50.37, 'intellect_t': 48.48, 'flexibility_t': 51.15, 'tolerance_t': 52.93, 'exhibitionism_t': 41.26, 'self_indulgence_t': 40.02, 'impulsiveness_t': 55.22, 'hostility_t': 51.16, 'conventionality_t': 50.03, 'extraversion_t': 44.97, 'agreeableness_t': 41.81, 'conscientiousness_t': 43.47, 'neuroticism_t': 39.61, 'openness_t': 50.74, 'narcissism_t': 40.59, 'sensation_seeking_t': 52.14,
                'skor_rata_rata': 52, 'status_tes': 'Selesai', 'progress_tes': 100, 'progress_eksplorasi': 25
            },
            {
                'nim': '11022082357', 'nama': 'Tono Eka Dewanti', 'fakultas': 'FTE',
                'energy_raw': 26, 'sociability_raw': 26, 'assertiveness_raw': 21, 'excitement_raw': 22, 'warmth_raw': 23, 'trustfulness_raw': 27, 'sincerity_raw': 30, 'modesty_raw': 28, 'dutifulness_raw': 49, 'orderliness_raw': 42, 'self_reliance_raw': 48, 'ambition_raw': 42, 'anxiety_raw': 29, 'depression_raw': 28, 'moodiness_raw': 33, 'irritability_raw': 23, 'aestheticism_raw': 51, 'intellect_raw': 46, 'flexibility_raw': 53, 'tolerance_raw': 46, 'exhibitionism_raw': 62, 'self_indulgence_raw': 58, 'impulsiveness_raw': 13, 'hostility_raw': 18, 'conventionality_raw': 14, 'extraversion_raw': 95, 'agreeableness_raw': 108, 'conscientiousness_raw': 181, 'neuroticism_raw': 113, 'openness_raw': 196, 'narcissism_raw': 120, 'sensation_seeking_raw': 45,
                'energy_t': 48.0, 'sociability_t': 47.98, 'assertiveness_t': 45.51, 'excitement_t': 46.96, 'warmth_t': 45.41, 'trustfulness_t': 53.61, 'sincerity_t': 52.75, 'modesty_t': 54.82, 'dutifulness_t': 67.71, 'orderliness_t': 66.79, 'self_reliance_t': 66.76, 'ambition_t': 66.73, 'anxiety_t': 50.14, 'depression_t': 52.97, 'moodiness_t': 53.94, 'irritability_t': 47.53, 'aestheticism_t': 59.73, 'intellect_t': 60.94, 'flexibility_t': 61.35, 'tolerance_t': 60.95, 'exhibitionism_t': 55.15, 'self_indulgence_t': 55.58, 'impulsiveness_t': 32.18, 'hostility_t': 35.29, 'conventionality_t': 33.33, 'extraversion_t': 47.06, 'agreeableness_t': 51.53, 'conscientiousness_t': 67.31, 'neuroticism_t': 51.23, 'openness_t': 60.85, 'narcissism_t': 55.4, 'sensation_seeking_t': 33.34,
                'skor_rata_rata': 62, 'status_tes': 'Selesai', 'progress_tes': 100, 'progress_eksplorasi': 35
            },
            {
                'nim': '18022435203', 'nama': 'Vicky Wijaya', 'fakultas': 'FIT',
                'energy_raw': 27, 'sociability_raw': 30, 'assertiveness_raw': 28, 'excitement_raw': 27, 'warmth_raw': 40, 'trustfulness_raw': 35, 'sincerity_raw': 39, 'modesty_raw': 37, 'dutifulness_raw': 23, 'orderliness_raw': 13, 'self_reliance_raw': 14, 'ambition_raw': 13, 'anxiety_raw': 40, 'depression_raw': 33, 'moodiness_raw': 40, 'irritability_raw': 34, 'aestheticism_raw': 54, 'intellect_raw': 47, 'flexibility_raw': 54, 'tolerance_raw': 47, 'exhibitionism_raw': 51, 'self_indulgence_raw': 45, 'impulsiveness_raw': 11, 'hostility_raw': 13, 'conventionality_raw': 9, 'extraversion_raw': 112, 'agreeableness_raw': 151, 'conscientiousness_raw': 63, 'neuroticism_raw': 147, 'openness_raw': 202, 'narcissism_raw': 96, 'sensation_seeking_raw': 33,
                'energy_t': 49.26, 'sociability_t': 53.02, 'assertiveness_t': 55.55, 'excitement_t': 54.13, 'warmth_t': 63.26, 'trustfulness_t': 63.13, 'sincerity_t': 62.22, 'modesty_t': 65.5, 'dutifulness_t': 44.32, 'orderliness_t': 37.15, 'self_reliance_t': 36.3, 'ambition_t': 37.05, 'anxiety_t': 60.6, 'depression_t': 58.39, 'moodiness_t': 60.59, 'irritability_t': 59.44, 'aestheticism_t': 62.08, 'intellect_t': 61.83, 'flexibility_t': 62.13, 'tolerance_t': 61.84, 'exhibitionism_t': 48.78, 'self_indulgence_t': 47.49, 'impulsiveness_t': 30.09, 'hostility_t': 30.62, 'conventionality_t': 28.11, 'extraversion_t': 52.98, 'agreeableness_t': 63.81, 'conscientiousness_t': 38.61, 'neuroticism_t': 60.0, 'openness_t': 62.12, 'narcissism_t': 48.15, 'sensation_seeking_t': 29.24,
                'skor_rata_rata': 66, 'status_tes': 'Selesai', 'progress_tes': 100, 'progress_eksplorasi': 50
            },
            {
                'nim': '17012220458', 'nama': 'Omar Utami', 'fakultas': 'FIK',
                'skor_rata_rata': None, 'status_tes': 'Belum Selesai', 'progress_tes': 0, 'progress_eksplorasi': 0
            }
        ]
        
        for u in users_data:
            user = User(
                nim=u['nim'],
                nama=u['nama'],
                email=u['nama'].lower().replace(' ', '.') + '@student.telkomuniversity.ac.id',
                username=u['nama'].lower().replace(' ', ''),
                fakultas=u['fakultas'],
                is_admin=False,
                skor_rata_rata=u.get('skor_rata_rata'),
                status_tes=u.get('status_tes', 'Belum Selesai'),
                progress_profil=100,
                progress_tes=u.get('progress_tes', 0),
                progress_eksplorasi=u.get('progress_eksplorasi', 0),
                progress_kegiatan=0
            )
            
            if 'energy_raw' in u:
                user.energy_raw = u['energy_raw']
                user.sociability_raw = u['sociability_raw']
                user.assertiveness_raw = u['assertiveness_raw']
                user.excitement_raw = u['excitement_raw']
                user.warmth_raw = u['warmth_raw']
                user.trustfulness_raw = u['trustfulness_raw']
                user.sincerity_raw = u['sincerity_raw']
                user.modesty_raw = u['modesty_raw']
                user.dutifulness_raw = u['dutifulness_raw']
                user.orderliness_raw = u['orderliness_raw']
                user.self_reliance_raw = u['self_reliance_raw']
                user.ambition_raw = u['ambition_raw']
                user.anxiety_raw = u['anxiety_raw']
                user.depression_raw = u['depression_raw']
                user.moodiness_raw = u['moodiness_raw']
                user.irritability_raw = u['irritability_raw']
                user.aestheticism_raw = u['aestheticism_raw']
                user.intellect_raw = u['intellect_raw']
                user.flexibility_raw = u['flexibility_raw']
                user.tolerance_raw = u['tolerance_raw']
                user.exhibitionism_raw = u['exhibitionism_raw']
                user.self_indulgence_raw = u['self_indulgence_raw']
                user.impulsiveness_raw = u['impulsiveness_raw']
                user.hostility_raw = u['hostility_raw']
                user.conventionality_raw = u['conventionality_raw']
                user.extraversion_raw = u['extraversion_raw']
                user.agreeableness_raw = u['agreeableness_raw']
                user.conscientiousness_raw = u['conscientiousness_raw']
                user.neuroticism_raw = u['neuroticism_raw']
                user.openness_raw = u['openness_raw']
                user.narcissism_raw = u['narcissism_raw']
                user.sensation_seeking_raw = u['sensation_seeking_raw']
                
                user.energy_t = u['energy_t']
                user.sociability_t = u['sociability_t']
                user.assertiveness_t = u['assertiveness_t']
                user.excitement_t = u['excitement_t']
                user.warmth_t = u['warmth_t']
                user.trustfulness_t = u['trustfulness_t']
                user.sincerity_t = u['sincerity_t']
                user.modesty_t = u['modesty_t']
                user.dutifulness_t = u['dutifulness_t']
                user.orderliness_t = u['orderliness_t']
                user.self_reliance_t = u['self_reliance_t']
                user.ambition_t = u['ambition_t']
                user.anxiety_t = u['anxiety_t']
                user.depression_t = u['depression_t']
                user.moodiness_t = u['moodiness_t']
                user.irritability_t = u['irritability_t']
                user.aestheticism_t = u['aestheticism_t']
                user.intellect_t = u['intellect_t']
                user.flexibility_t = u['flexibility_t']
                user.tolerance_t = u['tolerance_t']
                user.exhibitionism_t = u['exhibitionism_t']
                user.self_indulgence_t = u['self_indulgence_t']
                user.impulsiveness_t = u['impulsiveness_t']
                user.hostility_t = u['hostility_t']
                user.conventionality_t = u['conventionality_t']
                user.extraversion_t = u['extraversion_t']
                user.agreeableness_t = u['agreeableness_t']
                user.conscientiousness_t = u['conscientiousness_t']
                user.neuroticism_t = u['neuroticism_t']
                user.openness_t = u['openness_t']
                user.narcissism_t = u['narcissism_t']
                user.sensation_seeking_t = u['sensation_seeking_t']
                
                user.energy_kategori = get_kategori(u['energy_t'])
                user.sociability_kategori = get_kategori(u['sociability_t'])
                user.assertiveness_kategori = get_kategori(u['assertiveness_t'])
                user.excitement_kategori = get_kategori(u['excitement_t'])
                user.warmth_kategori = get_kategori(u['warmth_t'])
                user.trustfulness_kategori = get_kategori(u['trustfulness_t'])
                user.sincerity_kategori = get_kategori(u['sincerity_t'])
                user.modesty_kategori = get_kategori(u['modesty_t'])
                user.dutifulness_kategori = get_kategori(u['dutifulness_t'])
                user.orderliness_kategori = get_kategori(u['orderliness_t'])
                user.self_reliance_kategori = get_kategori(u['self_reliance_t'])
                user.ambition_kategori = get_kategori(u['ambition_t'])
                user.anxiety_kategori = get_kategori(u['anxiety_t'])
                user.depression_kategori = get_kategori(u['depression_t'])
                user.moodiness_kategori = get_kategori(u['moodiness_t'])
                user.irritability_kategori = get_kategori(u['irritability_t'])
                user.aestheticism_kategori = get_kategori(u['aestheticism_t'])
                user.intellect_kategori = get_kategori(u['intellect_t'])
                user.flexibility_kategori = get_kategori(u['flexibility_t'])
                user.tolerance_kategori = get_kategori(u['tolerance_t'])
                user.exhibitionism_kategori = get_kategori(u['exhibitionism_t'])
                user.self_indulgence_kategori = get_kategori(u['self_indulgence_t'])
                user.impulsiveness_kategori = get_kategori(u['impulsiveness_t'])
                user.hostility_kategori = get_kategori(u['hostility_t'])
                user.conventionality_kategori = get_kategori(u['conventionality_t'])
                user.extraversion_kategori = get_kategori(u['extraversion_t'])
                user.agreeableness_kategori = get_kategori(u['agreeableness_t'])
                user.conscientiousness_kategori = get_kategori(u['conscientiousness_t'])
                user.neuroticism_kategori = get_kategori(u['neuroticism_t'])
                user.openness_kategori = get_kategori(u['openness_t'])
                user.narcissism_kategori = get_kategori(u['narcissism_t'])
                user.sensation_seeking_kategori = get_kategori(u['sensation_seeking_t'])
            
            user.set_password('mahasiswa123')
            db.session.add(user)
        
        activities = [
            Activity(
                nama='UKM Bengkel Seni Embun',
                kategori='UKM',
                tingkat_kesulitan='Sedang',
                peserta='45/80',
                deadline='31 Januari 2026',
                lokasi='Gedung Seni Tel-U',
                deskripsi='Bidang seni dan kebudayaan tradisional maupun kontemporer',
                required_traits='openness,aestheticism,creativity',
                persyaratan_json=json.dumps([
                    'Mahasiswa aktif semester 1–6',
                    'Memiliki minat di bidang seni',
                    'Bersedia mengikuti latihan rutin'
                ]),
                manfaat_json=json.dumps([
                    'Sertifikat kegiatan',
                    'Pengembangan kreativitas',
                    'Kesempatan pameran karya'
                ]),
                jadwal_json=json.dumps([
                    {'hari': 'Senin', 'waktu': '16.00 - 18.00', 'kegiatan': 'Latihan Seni'},
                    {'hari': 'Jumat', 'waktu': '16.00 - 18.00', 'kegiatan': 'Workshop'}
                ]),
                link='https://linktr.ee/ukm-seni-embun',
                contact_json=json.dumps({'name': 'Ketua UKM Seni', 'phone': '0812-3456-7890', 'email': 'seni@omnimap.ac.id'})
            ),

            Activity(
                nama='UKM Fotografi Telkom',
                kategori='UKM',
                tingkat_kesulitan='Sedang',
                peserta='38/60',
                deadline='15 Februari 2026',
                lokasi='Studio Fotografi Tel-U',
                deskripsi='UKM yang bergerak di bidang fotografi',
                required_traits='aestheticism,openness,creativity',
                persyaratan_json=json.dumps([
                    'Mahasiswa aktif',
                    'Memiliki kamera atau smartphone',
                    'Minat fotografi'
                ]),
                manfaat_json=json.dumps([
                    'Sertifikat',
                    'Portofolio fotografi',
                    'Relasi dengan fotografer'
                ]),
                jadwal_json=json.dumps([
                    {'hari': 'Selasa', 'waktu': '16.00 - 18.00', 'kegiatan': 'Hunting Foto'},
                    {'hari': 'Kamis', 'waktu': '16.00 - 18.00', 'kegiatan': 'Editing & Review'}
                ]),
                link='https://bit.ly/ukm-fotografi',
                contact_json=json.dumps({'name': 'Ketua UKM Foto', 'phone': '0813-1111-2222', 'email': 'foto@omnimap.ac.id'})
            ),

            Activity(
                nama='UKM Forum Sinema Telkom',
                kategori='UKM',
                tingkat_kesulitan='Tinggi',
                peserta='25/40',
                deadline='28 Februari 2026',
                lokasi='Studio Film Tel-U',
                deskripsi='Bidang seni perfilman, pembuatan film, dan sinematografi',
                required_traits='creativity,openness,aestheticism',
                persyaratan_json=json.dumps([
                    'Mahasiswa aktif',
                    'Minat di dunia film',
                    'Siap kerja tim'
                ]),
                manfaat_json=json.dumps([
                    'Pengalaman produksi film',
                    'Portofolio sinematografi',
                    'Relasi komunitas film'
                ]),
                jadwal_json=json.dumps([
                    {'hari': 'Rabu', 'waktu': '18.00 - 20.00', 'kegiatan': 'Diskusi Film'},
                    {'hari': 'Sabtu', 'waktu': '09.00 - 12.00', 'kegiatan': 'Produksi Film'}
                ]),
                link='https://bit.ly/forum-sinema',
                contact_json=json.dumps({'name': 'Koordinator Sinema', 'phone': '0814-2222-3333', 'email': 'sinema@omnimap.ac.id'})
            ),

            Activity(
                nama='UKM Teater TITIK',
                kategori='UKM',
                tingkat_kesulitan='Tinggi',
                peserta='30/50',
                deadline='10 Maret 2026',
                lokasi='Auditorium Tel-U',
                deskripsi='UKM yang bergerak di bidang seni teater',
                required_traits='extraversion,creativity,openness',
                persyaratan_json=json.dumps([
                    'Mahasiswa aktif',
                    'Berani tampil di depan umum',
                    'Komitmen latihan'
                ]),
                manfaat_json=json.dumps([
                    'Kemampuan public speaking',
                    'Pengembangan ekspresi diri',
                    'Pengalaman pentas'
                ]),
                jadwal_json=json.dumps([
                    {'hari': 'Senin', 'waktu': '18.00 - 20.00', 'kegiatan': 'Latihan Akting'},
                    {'hari': 'Kamis', 'waktu': '18.00 - 20.00', 'kegiatan': 'Latihan Pementasan'}
                ]),
                link='https://bit.ly/teater-titik',
                contact_json=json.dumps({'name': 'Ketua Teater', 'phone': '0815-3333-4444', 'email': 'teater@omnimap.ac.id'})
            ),

            Activity(
                nama='UKM Luminosus Animation',
                kategori='UKM',
                tingkat_kesulitan='Tinggi',
                peserta='22/35',
                deadline='20 Maret 2026',
                lokasi='Lab Animasi Tel-U',
                deskripsi='UKM yang bergerak di bidang seni, desain grafis dan animasi',
                required_traits='creativity,aestheticism,conscientiousness',
                persyaratan_json=json.dumps([
                    'Mahasiswa aktif',
                    'Minat desain/animasi',
                    'Laptop pribadi'
                ]),
                manfaat_json=json.dumps([
                    'Skill animasi',
                    'Portofolio desain',
                    'Pengalaman project'
                ]),
                jadwal_json=json.dumps([
                    {'hari': 'Selasa', 'waktu': '18.00 - 20.00', 'kegiatan': 'Belajar Software Animasi'},
                    {'hari': 'Jumat', 'waktu': '18.00 - 20.00', 'kegiatan': 'Project Tim'}
                ]),
                link='https://bit.ly/luminosus-animation',
                contact_json=json.dumps({'name': 'Ketua Luminosus', 'phone': '0816-4444-5555', 'email': 'animasi@omnimap.ac.id'})
            ),

            Activity(
                nama='UKM SAWANDA',
                kategori='UKM',
                tingkat_kesulitan='Sedang',
                peserta='40/70',
                deadline='25 Februari 2026',
                lokasi='Balai Budaya Tel-U',
                deskripsi='Bidang seni dan kebudayaan khususnya budaya Sunda',
                required_traits='openness,agreeableness,creativity',
                persyaratan_json=json.dumps([
                    'Mahasiswa aktif',
                    'Minat budaya Sunda'
                ]),
                manfaat_json=json.dumps([
                    'Pelestarian budaya',
                    'Pengalaman seni tradisional',
                    'Sertifikat'
                ]),
                jadwal_json=json.dumps([
                    {'hari': 'Rabu', 'waktu': '16.00 - 18.00', 'kegiatan': 'Latihan Seni Sunda'}
                ]),
                link='https://bit.ly/sawanda-telu',
                contact_json=json.dumps({'name': 'Ketua SAWANDA', 'phone': '0817-5555-6666', 'email': 'sawanda@omnimap.ac.id'})
            ),

            Activity(
                nama='BEM Fakultas Informatika',
                kategori='Organisasi',
                tingkat_kesulitan='Tinggi',
                peserta='15/25',
                deadline='1 Februari 2026',
                lokasi='Gedung FIF Tel-U',
                deskripsi='Organisasi mahasiswa tingkat fakultas',
                required_traits='leadership,organization,extraversion',
                persyaratan_json=json.dumps([
                    'Mahasiswa Fakultas Informatika',
                    'IPK minimal 3.00'
                ]),
                manfaat_json=json.dumps([
                    'Pengalaman kepemimpinan',
                    'Relasi organisasi',
                    'Sertifikat'
                ]),
                jadwal_json=json.dumps([
                    {'hari': 'Senin', 'waktu': '18.00 - 20.00', 'kegiatan': 'Rapat BEM'}
                ]),
                link='https://bit.ly/bem-fif',
                contact_json=json.dumps({'name': 'Sekretaris BEM', 'phone': '0818-6666-7777', 'email': 'bemfif@omnimap.ac.id'})
            ),

            Activity(
                nama='Lomba Hackathon AI',
                kategori='Lomba',
                tingkat_kesulitan='Sangat Tinggi',
                peserta='75/150',
                deadline='15 Januari 2026',
                lokasi='Lab Komputer Tel-U',
                deskripsi='Kompetisi pemrograman dan AI',
                required_traits='conscientiousness,creativity,teamwork',
                persyaratan_json=json.dumps([
                    'Mahasiswa aktif',
                    'Menguasai dasar pemrograman',
                    'Tim 3–5 orang'
                ]),
                manfaat_json=json.dumps([
                    'Hadiah lomba',
                    'Sertifikat nasional',
                    'Pengalaman kompetisi'
                ]),
                jadwal_json=json.dumps([
                    {'hari': 'Sabtu', 'waktu': '08.00 - 20.00', 'kegiatan': 'Hackathon'}
                ]),
                link='https://bit.ly/hackathon-ai',
                contact_json=json.dumps({'name': 'Panitia Hackathon', 'phone': '0819-7777-8888', 'email': 'hackathon@omnimap.ac.id'})
            )
        ]

        for activity in activities:
            db.session.add(activity)
        
        db.session.commit()
        
        print("\n✅ DATABASE BERHASIL DI-SEED!")
        print("\n📋 DAFTAR LOGIN:")
        print("=" * 80)
        print(f"{'USERNAME':<25} {'PASSWORD':<20} {'NAMA':<30} {'ROLE':<10}")
        print("=" * 80)
        print(f"{'puti':<25} {'admin123':<20} {'Admin Puti':<30} {'ADMIN':<10}")
        
        all_users = User.query.filter_by(is_admin=False).all()
        for user in all_users:
            print(f"{user.username:<25} {'mahasiswa123':<20} {user.nama:<30} {'MAHASISWA':<10}")
        
        print("=" * 80)
        print(f"\n📊 Total: 1 Admin + {len(all_users)} Mahasiswa")
        print(f"📝 Status Tes: {len([u for u in all_users if u.status_tes == 'Selesai'])} Selesai, {len([u for u in all_users if u.status_tes != 'Selesai'])} Belum Selesai\n")

if __name__ == '__main__':
    seed_database()