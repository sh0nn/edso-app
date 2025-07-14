
import streamlit as st
from fpdf import FPDF
import base64
from datetime import datetime

st.title("📋 Kuesioner E.D.S.O dan Laporan PDF")

# Fungsi untuk mengonversi skor ke kategori dan rekomendasi
def analyze_score(name, score):
    if score >= 8:
        level = "high"
    elif score >= 6:
        level = "medium"
    else:
        level = "low"
    return recommendation_template[name][level]

# Template rekomendasi
recommendation_template = {
    "Endorfin": {
        "high": ("Tinggi", "Kamu memiliki daya tahan mental yang kuat dan mampu mengelola stres dengan baik. Pertahankan gaya hidup sehat dan seimbang."),
        "medium": ("Cukup", "Kamu cukup tangguh, namun bisa ditingkatkan dengan olahraga rutin dan menjaga semangat."),
        "low": ("Rendah", "Tingkatkan hormon endorfin dengan lebih sering berolahraga, tertawa, dan beristirahat cukup.")
    },
    "Dopamin": {
        "high": ("Tinggi", "Kamu sangat termotivasi oleh target dan pencapaian. Pastikan tetap seimbang agar tidak mengorbankan etika atau kerja tim."),
        "medium": ("Cukup", "Kamu punya motivasi pribadi yang baik. Gunakan sistem reward dan tetap fokus pada progres."),
        "low": ("Rendah", "Perkuat motivasi dengan membuat tujuan jangka pendek, memberi reward pribadi, dan mencari inspirasi.")
    },
    "Serotonin": {
        "high": ("Tinggi", "Kamu percaya diri dan mampu membangun rasa hormat. Ini modal penting dalam kepemimpinan."),
        "medium": ("Cukup", "Kamu cukup dihargai dan percaya diri, namun bisa lebih baik dengan menumbuhkan apresiasi tim."),
        "low": ("Rendah", "Bangun rasa percaya diri melalui refleksi positif, ambil peran kecil dalam tim, dan cari umpan balik membangun.")
    },
    "Oksitosin": {
        "high": ("Tinggi", "Kamu memiliki koneksi sosial yang kuat. Ini memperkuat rasa aman dan kepercayaan dalam tim."),
        "medium": ("Cukup", "Hubungan sosialmu baik. Pertahankan dengan terus membangun kepercayaan tim."),
        "low": ("Rendah", "Bangun empati, beri dukungan pada rekan, dan buat lingkungan yang terbuka dan aman.")
    }
}

with st.form("edso_form"):
    name = st.text_input("Nama lengkap")
    email = st.text_input("Email")

    st.subheader("Endorfin")
    end_scores = [st.slider(f"Pertanyaan Endorfin {i+1}", 1, 5, 3) for i in range(10)]

    st.subheader("Dopamin")
    dop_scores = [st.slider(f"Pertanyaan Dopamin {i+1}", 1, 5, 3) for i in range(10)]

    st.subheader("Serotonin")
    ser_scores = [st.slider(f"Pertanyaan Serotonin {i+1}", 1, 5, 3) for i in range(10)]

    st.subheader("Oksitosin")
    oks_scores = [st.slider(f"Pertanyaan Oksitosin {i+1}", 1, 5, 3) for i in range(10)]

    submitted = st.form_submit_button("Buat Laporan PDF")

if submitted:
    avg_end = sum(end_scores) / 10
    avg_dop = sum(dop_scores) / 10
    avg_ser = sum(ser_scores) / 10
    avg_oks = sum(oks_scores) / 10

    hasil = {
        "Endorfin": analyze_score("Endorfin", avg_end),
        "Dopamin": analyze_score("Dopamin", avg_dop),
        "Serotonin": analyze_score("Serotonin", avg_ser),
        "Oksitosin": analyze_score("Oksitosin", avg_oks)
    }

    st.subheader("📊 Hasil Ringkasan")
    for k, v in hasil.items():
        st.markdown(f"**{k}** – {v[0]}: {v[1]}")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, f"Hasil Kuesioner E.D.S.O", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(200, 10, f"Nama: {name}", ln=True)
    pdf.cell(200, 10, f"Email: {email}", ln=True)
    pdf.cell(200, 10, f"Tanggal: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

    pdf.ln(10)
    for k, v in hasil.items():
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, f"{k} – {v[0]}", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 10, v[1])
        pdf.ln(2)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        with open(tmp.name, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="Laporan_EDSO_{name}.pdf">📥 Download PDF</a>'
            st.markdown(href, unsafe_allow_html=True)


    # Analisis gabungan Endorfin + Oksitosin
    def classify(score):
        if score >= 8:
            return "high"
        elif score >= 6:
            return "medium"
        else:
            return "low"

    eo_combo = (classify(avg_end), classify(avg_oks))
    combined_notes = {
        ("high", "high"): "Kamu adalah sosok yang sangat bersemangat dan penuh empati. Kombinasi ini mencerminkan pemimpin yang tangguh dan sangat peduli pada tim. Cocok untuk peran-peran yang membutuhkan stamina tinggi dan membina hubungan erat.",
        ("high", "medium"): "Kamu penuh semangat dan punya hubungan sosial yang baik. Namun, perlu sedikit lebih banyak membangun kepercayaan tim secara emosional.",
        ("high", "low"): "Kamu sangat kuat secara pribadi, tapi kurang membangun koneksi emosional. Waspadai kecenderungan terlalu individualis. Coba lebih hadir untuk orang lain.",
        ("medium", "high"): "Kamu cukup stabil dan punya hubungan sosial yang kuat. Gaya kepemimpinanmu cenderung mendukung dan kolaboratif.",
        ("medium", "medium"): "Kamu berada di tengah-tengah. Potensial untuk menjadi pemimpin seimbang, tapi masih bisa ditingkatkan dengan perhatian ke semangat dan hubungan tim.",
        ("medium", "low"): "Hubungan sosial bisa jadi penghambat bagimu. Cobalah lebih aktif mendengarkan dan membangun empati dalam tim.",
        ("low", "high"): "Kamu dicintai dan dipercaya orang lain, tapi sering merasa tidak cukup kuat atau semangat. Coba jaga stamina dan energi emosionalmu.",
        ("low", "medium"): "Kamu cenderung kelelahan dan relasi sosial kurang stabil. Berisiko burnout atau merasa tidak cukup dihargai.",
        ("low", "low"): "Waspadai kelelahan emosional dan keterasingan sosial. Coba mulai dari aktivitas menyenangkan bersama orang lain, perkuat keseimbangan kerja dan istirahat."
    }

    st.markdown("---")
    st.subheader("🔄 Analisis Gabungan: Endorfin & Oksitosin")
    st.info(combined_notes[eo_combo])

    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Analisis Gabungan (Endorfin + Oksitosin):", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 10, combined_notes[eo_combo])
