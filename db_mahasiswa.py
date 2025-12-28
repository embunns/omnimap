import json
from app import app, db, User

def add_mahasiswa_belum_tes():
    with app.app_context():
        # ✅ DATA 20 MAHASISWA (Belum Tes)
        mahasiswa_baru = [
            # 6 Mahasiswa Custom
            {'nim': '1301220198', 'nama': 'Embun Nawang Sari', 'username': 'embunns', 'fakultas': 'FIF'},
            {'nim': '1301226270', 'nama': 'Anila Dwi Lestari', 'username': 'aniladwi', 'fakultas': 'FIF'},
            {'nim': '1301223456', 'nama': 'Joshua Pinem', 'username': 'joshuapinem', 'fakultas': 'FIF'},
            {'nim': '1301224567', 'nama': 'Yasmina Arethaya Hanjani', 'username': 'yasminaarethaya', 'fakultas': 'FIF'},
            {'nim': '1301225678', 'nama': 'Muhammad Rafie Hamizan', 'username': 'rafiehamizan', 'fakultas': 'FIF'},
            {'nim': '1301226789', 'nama': 'Rayhan Arsy Sashenka', 'username': 'rayhanarsy', 'fakultas': 'FIF'},
            
            # 14 Mahasiswa Tambahan
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
        
        # ✅ TAMBAHKAN KE DATABASE
        added_count = 0
        skipped_count = 0
        
        for mhs in mahasiswa_baru:
            # Cek apakah NIM sudah ada
            existing = User.query.filter_by(nim=mhs['nim']).first()
            if existing:
                print(f"⚠️  Skip: {mhs['nama']} ({mhs['nim']}) - NIM sudah ada")
                skipped_count += 1
                continue
            
            # Cek apakah username sudah ada
            existing_username = User.query.filter_by(username=mhs['username']).first()
            if existing_username:
                print(f"⚠️  Skip: {mhs['nama']} ({mhs['username']}) - Username sudah ada")
                skipped_count += 1
                continue
            
            user = User(
                nim=mhs['nim'],
                nama=mhs['nama'],
                email=f"{mhs['username']}@student.telkomuniversity.ac.id",
                username=mhs['username'],
                fakultas=mhs['fakultas'],
                is_admin=False,
                skor_rata_rata=None,
                status_tes='Belum Selesai',
                progress_profil=100,
                progress_tes=0,
                progress_eksplorasi=0,
                progress_kegiatan=0
            )
            
            user.set_password('mahasiswa123')
            db.session.add(user)
            added_count += 1
            print(f"✅ Tambah: {mhs['nama']} ({mhs['nim']}) - {mhs['fakultas']}")
        
        db.session.commit()
        
        print("\n" + "=" * 80)
        print(f"✅ BERHASIL MENAMBAHKAN {added_count} MAHASISWA BARU")
        if skipped_count > 0:
            print(f"⚠️  {skipped_count} mahasiswa di-skip (sudah ada)")
        print("=" * 80)
        
        # ✅ TAMPILKAN DAFTAR LOGIN MAHASISWA BARU
        print("\n📋 DAFTAR LOGIN MAHASISWA BARU:")
        print("=" * 80)
        print(f"{'USERNAME':<25} {'PASSWORD':<20} {'NAMA':<30} {'NIM':<15}")
        print("=" * 80)
        
        for mhs in mahasiswa_baru:
            print(f"{mhs['username']:<25} {'mahasiswa123':<20} {mhs['nama']:<30} {mhs['nim']:<15}")
        
        print("=" * 80)
        print(f"\n📊 Total Mahasiswa Belum Tes: {User.query.filter_by(is_admin=False, status_tes='Belum Selesai').count()}")
        print(f"📊 Total Mahasiswa Sudah Tes: {User.query.filter_by(is_admin=False, status_tes='Selesai').count()}")
        print(f"📊 Total Semua Mahasiswa: {User.query.filter_by(is_admin=False).count()}\n")

if __name__ == '__main__':
    print("\n🔄 MENAMBAHKAN MAHASISWA BARU KE DATABASE...")
    print("=" * 80)
    add_mahasiswa_belum_tes()