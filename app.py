import streamlit as st
import pandas as pd
import os
import datetime
import random

st.set_page_config(
    page_title="Accessible Grievance System / ಧ್ವನಿ ಆಧಾರಿತ ದೂರು ವ್ಯವಸ್ಥೆ",
    page_icon="🏥",
    layout="wide"
)

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

st.sidebar.title("🏥 Solvathon 2026 Navigation / ಆಯ್ಕೆಗಳು")
portal_choice = st.sidebar.radio(
    "Select Portal / ವಿಭಾಗವನ್ನು ಆಯ್ಕೆ ಮಾಡಿ", 
    [
        "🗣️ Citizen Intake & Tracking / ದೂರು ಸಲ್ಲಿಕೆ ಮತ್ತು ಪರಿಶೀಲನೆ", 
        "🩺 Doctor & Staff Portal / ವೈದ್ಯರು ಮತ್ತು ಸಿಬ್ಬಂದಿ ಪೋರ್ಟಲ್", 
        "📊 Admin Dashboard / ಮೇಲಾಧಿಕಾರಿಗಳ ಡ್ಯಾಶ್‌ಬೋರ್ಡ್"
    ]
)

# ---------------------------------------------------------
# PORTAL 1: CITIZEN INTAKE & PATIENT TRACKING
# ---------------------------------------------------------
if portal_choice == "🗣️ Citizen Intake & Tracking / ದೂರು ಸಲ್ಲಿಕೆ ಮತ್ತು ಪರಿಶೀಲನೆ":
    st.title("🗣️ Accessible Grievance System / ಸಾರ್ವಜನಿಕ ಆಸ್ಪತ್ರೆ ದೂರು ವ್ಯವಸ್ಥೆ")
    st.write("For rural patients and citizens across Karnataka / ಕರ್ನಾಟಕದ ಸಾರ್ವಜನಿಕರು ಮತ್ತು ಗ್ರಾಮೀಣ ರೋಗಿಗಳಿಗೆ")

    tab_call, tab_sms, tab_kiosk, tab_track = st.tabs([
        "📞 Voice Call (IVR) / ಧ್ವನಿ ಕರೆ ದೂರು", 
        "📱 SMS Gateway / ಎಸ್‌ಎಂಎಸ್ ದೂರು", 
        "🏥 Helpdesk Kiosk / ಆಸ್ಪತ್ರೆ ಸಹಾಯ ಕೇಂದ್ರ", 
        "🔍 Track Status & Escalate / ದೂರಿನ ಸ್ಥಿತಿ ಪರಿಶೀಲನೆ"
    ])

    with tab_call:
        st.subheader("Interactive Voice Call Portal / ಧ್ವನಿ ಕರೆ ಮೂಲಕ ದೂರು ನೀಡಿ")
        
        selected_district = st.selectbox("Select District / ಜಿಲ್ಲೆಯನ್ನು ಆಯ್ಕೆ ಮಾಡಿ", sorted(list(HOSPITAL_DATABASE.keys())), key="call_dist")
        available_talukas = sorted(list(HOSPITAL_DATABASE[selected_district].keys()))
        selected_taluka = st.selectbox("Select Taluka / ತಾಲೂಕನ್ನು ಆಯ್ಕೆ ಮಾಡಿ", available_talukas, key="call_tal")
        available_hospitals = HOSPITAL_DATABASE[selected_district][selected_taluka]
        selected_hospital = st.selectbox("Select Government Hospital / ಆಸ್ಪತ್ರೆಯನ್ನು ಆಯ್ಕೆ ಮಾಡಿ", available_hospitals, key="call_hosp")
        
        with st.form("call_form"):
            call_lang = st.selectbox("Language Spoken / ಭಾಷೆ", ["Kannada (ಕನ್ನಡ)", "Hindi (ಹಿन्दी)", "English"])
            voice_transcript = st.text_area("Voice Grievance Message / ಧ್ವನಿ ಸಂದೇಶ:", placeholder="ಆಸ್ಪತ್ರೆಯಲ್ಲಿ ವೈದ್ಯರು ಲಭ್ಯವಿಲ್ಲ...")

            submitted_call = st.form_submit_button("Submit Voice Grievance / ದೂರು ಸಲ್ಲಿಸಿ")
            
            if submitted_call and voice_transcript.strip():
                df = load_data()
                cid = f"HOSP-CALL-{datetime.datetime.now().strftime('%Y%m%d')}-{random.randint(100, 999)}"
                
                cat = "General Facilities / ಮೂಲಭೂತ ಸೌಕರ್ಯ"
                txt = voice_transcript.lower()
                if "doctor" in txt or "ವೈದ್ಯ" in txt or "staff" in txt or "ಡಾಕ್ಟರ್" in txt:
                    cat = "Doctors & Staff / ವೈದ್ಯರು ಮತ್ತು ಸಿಬ್ಬಂದಿ"
                elif "medicine" in txt or "tablet" in txt or "ಔಷಧಿ" in txt or "ಮಾತ್ರೆ" in txt:
                    cat = "Medicine Shortage / ಔಷಧಗಳ ಕೊರತೆ"

                new_row = pd.DataFrame([{
                    "Complaint ID": cid,
                    "Intake Channel": "Voice Call (IVR) / ಧ್ವನಿ ಕರೆ",
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
                st.success(f"Grievance successfully registered / ದೂರು ಯಶಸ್ವಿಯಾಗಿ ದಾಖಲಾಗಿದೆ! Ticket ID: **{cid}**")

    with tab_sms:
        st.subheader("SMS Gateway / ಎಸ್‌ಎಂಎಸ್ ಮೂಲಕ ದೂರು")
        sms_district = st.selectbox("Select District / ಜಿಲ್ಲೆಯನ್ನು ಆಯ್ಕೆ ಮಾಡಿ", sorted(list(HOSPITAL_DATABASE.keys())), key="sms_dist")
        sms_taluka = st.selectbox("Select Taluka / ತಾಲೂಕನ್ನು ಆಯ್ಕೆ ಮಾಡಿ", sorted(list(HOSPITAL_DATABASE[sms_district].keys())), key="sms_tal")
        sms_hosp = st.selectbox("Select Hospital / ಆಸ್ಪತ್ರೆಯನ್ನು ಆಯ್ಕೆ ಮಾಡಿ", HOSPITAL_DATABASE[sms_district][sms_taluka], key="sms_hosp")
        
        with st.form("sms_form"):
            sms_body = st.text_area("SMS Text Message / ಎಸ್‌ಎಂಎಸ್ ಸಂದೇಶ", placeholder="MEDICINE SHORTAGE IN WARD...")
            submitted_sms = st.form_submit_button("Send SMS Grievance / ಎಸ್‌ಎಂಎಸ್ ಕಳುಹಿಸಿ")
            
            if submitted_sms and sms_body.strip():
                df = load_data()
                cid = f"HOSP-SMS-{datetime.datetime.now().strftime('%Y%m%d')}-{random.randint(100, 999)}"
                new_row = pd.DataFrame([{
                    "Complaint ID": cid,
                    "Intake Channel": "SMS / ಎಸ್‌ಎಂಎಸ್",
                    "District": sms_district,
                    "Taluka": sms_taluka,
                    "Hospital": sms_hosp,
                    "Department / Category": "Medicine / ಔಷಧಗಳು",
                    "Language": "Regional Code",
                    "Voice / Text Transcript": sms_body,
                    "Status": "Pending",
                    "Doctor Action / Official Response": "No action taken yet / ಇನ್ನೂ ಯಾವುದೇ ಕ್ರಮ ಕೈಗೊಂಡಿಲ್ಲ",
                    "Patient Rating": "Not Rated",
                    "Escalation Status": "Normal",
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }])
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.success(f"SMS registered / ಎಸ್‌ಎಂಎಸ್ ದಾಖಲಾಗಿದೆ! Ticket ID: **{cid}**")

    with tab_kiosk:
        st.subheader("Hospital Helpdesk Kiosk / ಆಸ್ಪತ್ರೆ ಸಹಾಯ ಕೇಂದ್ರ")
        k_district = st.selectbox("Select District / ಜಿಲ್ಲೆಯನ್ನು ಆಯ್ಕೆ ಮಾಡಿ", sorted(list(HOSPITAL_DATABASE.keys())), key="k_dist")
        k_taluka = st.selectbox("Select Taluka / ತಾಲೂಕನ್ನು ಆಯ್ಕೆ ಮಾಡಿ", sorted(list(HOSPITAL_DATABASE[k_district].keys())), key="k_tal")
        k_hosp = st.selectbox("Select Hospital / ಆಸ್ಪತ್ರೆಯನ್ನು ಆಯ್ಕೆ ಮಾಡಿ", HOSPITAL_DATABASE[k_district][k_taluka], key="k_hosp")
        
        with st.form("kiosk_form"):
            kiosk_desc = st.text_area("Issue Description / ಸಮಸ್ಯೆಯ ವಿವರಣೆ", placeholder="Describe issue...")
            submitted_kiosk = st.form_submit_button("Log Grievance / ಸಹಾಯ ಕೇಂದ್ರದಲ್ಲಿ ನಮೂದಿಸಿ")
            
            if submitted_kiosk and kiosk_desc.strip():
                df = load_data()
                cid = f"HOSP-KIOSK-{datetime.datetime.now().strftime('%Y%m%d')}-{random.randint(100, 999)}"
                new_row = pd.DataFrame([{
                    "Complaint ID": cid,
                    "Intake Channel": "Helpdesk Kiosk / ಸಹಾಯ ಕೇಂದ್ರ",
                    "District": k_district,
                    "Taluka": k_taluka,
                    "Hospital": k_hosp,
                    "Department / Category": "General / ಮೂಲಭೂತ ಸೌಕರ್ಯ",
                    "Language": "Assisted Entry",
                    "Voice / Text Transcript": kiosk_desc,
                    "Status": "Pending",
                    "Doctor Action / Official Response": "No action taken yet / ಇನ್ನೂ ಯಾವುದೇ ಕ್ರಮ ಕೈಗೊಂಡಿಲ್ಲ",
                    "Patient Rating": "Not Rated",
                    "Escalation Status": "Normal",
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }])
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.success(f"Grievance logged / ದೂರು ನಮೂದಿಸಲಾಗಿದೆ! Ticket ID: **{cid}**")

    with tab_track:
        st.subheader("Track Status & Escalate / ದೂರಿನ ಸ್ಥಿತಿ ಪರಿಶೀಲನೆ ಮತ್ತು ಮೇಲ್ಮನವಿ")
        search_id = st.text_input("Enter Complaint ID / ನಿಮ್ಮ ದೂರು ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ:")
        
        if st.button("Search Ticket / ದೂರು ಹುಡುಕಿ"):
            df = load_data()
            if not df.empty:
                result = df[df["Complaint ID"] == search_id.strip()]
                if not result.empty:
                    st.dataframe(result[["Complaint ID", "Hospital", "Voice / Text Transcript", "Status", "Doctor Action / Official Response", "Escalation Status"]])
                    
                    status = result["Status"].values[0]
                    escalation = result["Escalation Status"].values[0]
                    
                    if status == "Pending":
                        st.warning("⚠️ Notice: Hospital staff have not taken any action yet / ಆಸ್ಪತ್ರೆ ಸಿಬ್ಬಂದಿ ಇನ್ನೂ ಯಾವುದೇ ಕ್ರಮ ಕೈಗೊಂಡಿಲ್ಲ.")
                        
                        if escalation == "Normal":
                            if st.button("🚨 Escalate to District Medical Officer (DMO) / ಜಿಲ್ಲಾ ಆರೋಗ್ಯಾಧಿಕಾರಿಗಳಿಗೆ ಮೇಲ್ಮನವಿ ಸಲ್ಲಿಸಿ"):
                                df.loc[df["Complaint ID"] == search_id.strip(), "Escalation Status"] = "ESCALATED TO DMO ⚠️"
                                df.to_csv(DATA_FILE, index=False)
                                st.error("Complaint escalated to DMO due to lack of staff action!")
                                st.rerun()
                        else:
                            st.error("🚨 Complaint is Escalated to DMO / ಈ ದೂರು ಈಗಾಗಲೇ ಜಿಲ್ಲಾ ಆರೋಗ್ಯಾಧಿಕಾರಿಗಳ ಬಳಿ ಇದೆ.")
                            
                    elif status == "Resolved":
                        st.success("✅ This complaint has been resolved by hospital staff.")
                        rating = st.slider("Rate Hospital Action (1 to 5 Stars) / ಸೇವೆಯ ರೇಟಿಂಗ್ ನೀಡಿ", 1, 5, 5)
                        if st.button("Submit Rating / ರೇಟಿಂಗ್ ಸಲ್ಲಿಸಿ"):
                            df.loc[df["Complaint ID"] == search_id.strip(), "Patient Rating"] = f"⭐ {rating} Stars"
                            df.to_csv(DATA_FILE, index=False)
                            st.success("Thank you for your feedback!")
                            st.rerun()
                else:
                    st.error("Complaint ID not found / ದೂರು ಸಂಖ್ಯೆ ಕಂಡುಬಂದಿಲ್ಲ.")
            else:
                st.info("No records available / ಯಾವುದೇ ದಾಖಲೆಗಳಿಲ್ಲ.")

# ---------------------------------------------------------
# PORTAL 2: DOCTOR & HOSPITAL STAFF PORTAL
# ---------------------------------------------------------
elif portal_choice == "🩺 Doctor & Staff Portal / ವೈದ್ಯರು ಮತ್ತು ಸಿಬ್ಬಂದಿ ಪೋರ್ಟಲ್":
    st.title("🩺 Doctor & Hospital Staff Action Portal")
    st.write("Review grievances, take action, and respond to patients.")
    
    df = load_data()
    staff_district = st.selectbox("Filter by District / ಜಿಲ್ಲೆಯ ಪ್ರಕಾರ ಹುಡುಕಿ", ["All Districts / ಎಲ್ಲಾ ಜಿಲ್ಲೆಗಳು"] + sorted(list(HOSPITAL_DATABASE.keys())))
    if staff_district != "All Districts / ಎಲ್ಲಾ ಜಿಲ್ಲೆಗಳು":
        df_filtered = df[df["District"] == staff_district]
    else:
        df_filtered = df

    st.subheader("Patient Grievances List / ರೋಗಿಗಳ ದೂರುಗಳ ಪಟ್ಟಿ")
    if not df_filtered.empty:
        st.dataframe(df_filtered[["Complaint ID", "Hospital", "Department / Category", "Voice / Text Transcript", "Status", "Escalation Status"]])
        
        active_ids = df_filtered["Complaint ID"].tolist()
        if active_ids:
            st.markdown("---")
            st.subheader("📝 Take Action & Answer Complaint")
            doc_selected_id = st.selectbox("Select Ticket ID / ದೂರು ಸಂಖ್ಯೆ ಆಯ್ಕೆ ಮಾಡಿ", active_ids)
            
            curr_status = df.loc[df["Complaint ID"] == doc_selected_id, "Status"].values[0]
            if curr_status == "Pending":
                st.error("⚠️ Status: No action taken yet by staff.")
            
            doctor_answer = st.text_area("Official Staff Response / ಸ್ವೀಕರಿಸಿದ ಕ್ರಮದ ವಿವರಣೆ:", placeholder="Describe action taken...")
            
            col_d1, col_d2 = st.columns(2)
            if col_d1.button("Mark In Progress / ಪ್ರಗತಿಯಲ್ಲಿದೆ"):
                df.loc[df["Complaint ID"] == doc_selected_id, "Status"] = "In Progress"
                df.loc[df["Complaint ID"] == doc_selected_id, "Doctor Action / Official Response"] = doctor_answer
                df.to_csv(DATA_FILE, index=False)
                st.success("Status updated to In Progress.")
                st.rerun()
                
            if col_d2.button("Mark Resolved & Submit Answer / ಬಗೆಹರಿಸಲಾಗಿದೆ"):
                if doctor_answer.strip():
                    df.loc[df["Complaint ID"] == doc_selected_id, "Status"] = "Resolved"
                    df.loc[df["Complaint ID"] == doc_selected_id, "Doctor Action / Official Response"] = doctor_answer
                    df.loc[df["Complaint ID"] == doc_selected_id, "Escalation Status"] = "Resolved & Closed"
                    df.to_csv(DATA_FILE, index=False)
                    st.success("Marked as Resolved!")
                    st.rerun()
                else:
                    st.error("Please enter action remarks before resolving.")
    else:
        st.info("No complaints found.")

# ---------------------------------------------------------
# PORTAL 3: ADMIN & AUTHORITY DASHBOARD
# ---------------------------------------------------------
else:
    st.title("📊 Health Authority Monitoring Dashboard")
    df = load_data()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Grievances", len(df))
    col2.metric("Pending / No Action", len(df[df["Status"] == "Pending"]))
    col3.metric("Escalated to DMO", len(df[df["Escalation Status"] == "ESCALATED TO DMO ⚠️"]))
    col4.metric("Resolved", len(df[df["Status"] == "Resolved"]))

    st.markdown("---")
    st.subheader("⚠️ Escalated Complaints (Inaction Alerts)")
    escalated_df = df[df["Escalation Status"] == "ESCALATED TO DMO ⚠️"]
    if not escalated_df.empty:
        st.dataframe(escalated_df)
    else:
        st.info("No escalated complaints.")

    st.markdown("---")
    st.subheader("Master Registry")
    if not df.empty:
        st.dataframe(df)
