import streamlit as st
import pandas as pd
import os
import datetime
import random

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Swasthya Sahay | ಸಾರ್ವಜನಿಕ ಆರೋಗ್ಯ ದೂರು ವ್ಯವಸ್ಥೆ",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MODERN HEALTH-TECH CSS STYLING ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    .stApp {
        background: radial-gradient(circle at top left, #f0fdf4 0%, #f8fafc 50%, #f1f5f9 100%);
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #0f172a;
    }
    
    /* Sidebar Polish */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    section[data-testid="stSidebar"] .stRadio label {
        color: #f1f5f9 !important;
        font-weight: 500;
        font-size: 0.95rem;
    }
    
    /* Hero Header Banner */
    .hero-banner {
        background: linear-gradient(135deg, #065f46 0%, #0d9488 50%, #0284c7 100%);
        padding: 2.5rem;
        border-radius: 20px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 20px 25px -5px rgba(13, 148, 136, 0.2);
    }
    .hero-title {
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        margin-bottom: 0.4rem;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        opacity: 0.95;
        font-weight: 400;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        padding: 0.65rem 1.4rem;
        box-shadow: 0 4px 12px rgba(13, 148, 136, 0.25);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(13, 148, 136, 0.35);
        background: linear-gradient(135deg, #0f766e 0%, #115e59 100%);
    }
    
    /* Metrics */
    div[data-testid="stMetric"] {
        background: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
        border: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

DATA_FILE = "complaints.csv"

# Comprehensive Database of All Districts, Talukas & Government Hospitals in Karnataka
HOSPITAL_DATABASE = {
    "Bagalkot / ಬಾಗಲಕೋಟೆ": {
        "Bagalkot": ["District Hospital Bagalkot", "General Hospital Bagalkot"],
        "Badami": ["Taluk Hospital Badami"],
        "Hungund": ["Taluk Hospital Hungund"],
        "Jamkhandi": ["Taluk Hospital Jamkhandi"],
        "Mudhol": ["Taluk Hospital Mudhol"],
        "Bilagi": ["Taluk Hospital Bilagi"],
        "Rabkavi Banhatti": ["Community Health Centre Rabkavi"]
    },
    "Ballari / ಬಳ್ಳಾರಿ": {
        "Ballari": ["VIMS Hospital Ballari", "District Hospital Ballari"],
        "Hospet": ["Taluk Hospital Hospet"],
        "Sandur": ["Taluk Hospital Sandur"],
        "Siruguppa": ["Taluk Hospital Siruguppa"],
        "Kudligi": ["Taluk Hospital Kudligi"]
    },
    "Belagavi / ಬೆಳಗಾವಿ": {
        "Belagavi": ["District Hospital Belagavi", "BIMS Hospital Belagavi"],
        "Chikkodi": ["Government General Hospital Chikkodi"],
        "Bailhongal": ["Taluk Hospital Bailhongal"],
        "Athani": ["Taluk Hospital Athani"],
        "Gokak": ["Taluk Hospital Gokak"],
        "Raybag": ["Taluk Hospital Raybag"],
        "Saundatti": ["Taluk Hospital Saundatti"],
        "Kittur": ["Community Health Centre Kittur"],
        "Khanapur": ["Taluk Hospital Khanapur"],
        "Hukkeri": ["Taluk Hospital Hukkeri"],
        "Nippani": ["Taluk Hospital Nippani"]
    },
    "Bengaluru Urban / ಬೆಂಗಳೂರು ನಗರ": {
        "Bengaluru North": ["Bowring & Lady Curzon Hospital", "KC General Hospital Malleshwaram"],
        "Bengaluru South": ["Victoria Hospital Fort", "Vanivilas Women and Children Hospital"],
        "Bengaluru East": ["General Hospital Jayanagar", "C.V. Raman General Hospital"],
        "Anekal": ["Taluk Hospital Anekal"]
    },
    "Bidar / ಬೀದರ್": {
        "Bidar": ["District Hospital Bidar", "BRIMS Teaching Hospital"],
        "Bhalki": ["Taluk Hospital Bhalki"],
        "Basavakalyan": ["Taluk Hospital Basavakalyan"],
        "Humnabad": ["Taluk Hospital Humnabad"],
        "Aurad": ["Taluk Hospital Aurad"]
    },
    "Chamarajanagar / ಚಾಮರಾಜನಗರ": {
        "Chamarajanagar": ["District Hospital Chamarajanagar"],
        "Kollegal": ["Sub-Divisional Hospital Kollegal"],
        "Gundlupet": ["Taluk Hospital Gundlupet"],
        "Yelandur": ["Community Health Centre Yelandur"]
    },
    "Chikkaballapura / ಚಿಕ್ಕಬಳ್ಳಾಪುರ": {
        "Chikkaballapura": ["District Hospital Chikkaballapura"],
        "Bagepalli": ["Taluk Hospital Bagepalli"],
        "Chintamani": ["Taluk Hospital Chintamani"],
        "Gauribidanur": ["Taluk Hospital Gauribidanur"],
        "Sidlaghatta": ["Taluk Hospital Sidlaghatta"]
    },
    "Chikkamagaluru / ಚಿಕ್ಕಮಗಳೂರು": {
        "Chikkamagaluru": ["District Hospital Chikkamagaluru"],
        "Kadur": ["Taluk Hospital Kadur"],
        "Koppa": ["Taluk Hospital Koppa"],
        "Mudigere": ["Taluk Hospital Mudigere"],
        "Narasimharajapura": ["Taluk Hospital NR Pura"],
        "Sringeri": ["Taluk Hospital Sringeri"],
        "Tarikere": ["Taluk Hospital Tarikere"]
    },
    "Chitradurga / ಚಿತ್ರದುರ್ಗ": {
        "Chitradurga": ["District Hospital Chitradurga"],
        "Challakere": ["Taluk Hospital Challakere"],
        "Hiriyur": ["Taluk Hospital Hiriyur"],
        "Hosadurga": ["Taluk Hospital Hosadurga"],
        "Molakalmuru": ["Taluk Hospital Molakalmuru"]
    },
    "Dakshina Kannada / ದಕ್ಷಿಣ ಕನ್ನಡ": {
        "Mangaluru": ["Government Lady Goschen Hospital", "Wenlock District Hospital Mangaluru"],
        "Bantwal": ["Taluk Hospital Bantwal"],
        "Puttur": ["Government Hospital Puttur"],
        "Belthangady": ["Taluk Hospital Belthangady"],
        "Sullia": ["Taluk Hospital Sullia"]
    },
    "Davanagere / ದಾವಣಗೆರೆ": {
        "Davanagere": ["Chigateri District Hospital", "McGann Teaching Hospital"],
        "Harihar": ["Taluk Hospital Harihar"],
        "Honnali": ["Taluk Hospital Honnali"],
        "Nyamati": ["Community Health Centre Nyamati"],
        "Jagalur": ["Taluk Hospital Jagalur"]
    },
    "Dharwad / ಧಾರವಾಡ": {
        "Dharwad": ["District Hospital Dharwad", "KIMS Hospital Dharwad"],
        "Hubballi": ["Karnataka Institute of Medical Sciences (KIMS)", "Civil Hospital Hubballi"],
        "Navalgund": ["Taluk Hospital Navalgund"],
        "Kundgol": ["Taluk Hospital Kundgol"],
        "Alnavar": ["Community Health Centre Alnavar"]
    },
    "Gadag / ಗದಗ": {
        "Gadag": ["GIMS Teaching Hospital Gadag", "District Hospital Gadag"],
        "Ron": ["Taluk Hospital Ron"],
        "Shirhatti": ["Taluk Hospital Shirhatti"],
        "Mundargi": ["Taluk Hospital Mundargi"],
        "Nargund": ["Taluk Hospital Nargund"]
    },
    "Hassan / ಹಾಸನ": {
        "Hassan": ["HIMS Teaching Hospital", "District Hospital Hassan"],
        "Arsikere": ["Taluk Hospital Arsikere"],
        "Channarayapatna": ["Taluk Hospital Channarayapatna"],
        "Holenarasipura": ["Taluk Hospital Holenarasipura"],
        "Sakleshpur": ["Taluk Hospital Sakleshpur"],
        "Belur": ["Taluk Hospital Belur"],
        "Alur": ["Community Health Centre Alur"]
    },
    "Haveri / ಹಾವೇರಿ": {
        "Haveri": ["District Hospital Haveri"],
        "Ranebennur": ["Taluk Hospital Ranebennur"],
        "Byadgi": ["Taluk Hospital Byadgi"],
        "Hirekerur": ["Taluk Hospital Hirekerur"],
        "Shiggav": ["Taluk Hospital Shiggaon"],
        "Savanur": ["Taluk Hospital Savanur"]
    },
    "Kalaburagi (Gulbarga) / ಕಲಬುರಗಿ": {
        "Kalaburagi": ["District Government Hospital Kalaburagi", "Super Speciality Hospital Kalaburagi", "ESIC Medical College & Hospital"],
        "Aland": ["Community Health Centre Aland", "Taluk General Hospital Aland"],
        "Afzalpur": ["Taluk Hospital Afzalpur", "CHC Dudhani"],
        "Chincholi": ["Taluk Hospital Chincholi"],
        "Jevargi": ["Taluk Hospital Jevargi"],
        "Sedam": ["Taluk Hospital Sedam"],
        "Yadrami": ["Community Health Centre Yadrami"]
    },
    "Kodagu / ಕೊಡಗು": {
        "Madikeri": ["District Hospital Madikeri"],
        "Virajpet": ["Taluk General Hospital Virajpet"],
        "Somwarpet": ["Taluk Hospital Somwarpet"]
    },
    "Kolar / ಕೋಲಾರ": {
        "Kolar": ["District Hospital Kolar", "RL Jalappa Hospital"],
        "Bangarapet": ["Taluk Hospital Bangarapet"],
        "Malur": ["Taluk Hospital Malur"],
        "Mulbagal": ["Taluk Hospital Mulbagal"],
        "Srinivaspur": ["Taluk Hospital Srinivaspur"]
    },
    "Koppal / ಕೊಪ್ಪಳ": {
        "Koppal": ["District Hospital Koppal", "KIMS Koppal"],
        "Gangavathi": ["Taluk Hospital Gangavathi"],
        "Yelburga": ["Taluk Hospital Yelburga"],
        "Kushtagi": ["Taluk Hospital Kushtagi"]
    },
    "Mandya / ಮಂಡ್ಯ": {
        "Mandya": ["Mandya Institute of Medical Sciences (MIMS)", "District Hospital Mandya"],
        "Maddur": ["Taluk Hospital Maddur"],
        "Malavalli": ["Taluk Hospital Malavalli"],
        "Srirangapatna": ["Taluk Hospital Srirangapatna"],
        "Pandavapura": ["Taluk Hospital Pandavapura"],
        "Nagamangala": ["Taluk Hospital Nagamangala"],
        "Krishnarajapet": ["Taluk Hospital KR Pet"]
    },
    "Mysuru / ಮೈಸೂರು": {
        "Mysuru": ["K.R. Hospital Mysuru", "Cheluvamba Hospital", "District Hospital Mysuru"],
        "Nanjangud": ["Taluk General Hospital Nanjangud"],
        "Hunsur": ["Taluk Hospital Hunsur"],
        "K.R. Nagar": ["Taluk Hospital KR Nagar"],
        "Periyapatna": ["Taluk Hospital Periyapatna"],
        "T. Narasipura": ["Taluk Hospital T. Narasipura"],
        "Heggadadevankote": ["Taluk Hospital HD Kote"]
    },
    "Raichur / ರಾಯಚೂರು": {
        "Raichur": ["RIMS Teaching Hospital", "District Hospital Raichur"],
        "Manvi": ["Taluk Hospital Manvi"],
        "Sindhanur": ["Taluk Hospital Sindhanur"],
        "Devadurga": ["Taluk Hospital Devadurga"],
        "Maski": ["Community Health Centre Maski"]
    },
    "Ramanagara / ರಾಮನಗರ": {
        "Ramanagara": ["District Hospital Ramanagara"],
        "Channapatna": ["Taluk Hospital Channapatna"],
        "Kanakapura": ["Taluk Hospital Kanakapura"],
        "Magadi": ["Taluk Hospital Magadi"]
    },
    "Shivamogga / ಶಿವಮೊಗ್ಗ": {
        "Shivamogga": ["McGann District Hospital", "SIMS Teaching Hospital"],
        "Bhadravathi": ["Taluk Hospital Bhadravathi"],
        "Sagara": ["Sub-Divisional Hospital Sagara"],
        "Shikaripura": ["Taluk Hospital Shikaripura"],
        "Sorab": ["Taluk Hospital Sorab"],
        "Tirthahalli": ["Taluk Hospital Tirthahalli"],
        "Hosanagara": ["Taluk Hospital Hosanagara"]
    },
    "Tumakuru / ತುಮಕೂರು": {
        "Tumakuru": ["District Hospital Tumakuru", "TSIIMS Hospital"],
        "Madhugiri": ["Sub-Divisional Hospital Madhugiri"],
        "Tiptur": ["Taluk Hospital Tiptur"],
        "Sira": ["Taluk Hospital Sira"],
        "Gubbi": ["Taluk Hospital Gubbi"],
        "Kunigal": ["Taluk Hospital Kunigal"],
        "Koratagere": ["Taluk Hospital Koratagere"],
        "Pavagada": ["Taluk Hospital Pavagada"]
    },
    "Udupi / ಉಡುಪಿ": {
        "Udupi": ["District Hospital Udupi"],
        "Kundapura": ["Government Hospital Kundapura"],
        "Karkala": ["Taluk Hospital Karkala"]
    },
    "Uttara Kannada / ಉತ್ತರ ಕನ್ನಡ": {
        "Karwar": ["District Hospital Karwar"],
        "Sirsi": ["Sub-Divisional Hospital Sirsi"],
        "Kumta": ["Taluk Hospital Kumta"],
        "Bhatkal": ["Taluk Hospital Bhatkal"],
        "Haliyal": ["Taluk Hospital Haliyal"],
        "Yellapur": ["Taluk Hospital Yellapur"],
        "Ankola": ["Taluk Hospital Ankola"]
    },
    "Vijayapura / ವಿಜಯಪುರ": {
        "Vijayapura": ["District Hospital Vijayapura", "BLDE Teaching Hospital"],
        "Basavana Bagevadi": ["Taluk Hospital Basavana Bagevadi"],
        "Indi": ["Taluk Hospital Indi"],
        "Muddebihal": ["Taluk Hospital Muddebihal"],
        "Sindagi": ["Taluk Hospital Sindagi"]
    },
    "Yadgir / ಯಾದಗಿರಿ": {
        "Yadgir": ["District Hospital Yadgir", "YIMS Hospital"],
        "Shahapur": ["Taluk Hospital Shahapur"],
        "Shorapur": ["Taluk Hospital Shorapur"],
        "Hunasagi": ["Community Health Centre Hunasagi"]
    }
}

def load_data():
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        df_init = pd.DataFrame(columns=[
            "Complaint ID", "Intake Channel", "District", "Taluka", "Hospital", 
            "Department / Category", "Language", "Voice / Text Transcript", 
            "Status", "Doctor Action / Official Response", "Patient Rating", "Escalation Status", "Timestamp"
        ])
        df_init.to_csv(DATA_FILE, index=False)
    try:
        return pd.read_csv(DATA_FILE)
    except Exception:
        df_init = pd.DataFrame(columns=[
            "Complaint ID", "Intake Channel", "District", "Taluka", "Hospital", 
            "Department / Category", "Language", "Voice / Text Transcript", 
            "Status", "Doctor Action / Official Response", "Patient Rating", "Escalation Status", "Timestamp"
        ])
        df_init.to_csv(DATA_FILE, index=False)
        return df_init

# --- SIDEBAR NAVIGATION ---
st.sidebar.markdown("<h2 style='color: #2dd4bf; font-weight: 700;'>🏥 Navigation / ಆಯ್ಕೆಗಳು</h2>", unsafe_allow_html=True)
portal_choice = st.sidebar.radio(
    "Select Portal / ವಿಭಾಗ", 
    [
        "🗣️ Citizen Intake & Tracking / ದೂರು ಸಲ್ಲಿಕೆ", 
        "🩺 Doctor & Staff Portal / ವೈದ್ಯರ ಪೋರ್ಟಲ್", 
        "📊 Admin Dashboard / ಮೇಲ್ವಿಚಾರಣಾ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್"
    ]
)
st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div style='color: #94a3b8; font-size: 0.85rem;'>
        <b>Solvathon 2026 Project</b><br>
        Rural Healthcare Grievance & Staff Accountability Platform.
    </div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# PORTAL 1: CITIZEN INTAKE & PATIENT TRACKING
# ---------------------------------------------------------
if portal_choice == "🗣️ Citizen Intake & Tracking / ದೂರು ಸಲ್ಲಿಕೆ":
    st.markdown("""
        <div class="hero-banner">
            <div class="hero-title">🏥 Swasthya Sahay: Public Health Grievance System</div>
            <div class="hero-subtitle">Empowering rural citizens across Karnataka with zero-smartphone voice & SMS grievance redressal.<br>ಕನ್ನಡ ಮತ್ತು ಇಂಗ್ಲಿಷ್‌ನಲ್ಲಿ ಸಾರ್ವಜನಿಕ ಆಸ್ಪತ್ರೆ ದೂರು ವ್ಯವಸ್ಥೆ</div>
        </div>
    """, unsafe_allow_html=True)

    tab_call, tab_sms, tab_kiosk, tab_track = st.tabs([
        "📞 Voice Call (IVR) / ಧ್ವನಿ ಕರೆ", 
        "📱 SMS Gateway / ಎಸ್‌ಎಂಎಸ್", 
        "🏥 Kiosk Helpdesk / ಸಹಾಯ ಕೇಂದ್ರ", 
        "🔍 Track Status / ದೂರಿನ ಸ್ಥಿತಿ"
    ])

    with tab_call:
        st.image("https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=1200&q=80", use_container_width=True)
        st.markdown("### 🎙️ Interactive Voice Response (IVR) / ಧ್ವನಿ ಕರೆ ಮೂಲಕ ದೂರು ನೀಡಿ")
        
        col1, col2 = st.columns(2)
        with col1:
            selected_district = st.selectbox("Select District / ಜಿಲ್ಲೆ", sorted(list(HOSPITAL_DATABASE.keys())), key="c_dist")
            available_talukas = sorted(list(HOSPITAL_DATABASE[selected_district].keys()))
            selected_taluka = st.selectbox("Select Taluka / ತಾಲೂಕು", available_talukas, key="c_tal")
        with col2:
            available_hospitals = HOSPITAL_DATABASE[selected_district][selected_taluka]
            selected_hospital = st.selectbox("Select Government Hospital / ಆಸ್ಪತ್ರೆ", available_hospitals, key="c_hosp")
            call_lang = st.selectbox("Language Spoken / ಭಾಷೆ", ["Kannada (ಕನ್ನಡ)", "Hindi (हिन्दी)", "English"], key="c_lang")
        
        with st.form("call_form"):
            voice_transcript = st.text_area("Voice Grievance Message / ಧ್ವನಿ ಸಂದೇಶ (ಮಾತನಾಡಿ ಅಥವಾ ಟೈಪ್ ಮಾಡಿ):", placeholder="ಉದಾಹರಣೆಗೆ: ಆಸ್ಪತ್ರೆಯಲ್ಲಿ ವೈದ್ಯರು ಲಭ್ಯವಿಲ್ಲ / Doctors not available...")
            submitted_call = st.form_submit_button("Submit Voice Grievance / ದೂರು ಸಲ್ಲಿಸಿ", use_container_width=True)
            
            if submitted_call and voice_transcript.strip():
                df = load_data()
                cid = f"HOSP-CALL-{datetime.datetime.now().strftime('%Y%m%d')}-{random.randint(100, 999)}"
                
                cat = "General Facilities / ಮೂಲಭೂತ ಸೌಕರ್ಯ"
                txt = voice_transcript.lower()
                if any(w in txt for w in ["doctor", "ವೈದ್ಯ", "staff", "ಡಾಕ್ಟರ್"]):
                    cat = "Doctors & Staff / ವೈದ್ಯರು ಮತ್ತು ಸಿಬ್ಬಂದಿ"
                elif any(w in txt for w in ["medicine", "tablet", "ಔಷಧಿ", "ಮಾತ್ರೆ"]):
                    cat = "Medicine Shortage / ಔಷಧಗಳ ಕೊರತೆ"

                new_row = pd.DataFrame([{
                    "Complaint ID": cid,
                    "Intake Channel": "Voice Call (IVR)",
                    "District": selected_district,
                    "Taluka": selected_taluka,
                    "Hospital": selected_hospital,
                    "Department / Category": cat,
                    "Language": call_lang,
                    "Voice / Text Transcript": voice_transcript,
                    "Status": "Pending",
                    "Doctor Action / Official Response": "No action taken yet / ಇನ್ನೂ ಯಾವುದೇ ಕ್ರಮ ಕೈಗೊಂಡಿಲ್ಲ",
                    "Patient Rating": "Not Rated",
                    "Escalation Status": "Normal",
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }])
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.success(f"🎉 Grievance registered successfully! Unique Ticket ID: **{cid}**")

    with tab_sms:
        st.image("https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=1200&q=80", use_container_width=True)
        st.markdown("### 📱 SMS / Feature Phone Gateway")
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            sms_district = st.selectbox("Select District / ಜಿಲ್ಲೆ", sorted(list(HOSPITAL_DATABASE.keys())), key="s_dist")
            sms_taluka = st.selectbox("Select Taluka / ತಾಲೂಕು", sorted(list(HOSPITAL_DATABASE[sms_district].keys())), key="s_tal")
        with col_s2:
            sms_hosp = st.selectbox("Select Hospital / ಆಸ್ಪತ್ರೆ", HOSPITAL_DATABASE[sms_district][sms_taluka], key="s_hosp")
        
        with st.form("sms_form"):
            sms_body = st.text_area("SMS Text Message / ಎಸ್‌ಎಂಎಸ್ ಸಂದೇಶ", placeholder="MEDICINE SHORTAGE IN WARD...")
            submitted_sms = st.form_submit_button("Send SMS Grievance / ಎಸ್‌ಎಂಎಸ್ ಕಳುಹಿಸಿ", use_container_width=True)
            
            if submitted_sms and sms_body.strip():
                df = load_data()
                cid = f"HOSP-SMS-{datetime.datetime.now().strftime('%Y%m%d')}-{random.randint(100, 999)}"
                new_row = pd.DataFrame([{
                    "Complaint ID": cid,
                    "Intake Channel": "SMS / Feature Phone",
                    "District": sms_district,
                    "Taluka": sms_taluka,
                    "Hospital": sms_hosp,
                    "Department / Category": "Medicine / ಔಷಧಗಳು",
                    "Language": "Regional Code",
                    "Voice / Text Transcript": sms_body,
                    "Status": "Pending",
                    "Doctor Action / Official Response": "No action taken yet",
                    "Patient Rating": "Not Rated",
                    "Escalation Status": "Normal",
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }])
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.success(f"🎉 Grievance logged! Ticket ID: **{cid}**")

    with tab_track:
        st.markdown("### 🔍 Track Status & Escalate / ದೂರಿನ ಸ್ಥಿತಿ ಪರಿಶೀಲನೆ ಮತ್ತು ಮೇಲ್ಮನವಿ")
        search_id = st.text_input("Enter Complaint Ticket ID / ನಿಮ್ಮ ದೂರು ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ:")
        
        if st.button("Search Ticket / ದೂರು ಹುಡುಕಿ", use_container_width=True):
            df = load_data()
            if not df.empty:
                result = df[df["Complaint ID"] == search_id.strip()]
                if not result.empty:
                    st.dataframe(result[["Complaint ID", "Hospital", "Voice / Text Transcript", "Status", "Doctor Action / Official Response", "Escalation Status"]], use_container_width=True)
                    
                    status = result["Status"].values[0]
                    escalation = result["Escalation Status"].values[0]
                    
                    if status == "Pending":
                        st.warning("⚠️ **Notice:** Hospital staff have **not taken any action yet** / ಆಸ್ಪತ್ರೆ ಸಿಬ್ಬಂದಿ ಇನ್ನೂ ಯಾವುದೇ ಕ್ರಮ ಕೈಗೊಂಡಿಲ್ಲ.")
                        
                        if escalation == "Normal":
                            if st.button("🚨 Escalate to District Medical Officer (DMO) / ಜಿಲ್ಲಾ ಆರೋಗ್ಯಾಧಿಕಾರಿಗಳಿಗೆ ಮೇಲ್ಮನವಿ ಸಲ್ಲಿಸಿ", use_container_width=True):
                                df.loc[df["Complaint ID"] == search_id.strip(), "Escalation Status"] = "ESCALATED TO DMO ⚠️"
                                df.to_csv(DATA_FILE, index=False)
                                st.error("Complaint escalated to DMO due to lack of staff action!")
                                st.rerun()
                        else:
                            st.error("🚨 Complaint is Escalated to DMO / ಈ ದೂರು ಈಗಾಗಲೇ ಜಿಲ್ಲಾ ಆರೋಗ್ಯಾಧಿಕಾರಿಗಳ ಬಳಿ ಇದೆ.")
                            
                    elif status == "Resolved":
                        st.success("✅ This complaint has been resolved by hospital staff.")
                        rating = st.slider("Rate Hospital Action (1 to 5 Stars) / ಸೇವೆಯ ರೇಟಿಂಗ್ ನೀಡಿ", 1, 5, 5, key="patient_rating_slider")
                        if st.button("Submit Rating / ರೇಟಿಂಗ್ ಸಲ್ಲಿಸಿ", use_container_width=True):
                            df.loc[df["Complaint ID"] == search_id.strip(), "Patient Rating"] = f"⭐ {rating} Stars"
                            df.to_csv(DATA_FILE, index=False)
                            st.success("Thank you for your feedback!")
                            st.rerun()
                else:
                    st.error("Complaint ID not found / ದೂರು ಸಂಖ್ಯೆ ಕಂಡುಬಂದಿಲ್ಲ.")
            else:
                st.info("No records available.")

# ---------------------------------------------------------
# PORTAL 2: DOCTOR & HOSPITAL STAFF PORTAL
# ---------------------------------------------------------
elif portal_choice == "🩺 Doctor & Staff Portal / ವೈದ್ಯರ ಪೋರ್ಟಲ್":
    st.markdown("""
        <div class="hero-banner" style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);">
            <div class="hero-title">🩺 Doctor & Hospital Staff Portal</div>
            <div class="hero-subtitle">ವೈದ್ಯರು ಮತ್ತು ಸಿಬ್ಬಂದಿ ಕಾರ್ಯಾಚರಣೆ ಪೋರ್ಟಲ್</div>
        </div>
    """, unsafe_allow_html=True)
    
    df = load_data()
    staff_district = st.selectbox("Filter by District / ಜಿಲ್ಲೆಯ ಪ್ರಕಾರ ಹುಡುಕಿ", ["All Districts / ಎಲ್ಲಾ ಜಿಲ್ಲೆಗಳು"] + sorted(list(HOSPITAL_DATABASE.keys())), key="staff_dist_filter")
    if staff_district != "All Districts / ಎಲ್ಲಾ ಜಿಲ್ಲೆಗಳು":
        df_filtered = df[df["District"] == staff_district]
    else:
        df_filtered = df

    st.markdown("### 📋 Assigned Grievances List / ರೋಗಿಗಳ ದೂರುಗಳ ಪಟ್ಟಿ")
    if not df_filtered.empty:
        st.dataframe(df_filtered[["Complaint ID", "Hospital", "Department / Category", "Voice / Text Transcript", "Status", "Escalation Status"]], use_container_width=True)
        
        active_ids = df_filtered["Complaint ID"].tolist()
        if active_ids:
            st.markdown("---")
            st.markdown("### 📝 Resolve & Answer Patient Complaint")
            doc_selected_id = st.selectbox("Select Ticket ID / ದೂರು ಸಂಖ್ಯೆ ಆಯ್ಕೆ ಮಾಡಿ", active_ids, key="doc_ticket_select")
            
            curr_status = df.loc[df["Complaint ID"] == doc_selected_id, "Status"].values[0]
            if curr_status == "Pending":
                st.warning("⚠️ **Status:** No action taken yet by hospital staff.")
            
            doctor_answer = st.text_area("Official Response / ಕೈಗೊಂಡ ಕ್ರಮದ ವಿವರಣೆ:", placeholder="Describe action taken...", key="doc_answer_text")
            
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                if st.button("Mark In Progress / ಪ್ರಗತಿಯಲ್ಲಿದೆ", use_container_width=True, key="btn_in_prog"):
                    df.loc[df["Complaint ID"] == doc_selected_id, "Status"] = "In Progress"
                    df.loc[df["Complaint ID"] == doc_selected_id, "Doctor Action / Official Response"] = doctor_answer
                    df.to_csv(DATA_FILE, index=False)
                    st.success("Status updated to In Progress.")
                    st.rerun()
            with col_d2:
                if st.button("Mark Resolved & Submit Answer / ಪರಿಹರಿಸಲಾಗಿದೆ", use_container_width=True, key="btn_resolved"):
                    if doctor_answer.strip():
                        df.loc[df["Complaint ID"] == doc_selected_id, "Status"] = "Resolved"
                        df.loc[df["Complaint ID"] == doc_selected_id, "Doctor Action / Official Response"] = doctor_answer
                        df.loc[df["Complaint ID"] == doc_selected_id, "Escalation Status"] = "Resolved & Closed"
                        df.to_csv(DATA_FILE, index=False)
                        st.success("Marked as Resolved!")
                        st.rerun()
                    else:
                        st.error("Please enter official remarks before resolving.")
    else:
        st.info("No complaints found.")

# ---------------------------------------------------------
# PORTAL 3: ADMIN & AUTHORITY DASHBOARD
# ---------------------------------------------------------
else:
    st.markdown("""
        <div class="hero-banner" style="background: linear-gradient(135deg, #334155 0%, #0f172a 100%);">
            <div class="hero-title">📊 Health Authority Monitoring Dashboard</div>
            <div class="hero-subtitle">ಜಿಲ್ಲಾ ಆರೋಗ್ಯಾಧಿಕಾರಿಗಳ ಮತ್ತು ಮೇಲ್ವಿಚಾರಣಾ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್</div>
        </div>
    """, unsafe_allow_html=True)
    
    df = load_data()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Grievances", len(df))
    with col2:
        st.metric("Pending / No Action", len(df[df["Status"] == "Pending"]))
    with col3:
        st.metric("Escalated to DMO", len(df[df["Escalation Status"] == "ESCALATED TO DMO ⚠️"]))
    with col4:
        st.metric("Resolved", len(df[df["Status"] == "Resolved"]))

    st.markdown("---")
    st.markdown("### ⚠️ Escalated Complaints (Inaction Alerts)")
    escalated_df = df[df["Escalation Status"] == "ESCALATEDTO DMO ⚠️" if "ESCALATEDTO DMO ⚠️" in df.columns else df["Escalation Status"] == "ESCALATED TO DMO ⚠️"]
    if not escalated_df.empty:
        st.dataframe(escalated_df, use_container_width=True)
    else:
        st.info("No escalated complaints due to staff inaction.")

    st.markdown("---")
    st.markdown("### 📋 Master Registry Across All Districts")
    if not df.empty:
        st.dataframe(df, use_container_width=True)
