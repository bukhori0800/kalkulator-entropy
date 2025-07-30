import streamlit as st
import math
import re
import time


# Fungsi utama kalkulatornya
# =================================================================================

def calculate_entropy(password):
    """
    Menghitung skor entropy dari sebuah password.
    Entropy (E) dihitung dengan rumus: E = L * log2(N)
    di mana L adalah panjang password dan N adalah jumlah kemungkinan karakter (character set).
    """
    if not password:
        return 0

    charset = 0
    # Cek huruf kecil (a-z)
    if any(c.islower() for c in password):
        charset += 26
    # Cek huruf besar (A-Z)
    if any(c.isupper() for c in password):
        charset += 26
    # Cek angka (0-9)
    if any(c.isdigit() for c in password):
        charset += 10
    # Cek simbol yang umum
    symbols = r"!@#$%^&*()_\-=><\.,:'+"
    if any(c in symbols for c in password):
        charset += len(symbols)
    
    # Menghindari log(0) atau log(1) jika charset sangat kecil
    if charset <= 1:
        return 0
        
    entropy = len(password) * math.log2(charset)
    return round(entropy, 2)

def classify_entropy(entropy):
    """
    Mengklasifikasikan kekuatan password berdasarkan skor entropy.
    """
    if entropy < 28:
        return "Sangat Lemah"
    elif entropy < 35:
        return "Lemah"
    elif entropy < 59:
        return "Sedang"
    elif entropy < 127:
        return "Kuat"

# =================================================================================
# STRUKTUR APLIKASI WEB STREAMLIT
# =================================================================================

# Konfigurasi haalaman
st.set_page_config(
    page_title="Kalkulator Entropy Password",
    page_icon="🔐",
    layout="wide"
)

# Custom CSS untuk mempercantik tampilan
st.markdown("""
<style>
    .main-title {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    .password-metrics {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .strength-indicator {
        padding: 1rem;
        border-radius: 20px;
        text-align: center;
        margin: 1rem 0;
        font-size: 1.5rem;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        animation: fadeInUp 0.8s ease-out;
    }
    
    .strength-very-weak {
        background: linear-gradient(135deg, #ff416c 0%, #ff4757 100%);
        color: white;
        animation: pulse 2s infinite;
    }
    
    .strength-weak {
        background: linear-gradient(135deg, #ffa726 0%, #fb8c00 100%);
        color: white;
    }
    
    .strength-medium {
        background: linear-gradient(135deg, #66bb6a 0%, #43a047 100%);
        color: white;
    }
    
    .strength-strong {
        background: linear-gradient(135deg, #42a5f5 0%, #1e88e5 100%);
        color: white;
        animation: glow 2s ease-in-out infinite alternate;
    }
            
    .strength-very-strong {
    background: linear-gradient(135deg, #8e24aa 0%, #5e35b1 100%);
    color: white;
    animation: glow 2s ease-in-out infinite alternate;
    }

    
    .entropy-display {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .entropy-score {
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .tips-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .theory-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
    }
    
    .progress-container {
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .stProgress .st-bo {
        background: linear-gradient(90deg, #ff416c, #ff4757, #ffa726, #66bb6a, #42a5f5) !important;
        height: 20px !important;
        border-radius: 10px !important;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    @keyframes glow {
        from {
            box-shadow: 0 0 20px rgba(66, 165, 245, 0.5);
        }
        to {
            box-shadow: 0 0 30px rgba(66, 165, 245, 0.8);
        }
    }
    
    .password-input {
        font-size: 1.2rem !important;
        padding: 1rem !important;
        border-radius: 10px !important;
        border: 2px solid #e0e0e0 !important;
    }
    
    .password-input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- JUDUL DAN PENDAHULUAN ---

add_selectbox = st.sidebar.selectbox(
    "Select Page: ",
    ("Calculator", "Tips")
)

if add_selectbox == "Calculator":
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 0.5rem;">
        <span style="font-size: 2.5rem;">🔐</span>
        <h1 class="main-title" style="margin: 0;">Analisis dan Pengukuran Keamanan Password</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="padding-left: 0.5rem; padding-right: 5rem;">
        <p style="text-align: justify; font-size: 1.05rem;">
            Aplikasi ini dirancang untuk menganalisis dan mengukur kekuatan password berdasarkan tingkat kompleksitasnya.
            Melalui perhitungan <strong>entropy</strong>, pengguna dapat mengetahui seberapa aman password yang digunakan
            terhadap berbagai jenis serangan seperti <em>brute-force</em> atau <em>dictionary attack</em>. 
            Semakin tinggi nilai entropi, semakin sulit password untuk ditebak dan semakin tinggi pula tingkat keamanannya.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # --- BAGIAN KALKULATOR INTERAKTIF ---
    st.header("🔑 Kalkulator Kekuatan Password")

    # Kolom untuk input dan toggle
    col_input, col_toggle = st.columns([4, 1])

    with col_input:
        password_input = st.text_input(
            "Masukkan password Anda di sini:", 
            type="password",
            help="Password yang Anda masukkan tidak disimpan. Kalkulasi dilakukan secara real-time di browser Anda.",
            key="password_input"
        )

    with col_toggle:
        st.write("")  # Spacer
        show_password = st.checkbox("👁️ Tampilkan")

    if show_password and password_input:
        st.text_input("Password Anda:", value=password_input, disabled=True)

    if password_input:
        # Animasi loading
        with st.spinner('🔍 Menganalisis keamanan password...'):
            time.sleep(0.3)  # Simulasi loading
        
        # Hitung entropy dan klasifikasikan
        entropy_score = calculate_entropy(password_input)
        strength_category = classify_entropy(entropy_score)

        # Menentukan CSS class berdasarkan kategori
        if strength_category == "Sangat Lemah":
            css_class = "strength-very-weak"
            emoji = "🔴"
            risk_text = "⚠️ BAHAYA TINGGI"
        elif strength_category == "Sedang":
            css_class = "strength-medium"
            emoji = "🟡"
            risk_text = "⚠️ RISIKO SEDANG"
        elif strength_category == "Kuat":
            css_class = "strength-strong"
            emoji = "🟢"
            risk_text = "✅ CUKUP AMAN"
        elif strength_category == "Sangat kuat":
            css_class = "strength-very-strong"
            emoji = "🔵"
            risk_text = "🛡️ SANGAT AMAN"
        else: # Sangat Kuat
            css_class = "strength-very-strong"
            emoji = "🔵"
            risk_text = "🛡️ SANGAT AMAN"
        
        # Layout hasil dengan 3 kolom
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            # Tampilkan metrics dasar
            st.markdown(f"""
            <div class="password-metrics">
                <h3 style="margin-bottom: 1rem;">📊 Metrics</h3>
                <p><strong>📏 Panjang:</strong> {len(password_input)} karakter</p>
                <p><strong>🔢 Charset:</strong> {26 if any(c.islower() for c in password_input) else 0} + 
                    {26 if any(c.isupper() for c in password_input) else 0} + 
                    {10 if any(c.isdigit() for c in password_input) else 0} + 
                    {22 if any(c in "!@#$%^&*()_\-=><\.,:'+" for c in password_input) else 0}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Tampilan Entropy Scorenya
            st.markdown(f"""
            <div class="entropy-display">
                <h2 style="margin-bottom: 1rem;">🎯 Entropy Analysis</h2>
                <div class="entropy-score">{entropy_score}</div>
                <p style="font-size: 1.2rem; margin-bottom: 1rem;">bits</p>
                <p style="font-size: 1rem; opacity: 0.9;">Semakin tinggi skor, semakin aman password Anda</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Progress bar dengan container yang dipercantik
            st.markdown('<div class="progress-container">', unsafe_allow_html=True)
            progress_value = min(entropy_score / 100.0, 1.0)
            st.progress(progress_value)
            st.caption(f"📈 Visualisasi Kekuatan: {progress_value*100:.1f}% dari skala maksimal")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            # Indikator kekuatan dengan animasi
            st.markdown(f"""
            <div class="strength-indicator {css_class}">
                {emoji}<br>
                {strength_category}<br>
                <small style="font-size: 0.8rem; opacity: 0.9;">{risk_text}</small>
            </div>
            """, unsafe_allow_html=True)
        
        # Checklist keamanan dengan styling menarik
        st.markdown("### ✅ Analisis Komponen Password")
        
        # Buat checklist dengan 4 kolom
        check_col1, check_col2, check_col3, check_col4 = st.columns(4)
        
        checks = [
            ("📏 Panjang ≥ 12", len(password_input) >= 12),
            ("🔡 Huruf kecil", any(c.islower() for c in password_input)),
            ("🔠 Huruf besar", any(c.isupper() for c in password_input)),
            ("🔢 Angka", any(c.isdigit() for c in password_input)),
        ]
        
        cols = [check_col1, check_col2, check_col3, check_col4]
        
        for i, (check_text, is_passed) in enumerate(checks):
            with cols[i]:
                if is_passed:
                    st.success(f"✅ {check_text}")
                else:
                    st.error(f"❌ {check_text}")
        
        # Tambahan untuk simbol
        has_symbols = any(c in "!@#$%^&*()_\-=><\.,:'+" for c in password_input)
        if has_symbols:
            st.success("✅ 🔣 Mengandung simbol khusus")
        else:
            st.error("❌ 🔣 Tidak ada simbol khusus")

    st.markdown("---")

    # --- BAGIAN ANALISIS DATASET terhubung ke kaggler rockyou ---
    st.header("📊 Studi Kasus: Analisis Dataset `rockyou.txt`")
    st.write("Sebagai bagian dari penelitian, dilakukan analisis terhadap **14 juta password** dari dataset [`rockyou.txt`](https://www.kaggle.com/datasets/wjburns/common-password-list-rockyoutxt)")

    try:
        img_col1, img_col2 = st.columns(2)
        with img_col1:
            st.image("diagram pie.png")
        with img_col2:
            st.image("diagram histogram.png",)
    except FileNotFoundError:
        st.info("💡 Gambar diagram akan ditampilkan jika file `diagram pie.png` dan `diagram histogram.png` tersedia di folder yang sama.")

elif add_selectbox == "Tips":
    # --- BAGIAN PENJELASAN TEORI ---
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2.5rem;">
            <h1 class="main-title" style="margin-bottom: 0.5rem;">
                Tips Keamanan Password
            </h1>
            <p class="subtitle" style="font-size: 1.25rem; color: #764ba2;">
                Tingkatkan keamanan akun Anda dengan password yang kuat dan unik
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
    <div class="theory-card">
        <h2>🧮 Apa itu Entropy?</h2>
        <p style="margin-bottom: 1rem;">
            Dalam konteks keamanan password, <strong>entropy</strong> adalah ukuran ketidakpastian atau keacakan sebuah password.
            Semakin tinggi nilai entropynya, semakin sulit password tersebut untuk ditebak oleh peretas
            (baik oleh manusia maupun oleh komputer melalui serangan <em>brute-force</em>).
        </p>
        <p style="margin-bottom: 1rem;">
            Skor entropy dihitung berdasarkan dua faktor utama:
        </p>
        <ul style="padding-left: 1.5rem;">
            <li><strong>Panjang Password (L):</strong> Jumlah karakter dalam password.</li>
            <li><strong>Kumpulan Karakter (N):</strong> Variasi karakter yang digunakan (misalnya, hanya huruf kecil, atau campuran huruf besar, huruf kecil, angka, dan simbol).</li>
        </ul>
        <p style="margin-top: 1rem;"><strong>Rumus Entropy:</strong></p>
        <div style="text-align: center; margin-top: 0.5rem;">
            <span style="background-color: #f0f0f0; padding: 6px 12px; border-radius: 6px; display: inline-block; font-weight: bold;">
                H = L × log₂(N)
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)


    with col2:
        st.markdown("""
        <div class="theory-card">
            <h2>🛡️ Mengapa Ini Penting?</h2>
            <p>Setiap hari, banyak upaya pembobolan data. Password yang mudah ditebak seperti "123456" atau "password" menjadi target utama.</p>
            <p>
                Dengan memahami konsep entropy, Anda dapat:
            </p>
            <ul style="padding-left: 1.5rem;">
                <li>Membuat keputusan yang lebih baik saat membuat password baru.</li>
                <li>Menilai risiko dari password yang sedang Anda gunakan.</li>
                <li>Menghindari pola umum yang membuat password Anda rentan.</li>
                <li>Menghindari terjadinya peretasan.</li>
                <li>Mengetahui nilai keamanan password Anda.</li>        
            </ul>
            <p>
                Pemahaman terhadap entropy sangat penting dalam dunia keamanan siber modern. 
                Dengan menerapkannya, kita dapat membangun sistem autentikasi yang jauh lebih aman.
            </p>
        </div>
        """, unsafe_allow_html=True)


    st.markdown("---")

    # --- BAGIAN TIPS ---
    st.header("💡 Tips Membuat Password yang Kuat")

    # Bagi tips menjadi 2 kolom
    tip_col1, tip_col2 = st.columns(2)

    with tip_col1:
        st.markdown("""
        <div class="tips-card">
            <h3>✅ Yang Harus Dilakukan</h3>
            <ul>
                <li><strong>🎯 Gunakan Panjang, Bukan Kompleksitas yang Rumit:</strong> Password yang lebih panjang secara eksponensial lebih sulit ditebak. "saya suka makan nasi goreng pedas" jauh lebih kuat daripada "P@ssw0rd1!".</li>
                <li><strong>🔤 Kombinasikan Jenis Karakter:</strong> Gunakan campuran huruf besar, huruf kecil, angka, dan simbol.</li>
                <li><strong>🔄 Unik untuk Setiap Akun:</strong> Jangan pernah menggunakan password yang sama untuk beberapa layanan.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with tip_col2:
        st.markdown("""
        <div class="tips-card">
            <h3>❌ Yang Harus Dihindari</h3>
            <ul>
                <li><strong>🚫 Hindari Informasi Pribadi:</strong> Jangan gunakan nama, tanggal lahir, atau kata-kata umum yang mudah dihubungkan dengan Anda.</li>
                <li><strong>📚 Hindari Kata Kamus:</strong> Password yang hanya terdiri dari kata-kata kamus mudah ditebak.</li>
                <li><strong>🔧 Gunakan Manajer Password:</strong> Pertimbangkan untuk menggunakan aplikasi manajer password untuk membuat dan menyimpan password yang sangat kuat dan unik.</li>
                <li><strong>❗ Hindari Pengulangan Kata:</strong> Jangan menggunakan kata atau pola yang diulang.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Footer dengan styling yang lebih menarik
st.markdown("""
<div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px; margin-top: 2rem;'>
    <h3>🔬 Password Entropy Calculator</h3>
    <p>Menggunakan formula matematika H = L × log₂(N) untuk analisis keamanan yang akurat</p>
    <hr style='border-color: rgba(255,255,255,0.3); margin: 1rem 0;'>
    <p style='margin: 0; opacity: 0.8;'>© 2025 - Muhammad Bukhori | Informatika | Universitas Gunadarma</p>
</div>
""", unsafe_allow_html=True)