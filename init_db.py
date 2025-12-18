"""
Script untuk inisialisasi database dengan 200 pertanyaan lengkap OMNI
Jalankan dengan: python init_db.py
"""

from app import app, db, Question

def populate_all_questions():
    """Populate database with all 200 questions for OMNI personality test"""
    
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
        
        # SENSATION_SEEKING - Conventionality (8 questions - REVERSE SCORED for sensation seeking)
        {"no": 193, "text": "Saya mengikuti aturan dan tradisi yang ada", "trait": "conventionality", "reverse": False},
        {"no": 194, "text": "Saya suka melanggar aturan yang tidak masuk akal", "trait": "conventionality", "reverse": True},
        {"no": 195, "text": "Saya menghargai nilai-nilai konvensional", "trait": "conventionality", "reverse": False},
        {"no": 196, "text": "Saya tidak peduli dengan norma sosial", "trait": "conventionality", "reverse": True},
        {"no": 197, "text": "Saya mengikuti ekspektasi masyarakat", "trait": "conventionality", "reverse": False},
        {"no": 198, "text": "Saya suka melakukan hal yang tidak biasa", "trait": "conventionality", "reverse": True},
        {"no": 199, "text": "Saya patuh pada otoritas", "trait": "conventionality", "reverse": False},
        {"no": 200, "text": "Saya mempertanyakan aturan yang ada", "trait": "conventionality", "reverse": True},
    ]
    
    print(f"📝 Preparing to add {len(all_questions)} questions...")
    
    # Clear existing questions
    deleted = Question.query.delete()
    print(f"🗑️  Deleted {deleted} existing questions")
    
    # Add new questions
    for q_data in all_questions:
        question = Question(
            text=q_data["text"],
            trait=q_data["trait"],
            reverse_scored=q_data["reverse"],
            order=q_data["no"]
        )
        db.session.add(question)
    
    db.session.commit()
    print(f"✅ Successfully added {len(all_questions)} questions to database")
    
    # Verify by trait
    print("\n📊 Questions per trait:")
    traits = [
        'energy', 'sociability', 'assertiveness', 'excitement',
        'warmth', 'trustfulness', 'sincerity', 'modesty',
        'dutifulness', 'orderliness', 'self_reliance', 'ambition',
        'anxiety', 'depression', 'moodiness', 'irritability',
        'aestheticism', 'intellect', 'flexibility', 'tolerance',
        'exhibitionism', 'self_indulgence', 'impulsiveness', 'hostility', 'conventionality'
    ]
    
    for trait in traits:
        count = Question.query.filter_by(trait=trait).count()
        print(f"  - {trait}: {count} questions")

if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        print("📦 Database tables created")
        
        # Populate questions
        populate_all_questions()
        
        # Verify total
        total_count = Question.query.count()
        print(f"\n✓ Total questions in database: {total_count}")
        
        # Show first 5 questions as sample
        print("\n📋 Sample questions:")
        sample = Question.query.order_by(Question.order).limit(5).all()
        for q in sample:
            reverse_marker = " (REVERSE)" if q.reverse_scored else ""
            print(f"  {q.order}. [{q.trait}] {q.text}{reverse_marker}")