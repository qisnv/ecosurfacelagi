import streamlit as st
import pandas as pd

st.set_page_config(page_title="EcoSurface", page_icon="💧", layout="wide")

st.markdown("""
<style>
.card{
background:white;padding:18px;border-radius:12px;
border-left:6px solid #2E8B57;margin-bottom:12px;
box-shadow:0 2px 8px rgba(0,0,0,.08);
}
.success{background:#e8f5e9;padding:18px;border-radius:12px;}
.danger{background:#ffebee;padding:18px;border-radius:12px;}
</style>
""", unsafe_allow_html=True)

SAMPLING_GUIDE = {
    "pH":{"wadah":"Botol PE","volume":"100 mL","pengawet":"Tidak ada","penyimpanan":"4°C","holding_time":"< 2 jam","catatan":"Analisis segera."},
    "Suhu":{"wadah":"Botol Kaca","volume":"1 L","pengawet":"Tidak ada","penyimpanan":"In situ","holding_time":"Segera","catatan":"Diukur di lapangan."},
    "TSS":{"wadah":"Botol PE/Kaca","volume":"1 L","pengawet":"Tidak ada","penyimpanan":"4°C","holding_time":"7 hari","catatan":"Hindari pengadukan."},
    "TDS":{"wadah":"Botol PE","volume":"500 mL","pengawet":"Tidak ada","penyimpanan":"4°C","holding_time":"28 hari","catatan":"Filter 0,45 μm."},
    "DO":{"wadah":"Botol DO","volume":"300 mL","pengawet":"Winkler","penyimpanan":"4°C","holding_time":"8 jam","catatan":"Hindari gelembung."},
    "BOD":{"wadah":"Botol Amber","volume":"1 L","pengawet":"H2SO4 pH<2","penyimpanan":"4°C","holding_time":"48 jam","catatan":"Ideal <6 jam."},
    "COD":{"wadah":"Botol Kaca","volume":"500 mL","pengawet":"H2SO4 pH<2","penyimpanan":"4°C","holding_time":"28 hari","catatan":"Segera dinginkan."},
    "Nitrat":{"wadah":"Botol PE","volume":"250 mL","pengawet":"H2SO4 pH<2","penyimpanan":"4°C","holding_time":"28 hari","catatan":"Hindari kontaminasi."},
    "Nitrit":{"wadah":"Botol PE","volume":"250 mL","pengawet":"Pendinginan","penyimpanan":"4°C","holding_time":"48 jam","catatan":"Analisis cepat."},
    "Amonia":{"wadah":"Botol PE","volume":"500 mL","pengawet":"H2SO4 pH<2","penyimpanan":"4°C","holding_time":"28 hari","catatan":"Jaga kondisi asam."},
    "Fosfat":{"wadah":"Botol PE","volume":"250 mL","pengawet":"H2SO4 pH<2","penyimpanan":"4°C","holding_time":"28 hari","catatan":"Bebas fosfat."},
    "Sulfat":{"wadah":"Botol PE","volume":"250 mL","pengawet":"Tidak ada","penyimpanan":"4°C","holding_time":"28 hari","catatan":"Simpan dingin."},
    "Klorida":{"wadah":"Botol PE","volume":"250 mL","pengawet":"Tidak ada","penyimpanan":"4°C","holding_time":"28 hari","catatan":"Simpan dingin."},
    "Total Coliform":{"wadah":"Botol Steril","volume":"100 mL","pengawet":"Na2S2O3","penyimpanan":"4°C","holding_time":"24 jam","catatan":"Jaga sterilitas."},
    "Fecal Coliform":{"wadah":"Botol Steril","volume":"100 mL","pengawet":"Na2S2O3","penyimpanan":"4°C","holding_time":"24 jam","catatan":"Analisis cepat."},
    "Besi (Fe)":{"wadah":"Botol PE","volume":"500 mL","pengawet":"HNO3 pH<2","penyimpanan":"4°C","holding_time":"6 bulan","catatan":"Filtrasi untuk terlarut."},
    "Mangan (Mn)":{"wadah":"Botol PE","volume":"500 mL","pengawet":"HNO3 pH<2","penyimpanan":"4°C","holding_time":"6 bulan","catatan":"Simpan asam."}
}

WATER_STANDARDS = {
    "pH":{"tipe":"range","min":6.0,"max":9.0},
    "TSS":{"tipe":"<=","nilai":50},
    "DO":{"tipe":">=","nilai":4},
    "BOD":{"tipe":"<=","nilai":3},
    "COD":{"tipe":"<=","nilai":25},
    "Nitrat":{"tipe":"<=","nilai":0.5},
    "Nitrit":{"tipe":"<=","nilai":0.06},
    "Amonia":{"tipe":"<=","nilai":0.5},
    "Fosfat":{"tipe":"<=","nilai":0.5},
    "Total Coliform":{"tipe":"<=","nilai":100}
}

def card(title, text):
    st.markdown(f'<div class="card"><h4>{title}</h4>{text}</div>', unsafe_allow_html=True)

menu = st.sidebar.radio("Navigasi", ["Beranda","Panduan Sampling","Evaluasi Baku Mutu","Tentang Aplikasi"])

if menu == "Beranda":
    st.title("💧 EcoSurface")
    c1,c2 = st.columns(2)
    c1.metric("Parameter Sampling", len(SAMPLING_GUIDE))
    c2.metric("Parameter Baku Mutu", len(WATER_STANDARDS))
    st.info("Aplikasi pendukung pemantauan kualitas air permukaan.")

elif menu == "Panduan Sampling":
    st.title("🧪 Panduan Sampling")
    p = st.selectbox("Pilih Parameter", list(SAMPLING_GUIDE.keys()))
    d = SAMPLING_GUIDE[p]
    c1,c2 = st.columns(2)
    with c1:
        card("Wadah & Volume", f"Wadah: {d['wadah']}<br>Volume: {d['volume']}")
        card("Penyimpanan", f"Suhu: {d['penyimpanan']}<br>Holding Time: {d['holding_time']}")
    with c2:
        card("Pengawet", d['pengawet'])
        card("Catatan", d['catatan'])
    st.dataframe(pd.DataFrame(SAMPLING_GUIDE).T, use_container_width=True)

elif menu == "Evaluasi Baku Mutu":
    st.title("📈 Evaluasi Baku Mutu")
    p = st.selectbox("Parameter", list(WATER_STANDARDS.keys()))
    nilai = st.number_input("Nilai Hasil Analisis", min_value=0.0, step=0.01)
    if st.button("Evaluasi"):
        s = WATER_STANDARDS[p]
        if s["tipe"] == "range":
            ok = s["min"] <= nilai <= s["max"]
            baku = f"{s['min']} - {s['max']}"
            selisih = 0 if ok else min(abs(nilai-s["min"]), abs(nilai-s["max"]))
        elif s["tipe"] == "<=":
            ok = nilai <= s["nilai"]
            baku = str(s["nilai"])
            selisih = abs(nilai-s["nilai"])
        else:
            ok = nilai >= s["nilai"]
            baku = str(s["nilai"])
            selisih = abs(nilai-s["nilai"])

        cls = "success" if ok else "danger"
        status = "MEMENUHI BAKU MUTU" if ok else "TIDAK MEMENUHI BAKU MUTU"
        st.markdown(
            f'<div class="{cls}"><h2>{status}</h2>'
            f'<p>Parameter: {p}<br>Nilai Hasil: {nilai}<br>'
            f'Nilai Baku Mutu: {baku}<br>Selisih: {selisih:.2f}</p></div>',
            unsafe_allow_html=True
        )

else:
    st.title("ℹ️ Tentang Aplikasi")
    st.write("**EcoSurface** membantu panduan sampling dan evaluasi kualitas air permukaan.")
    st.write("Teknologi: Python & Streamlit")
