import streamlit as st
import pandas as pd
import os
import datetime
import random

st.set_page_config(
    page_title="Accessible Voice & Kiosk Public Grievance System",
    page_icon="🏥",
    layout="wide"
)

DATA_FILE = "complaints.csv"

# Comprehensive Database of All Districts, Talukas & Government Hospitals in Karnataka
HOSPITAL_DATABASE = {
    "Bagalkot": {
        "Bagalkot": ["District Hospital Bagalkot", "General Hospital Bagalkot"],
        "Badami": ["Taluk Hospital Badami"],
        "Hungund": ["Taluk Hospital Hungund"],
        "Jamkhandi": ["Taluk Hospital Jamkhandi"],
        "Mudhol": ["Taluk Hospital Mudhol"],
        "Bilagi": ["Taluk Hospital Bilagi"],
        "Rabkavi Banhatti": ["Community Health Centre Rabkavi"]
    },
    "Ballari (Bellary)": {
        "Ballari": ["VIMS Hospital Ballari", "District Hospital Ballari"],
        "Hospet (Vijayanagara)": ["Taluk Hospital Hospet"],
        "Sandur": ["Taluk Hospital Sandur"],
        "Siruguppa": ["Taluk Hospital Siruguppa"],
        "Kudligi": ["Taluk Hospital Kudligi"]
    },
    "Belagavi (Belgaum)": {
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
    "Bengaluru Rural": {
        "Devanahalli": ["Taluk General Hospital Devanahalli"],
        "Doddaballapura": ["Government Hospital Doddaballapura"],
        "Nelamangala": ["Taluk Hospital Nelamangala"],
        "Hoskote": ["General Hospital Hoskote"]
    },
    "Bengaluru Urban": {
        "Bengaluru North": ["Bowring & Lady Curzon Hospital", "KC General Hospital Malleshwaram"],
        "Bengaluru South": ["Victoria Hospital Fort", "Vanivilas Women and Children Hospital"],
        "Bengaluru East": ["General Hospital Jayanagar", "C.V. Raman General Hospital"],
        "Anekal": ["Taluk Hospital Anekal"]
    },
    "Bidar": {
        "Bidar": ["District Hospital Bidar", "BRIMS Teaching Hospital"],
        "Bhalki": ["Taluk Hospital Bhalki"],
        "Basavakalyan": ["Taluk Hospital Basavakalyan"],
        "Humnabad": ["Taluk Hospital Humnabad"],
        "Aurad": ["Taluk Hospital Aurad"]
    },
    "Chamarajanagar": {
        "Chamarajanagar": ["District Hospital Chamarajanagar"],
        "Kollegal": ["Sub-Divisional Hospital Kollegal"],
        "Gundlupet": ["Taluk Hospital Gundlupet"],
        "Yelandur": ["Community Health Centre Yelandur"]
    },
    "Chikkaballapura": {
        "Chikkaballapura": ["District Hospital Chikkaballapura"],
        "Bagepalli": ["Taluk Hospital Bagepalli"],
        "Chintamani": ["Taluk Hospital Chintamani"],
        "Gauribidanur": ["Taluk Hospital Gauribidanur"],
        "Sidlaghatta": ["Taluk Hospital Sidlaghatta"]
    },
    "Chikkamagaluru": {
        "Chikkamagaluru": ["District Hospital Chikkamagaluru"],
        "Kadur": ["Taluk Hospital Kadur"],
        "Koppa": ["Taluk Hospital Koppa"],
        "Mudigere": ["Taluk Hospital Mudigere"],
        "Narasimharajapura": ["Taluk Hospital NR Pura"],
        "Sringeri": ["Taluk Hospital Sringeri"],
        "Tarikere": ["Taluk Hospital Tarikere"]
    },
    "Chitradurga": {
        "Chitradurga": ["District Hospital Chitradurga"],
        "Challakere": ["Taluk Hospital Challakere"],
        "Hiriyur": ["Taluk Hospital Hiriyur"],
        "Hosadurga": ["Taluk Hospital Hosadurga"],
        "Molakalmuru": ["Taluk Hospital Molakalmuru"]
    },
    "Dakshina Kannada": {
        "Mangaluru": ["Government Lady Goschen Hospital", "Wenlock District Hospital Mangaluru"],
        "Bantwal": ["Taluk Hospital Bantwal"],
        "Puttur": ["Government Hospital Puttur"],
        "Belthangady": ["Taluk Hospital Belthangady"],
        "Sullia": ["Taluk Hospital Sullia"]
    },
    "Davanagere": {
        "Davanagere": ["Chigateri District Hospital", "McGann Teaching Hospital"],
        "Harihar": ["Taluk Hospital Harihar"],
        "Honnali": ["Taluk Hospital Honnali"],
        "Nyamati": ["Community Health Centre Nyamati"],
        "Jagalur": ["Taluk Hospital Jagalur"]
    },
    "Dharwad": {
        "Dharwad": ["District Hospital Dharwad", "KIMS Hospital Dharwad"],
        "Hubballi": ["Karnataka Institute of Medical Sciences (KIMS)", "Civil Hospital Hubballi"],
        "Navalgund": ["Taluk Hospital Navalgund"],
        "Kundgol": ["Taluk Hospital Kundgol"],
        "Alnavar": ["Community Health Centre Alnavar"]
    },
    "Gadag": {
        "Gadag": ["GIMS Teaching Hospital Gadag", "District Hospital Gadag"],
        "Ron": ["Taluk Hospital Ron"],
        "Shirhatti": ["Taluk Hospital Shirhatti"],
        "Mundargi": ["Taluk Hospital Mundargi"],
        "Nargund": ["Taluk Hospital Nargund"]
    },
    "Hassan": {
        "Hassan": ["HIMS Teaching Hospital", "District Hospital Hassan"],
        "Arsikere": ["Taluk Hospital Arsikere"],
        "Channarayapatna": ["Taluk Hospital Channarayapatna"],
        "Holenarasipura": ["Taluk Hospital Holenarasipura"],
        "Sakleshpur": ["Taluk Hospital Sakleshpur"],
        "Belur": ["Taluk Hospital Belur"],
        "Alur": ["Community Health Centre Alur"]
    },
    "Haveri": {
        "Haveri": ["District Hospital Haveri"],
        "Ranebennur": ["Taluk Hospital Ranebennur"],
        "Byadgi": ["Taluk Hospital Byadgi"],
        "Hirekerur": ["Taluk Hospital Hirekerur"],
        "Shiggav": ["Taluk Hospital Shiggaon"],
        "Savanur": ["Taluk Hospital Savanur"]
    },
    "Kalaburagi (Gulbarga)": {
        "Kalaburagi": ["District Government Hospital Kalaburagi", "Super Speciality Hospital Kalaburagi", "ESIC Medical College & Hospital"],
        "Aland": ["Community Health Centre Aland", "Taluk General Hospital Aland"],
        "Afzalpur": ["Taluk Hospital Afzalpur", "CHC Dudhani"],
        "Chincholi": ["Taluk Hospital Chincholi"],
        "Jevargi": ["Taluk Hospital Jevargi"],
        "Sedam": ["Taluk Hospital Sedam"],
        "Yadrami": ["Community Health Centre Yadrami"]
    },
    "Kodagu": {
        "Madikeri": ["District Hospital Madikeri"],
        "Virajpet": ["Taluk General Hospital Virajpet"],
        "Somwarpet": ["Taluk Hospital Somwarpet"]
    },
    "Kolar": {
        "Kolar": ["District Hospital Kolar", "RL Jalappa Hospital"],
        "Bangarapet": ["Taluk Hospital Bangarapet"],
        "Malur": ["Taluk Hospital Malur"],
        "Mulbagal": ["Taluk Hospital Mulbagal"],
        "Srinivaspur": ["Taluk Hospital Srinivaspur"]
    },
    "Koppal": {
        "Koppal": ["District Hospital Koppal", "KIMS Koppal"],
        "Gangavathi": ["Taluk Hospital Gangavathi"],
        "Yelburga": ["Taluk Hospital Yelburga"],
        "Kushtagi": ["Taluk Hospital Kushtagi"]
    },
    "Mandya": {
        "Mandya": ["Mandya Institute of Medical Sciences (MIMS)", "District Hospital Mandya"],
        "Maddur": ["Taluk Hospital Maddur"],
        "Malavalli": ["Taluk Hospital Malavalli"],
        "Srirangapatna": ["Taluk Hospital Srirangapatna"],
        "Pandavapura": ["Taluk Hospital Pandavapura"],
        "Nagamangala": ["Taluk Hospital Nagamangala"],
        "Krishnarajapet": ["Taluk Hospital KR Pet"]
    },
    "Mysuru (Mysore)": {
        "Mysuru": ["K.R. Hospital Mysuru", "Cheluvamba Hospital", "District Hospital Mysuru"],
        "Nanjangud": ["Taluk General Hospital Nanjangud"],
        "Hunsur": ["Taluk Hospital Hunsur"],
        "K.R. Nagar": ["Taluk Hospital KR Nagar"],
        "Periyapatna": ["Taluk Hospital Periyapatna"],
        "T. Narasipura": ["Taluk Hospital T. Narasipura"],
        "Heggadadevankote (H.D. Kote)": ["Taluk Hospital HD Kote"]
    },
    "Raichur": {
        "Raichur": ["RIMS Teaching Hospital", "District Hospital Raichur"],
        "Manvi": ["Taluk Hospital Manvi"],
        "Sindhanur": ["Taluk Hospital Sindhanur"],
        "Devadurga": ["Taluk Hospital Devadurga"],
        "Maski": ["Community Health Centre Maski"]
    },
    "Ramanagara": {
        "Ramanagara": ["District Hospital Ramanagara"],
        "Channapatna": ["Taluk Hospital Channapatna"],
        "Kanakapura": ["Taluk Hospital Kanakapura"],
        "Magadi": ["Taluk Hospital Magadi"]
    },
    "Shivamogga (Shimoga)": {
        "Shivamogga": ["McGann District Hospital", "SIMS Teaching Hospital"],
        "Bhadravathi": ["Taluk Hospital Bhadravathi"],
        "Sagara": ["Sub-Divisional Hospital Sagara"],
        "Shikaripura": ["Taluk Hospital Shikaripura"],
        "Sorab": ["Taluk Hospital Sorab"],
        "Tirthahalli": ["Taluk Hospital Tirthahalli"],
        "Hosanagara": ["Taluk Hospital Hosanagara"]
    },
    "Tumakuru (Tumkur)": {
        "Tumakuru": ["District Hospital Tumakuru", "TSIIMS Hospital"],
        "Madhugiri": ["Sub-Divisional Hospital Madhugiri"],
        "Tiptur": ["Taluk Hospital Tiptur"],
        "Sira": ["Taluk Hospital Sira"],
        "Gubbi": ["Taluk Hospital Gubbi"],
        "Kunigal": ["Taluk Hospital Kunigal"],
        "Koratagere": ["Taluk Hospital Koratagere"],
        "Pavagada": ["Taluk Hospital Pavagada"],
        "Chorayakanahalli": ["CHC C.N. Halli"]
    },
    "Udupi": {
        "Udupi": ["District Hospital Udupi"],
        "Kundapura": ["Government Hospital Kundapura"],
        "Karkala": ["Taluk Hospital Karkala"]
    },
    "Uttara Kannada (Karwar)": {
        "Karwar": ["District Hospital Karwar"],
        "Sirsi": ["Sub-Divisional Hospital Sirsi"],
        "Kumta": ["Taluk Hospital Kumta"],
        "Bhatkal": ["Taluk Hospital Bhatkal"],
        "Haliyal": ["Taluk Hospital Haliyal"],
        "Yellapur": ["Taluk Hospital Yellapur"],
        "Ankola": ["Taluk Hospital Ankola"]
    },
    "Vijayapura (Bijapur)": {
        "Vijayapura": ["District Hospital Vijayapura", "BLDE Teaching Hospital"],
        "Basavana Bagevadi": ["Taluk Hospital Basavana Bagevadi"],
        "Indi": ["Taluk Hospital Indi"],
        "Muddebihal": ["Taluk Hospital Muddebihal"],
        "Sindagi": ["Taluk Hospital Sindagi"]
    },
    "Yadgir": {
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

st.sidebar.title("🏥 Solvathon 2026 Navigation")
portal_choice = st.sidebar.radio(
    "Select Portal", 
    [
        "🗣️ Citizen Intake & Patient Tracking", 
        "🩺 Doctor & Hospital Staff Portal", 
        "📊 Admin & Authority Dashboard"
    ]
)

# ---------------------------------------------------------
# PORTAL 1: CITIZEN INTAKE & PATIENT TRACKING
# ---------------------------------------------------------
if portal_choice == "🗣️ Citizen Intake & Patient Tracking":
    st.title("🗣️ Accessible Public Grievance System")
    st.write("For rural patients and citizens across Karnataka to lodge complaints and track doctor responses.")

    tab_call, tab_sms, tab_kiosk, tab_track = st.tabs([
        "📞 Live Audio Call / IVR", 
        "📱 SMS Gateway", 
        "🏥 Hospital Helpdesk Kiosk", 
        "🔍 Track Status & Escalate"
    ])

    with tab_call:
        st.subheader("Interactive Voice Response (IVR) & Call Portal")
        with st.form("call_form"):
            selected_district = st.selectbox("Select District", sorted(list(HOSPITAL_DATABASE.keys())))
            available_talukas = sorted(list(HOSPITAL_DATABASE[selected_district].keys()))
            selected_taluka = st.selectbox("Select Taluka", available_talukas)
            available_hospitals = HOSPITAL_DATABASE[selected_district][selected_taluka]
            selected_hospital = st.selectbox("Select Government Hospital", available_hospitals)
            
            call_lang = st.selectbox("Select Language", ["Kannada (ಕನ್ನಡ)", "Hindi (हिन्दी)", "English"])
            voice_transcript = st.text_area("Voice Call Transcript:", placeholder="ಉದಾಹರಣೆಗೆ: ಆಸ್ಪತ್ರೆಯಲ್ಲಿ ವೈದ್ಯರು ಲಭ್ಯವಿಲ್ಲ...")

            submitted_call = st.form_submit_button("Submit Voice Grievance")
            
            if submitted_call and voice_transcript.strip():
                df = load_data()
                cid = f"HOSP-CALL-{datetime.datetime.now().strftime('%Y%m%d')}-{random.randint(100, 999)}"
                
                cat = "General Facilities"
                txt = voice_transcript.lower()
                if "doctor" in txt or "ವೈದ್ಯ" in txt or "staff" in txt:
                    cat = "Doctors & Staff Availability"
                elif "medicine" in txt or "tablet" in txt or "ಔಷಧಿ" in txt:
                    cat = "Medicine Availability"

                new_row = pd.DataFrame([{
                    "Complaint ID": cid,
                    "Intake Channel": "Voice Call / IVR",
                    "District": selected_district,
                    "Taluka": selected_taluka,
                    "Hospital": selected_hospital,
                    "Department / Category": cat,
                    "Language": call_lang,
                    "Voice / Text Transcript": voice_transcript,
                    "Status": "Pending",
                    "Doctor Action / Official Response": "No action taken yet",
                    "Patient Rating": "Not Rated",
                    "Escalation Status": "Normal",
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }])
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.success(f"Grievance successfully registered! Unique Ticket ID: **{cid}**")

    with tab_sms:
        st.subheader("SMS / Feature Phone Gateway")
        with st.form("sms_form"):
            sms_district = st.selectbox("Select District", sorted(list(HOSPITAL_DATABASE.keys())), key="sms_dist")
            sms_taluka = st.selectbox("Select Taluka", sorted(list(HOSPITAL_DATABASE[sms_district].keys())), key="sms_tal")
            sms_hosp = st.selectbox("Select Hospital", HOSPITAL_DATABASE[sms_district][sms_taluka], key="sms_hosp")
            sms_body = st.text_area("SMS Text Message", placeholder="MEDICINE SHORTAGE IN EMERGENCY WARD")
            
            submitted_sms = st.form_submit_button("Send SMS Grievance")
            if submitted_sms and sms_body.strip():
                df = load_data()
                cid = f"HOSP-SMS-{datetime.datetime.now().strftime('%Y%m%d')}-{random.randint(100, 999)}"
                new_row = pd.DataFrame([{
                    "Complaint ID": cid,
                    "Intake Channel": "SMS / Feature Phone",
                    "District": sms_district,
                    "Taluka": sms_taluka,
                    "Hospital": sms_hosp,
                    "Department / Category": "Medicine Availability",
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
                st.success(f"SMS registered successfully! Ticket ID: **{cid}**")

    with tab_kiosk:
        st.subheader("Assisted Hospital Helpdesk Kiosk")
        with st.form("kiosk_form"):
            k_district = st.selectbox("Select District", sorted(list(HOSPITAL_DATABASE.keys())), key="k_dist")
            k_taluka = st.selectbox("Select Taluka", sorted(list(HOSPITAL_DATABASE[k_district].keys())), key="k_tal")
            k_hosp = st.selectbox("Select Hospital", HOSPITAL_DATABASE[k_district][k_taluka], key="k_hosp")
            kiosk_desc = st.text_area("Issue Description", placeholder="Describe cleanliness or staff shortage...")
            
            submitted_kiosk = st.form_submit_button("Log Assisted Grievance")
            if submitted_kiosk and kiosk_desc.strip():
                df = load_data()
                cid = f"HOSP-KIOSK-{datetime.datetime.now().strftime('%Y%m%d')}-{random.randint(100, 999)}"
                new_row = pd.DataFrame([{
                    "Complaint ID": cid,
                    "Intake Channel": "Hospital Helpdesk Kiosk",
                    "District": k_district,
                    "Taluka": k_taluka,
                    "Hospital": k_hosp,
                    "Department / Category": "General Facilities",
                    "Language": "Assisted Entry",
                    "Voice / Text Transcript": kiosk_desc,
                    "Status": "Pending",
                    "Doctor Action / Official Response": "No action taken yet",
                    "Patient Rating": "Not Rated",
                    "Escalation Status": "Normal",
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }])
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.success(f"Helpdesk grievance logged! Ticket ID: **{cid}**")

    with tab_track:
        st.subheader("Track Status, Check Inaction & Escalate")
        search_id = st.text_input("Enter Unique Complaint ID (e.g., HOSP-CALL-...):")
        
        if st.button("Search Ticket"):
            df = load_data()
            if not df.empty:
                result = df[df["Complaint ID"] == search_id.strip()]
                if not result.empty:
                    st.dataframe(result[["Complaint ID", "Hospital", "Voice / Text Transcript", "Status", "Doctor Action / Official Response", "Escalation Status"]])
                    
                    status = result["Status"].values[0]
                    escalation = result["Escalation Status"].values[0]
                    
                    if status == "Pending":
                        st.warning("⚠️ Notice: Hospital staff have not taken any action yet on this complaint.")
                        
                        if escalation == "Normal":
                            if st.button("🚨 Escalate to District Medical Officer (No Action Taken)"):
                                df.loc[df["Complaint ID"] == search_id.strip(), "Escalation Status"] = "ESCALATED TO DMO ⚠️"
                                df.to_csv(DATA_FILE, index=False)
                                st.error("Complaint has been escalated to district health authorities due to lack of action!")
                                st.rerun()
                        else:
                            st.error("🚨 This complaint is currently Escalated to higher authorities due to delayed staff response.")
       
