import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Judul aplikasi
st.title("Kuesioner Keseimbangan Hormon E.D.S.O")

st.markdown("""
Jawab 40 pertanyaan berikut dengan skala:
- 1 = Tidak Setuju
- 2 = Kurang Setuju
- 3 = Netral
- 4 = Setuju
- 5 = Sangat Setuju
""")

# Pertanyaan per hormon
def ask_questions(hormon, questions):
    st.subheader(hormon)
    scores = []
    for i, q in enumerate(questions):
        scores.append(st.slider(f"{i+1}. {q}", 1, 5, 3))
    return np.mean(scores)

endorfin_qs = [
    "Saya merasa lebih baik setelah tertawa.",
    "Saya rutin berolahraga untuk meningkatkan mood.",
    "Saya bisa tetap tenang saat mengalami rasa sakit.",
    "Saya menikmati aktivitas yang memicu keringat.",
    "Saya merasa segar setelah aktivitas fisik.",
    "Saya suka mencari hiburan untuk menghilangkan stres.",
    "Saya merasa lega setelah menangis.",
    "Saya suka suasana ceria.",
    "Saya bisa melihat sisi lucu dalam situasi sulit.",
    "Saya mudah tertawa bersama orang lain."
]

dopamin_qs = [
    "Saya merasa puas setelah menyelesaikan target.",
    "Saya termotivasi dengan tantangan.",
    "Saya merasa senang mencentang to-do list.",
    "Saya suka membuat rencana kerja.",
    "Saya sering memecah tugas besar menjadi tugas kecil.",
    "Saya fokus pada pencapaian.",
    "Saya punya semangat tinggi saat mengejar tujuan.",
    "Saya merasa senang saat mendapat pengakuan.",
    "Saya merasa terdorong saat melihat progres kerja.",
    "Saya suka mengevaluasi pencapaian saya."
]

serotonin_qs = [
    "Saya merasa dihargai oleh rekan kerja.",
    "Saya merasa dipercaya oleh orang-orang sekitar saya.",
    "Saya merasa bangga jika memberi kontribusi positif.",
    "Saya merasa senang saat nama saya disebut secara positif.",
    "Saya suka memberi dukungan kepada orang lain.",
    "Saya bangga jika bisa memimpin dengan adil.",
    "Saya merasa nyaman saat ide saya diterima.",
    "Saya berusaha membuat orang merasa dihargai.",
    "Saya merasa senang saat dipercaya memegang tanggung jawab.",
    "Saya suka menjadi bagian dari sesuatu yang lebih besar."
]

oksitosin_qs = [
    "Saya nyaman membangun hubungan yang tulus.",
    "Saya suka membantu tanpa pamrih.",
    "Saya merasa tenang berada di dekat orang yang saya percaya.",
    "Saya terbuka terhadap perasaan orang lain.",
    "Saya suka menyapa atau menyemangati orang lain.",
    "Saya menikmati kerja tim yang harmonis.",
    "Saya sering berempati terhadap kesulitan orang lain.",
    "Saya suka suasana kerja yang hangat.",
    "Saya merasa senang saat ada kontak emosional yang kuat.",
    "Saya merasa puas jika bisa membuat orang lain nyaman."
]

# Skor per hormon
endorfin_score = ask_questions("Endorfin", endorfin_qs)
dopamin_score = ask_questions("Dopamin", dopamin_qs)
serotonin_score = ask_questions("Serotonin", serotonin_qs)
oksitosin_score = ask_questions("Oksitosin", oksitosin_qs)

# Radar Chart
labels = ['Endorfin', 'Dopamin', 'Serotonin', 'Oksitosin']
values = [endorfin_score, dopamin_score, serotonin_score, oksitosin_score]
values += values[:1]

angles = [n / float(len(labels)) * 2 * np.pi for n in range(len(labels))]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
ax.plot(angles, values, linewidth=2, linestyle='solid')
ax.fill(angles, values, alpha=0.3)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)
ax.set_yticklabels(["1", "2", "3", "4", "5"])
ax.set_title("Diagram Keseimbangan Hormon E.D.S.O", va='bottom')

st.pyplot(fig)

# Interpretasi
st.markdown("### Interpretasi Keseimbangan")
for label, val in zip(labels, values[:-1]):
    if val < 2.5:
        st.warning(f"{label}: Nilai rendah. Perlu perhatian lebih.")
    elif val > 4.0:
        st.info(f"{label}: Sangat kuat. Jaga agar tidak berlebihan.")
    else:
        st.success(f"{label}: Dalam kisaran seimbang.")
