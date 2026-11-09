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

# Comprehensive District, Taluka & Government Hospital Database
HOSPITAL_DATABASE = {
    "Kalaburagi": {
        "Kalaburagi (City)": [
            "District Government Hospital Kalaburagi", 
            "Super Speciality Hospital Kalaburagi", 
            "ESIC Medical College & Hospital"
        ],
        "Aland": [
            "Community Health Centre Aland", 
            "Taluk General Hospital Aland"
        ],
        "Afzalpur": [
            "Taluk Hospital Afzalpur", 
            "CHC Dudhani"
        ],
        "Chincholi": [
            "Taluk Hospital Chincholi"
        ],
        "Jevargi": [
            "Taluk Hospital Jevargi"
        ],
        "Sedam": [
            "Taluk Hospital Sedam"
        ]
    },
    "Bengaluru Urban": {
        "Bengaluru North": [
            "Bowring & Lady Curzon Hospital", 
            "KC General Hospital Malleshwaram"
        ],
        "Bengaluru South": [
            "Victoria Hospital Fort", 
            "Vanivilas Women and Children Hospital"
        ],
        "Bengaluru East": [
            "General Hospital Jayanagar"
        ]
    },
    "Belagavi": {
        "Belagavi City": [
            "District Hospital Belagavi", 
            "BIMS (Belagavi Institute of Medical Sciences) Hospital"
        ],
        "Chikkodi": [
            "Government General Hospital Chikkodi"
        ],
        "Bailhongal": [
            "Taluk Hospital Bailhongal"
        ]
    },
    "Mysuru": {
        "Mysuru City": [
            "K.R. Hospital (King Edward VII Memorial Hospital)", 
            "Cheluvamba Hospital", 
            "PKTB Sanatorium"
        ],
        "Nanjangud": [
            "Taluk General Hospital Nanjangud"
        ],
        "Hunsur": [
            "Taluk Hospital Hunsur"
        ]
    }
}

def load_data():
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        df_init = pd.DataFrame(columns=[
            "Complaint ID", "Intake Channel", "District", "Taluka", "Hospital", 
            "Department / Category", "Language", "Voice / Text Transcript", 
            "Status", "Doctor Action / Official Response", "Patient Rating", "Timestamp"
        ])
        df_init.to_csv(DATA_FILE, index=False)
    try:
        return pd.read_csv(DATA_FILE)
    except Exception:
        df_init = pd.DataFrame(columns=[
            "Complaint ID", "Intake Channel", "District", "Taluka", "Hospital", 
            "Department / Category", "Language", "Voice / Text Transcript", 
            "Status", "Doctor Action / Official Response", "Patient Rating", "Timestamp"
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
    st.write("For rural patients and citizens to lodge complaints and track doctor responses.")

    tab_call, tab_sms, tab_kiosk, tab_track = st.tabs([
        "📞 Live Audio Call / IVR", 
        "📱 SMS Gateway", 
        "🏥 Hospital Helpdesk Kiosk", 
        "🔍 Track Status & Provide Rating"
    ])

    # --- TAB 1: LIVE AUDIO CALL SIMULATION ---
    with tab_call:
        st.subheader("Interactive Voice Response (IVR) & Call Portal")
        with st.form("call_form"):
            selected_district = st.selectbox("Select District", list(HOSPITAL_DATABASE.keys()))
            available_talukas = list(HOSPITAL_DATABASE[selected_district].keys())
            selected_taluka = st.selectbox("Select Taluka", available_talukas)
            available_hospitals = HOSPITAL_DATABASE[selected_district][selected_taluka]
            selected_hospital = st.selectbox("Select Government Hospital", available_hospitals)
            
            call_lang = st.selectbox("Select Language", ["Kannada (ಕನ್ನಡ)", "Hindi (हिन्दी)", "English"])
            
            voice_transcript = st.text_area(
                "Voice Call Transcript:", 
                placeholder="ಆಸ್ಪತ್ರೆಯಲ್ಲಿ ವೈದ್ಯರು ಲಭ್ಯವಿಲ್ಲ / Doctors unavailable in emergency ward..."
            )

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
                elif "clean" in txt or "water" in txt or "hygiene" in txt:
                    cat = "Cleanliness & Sanitation"

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
                    "Doctor Action / Official Response": "Awaiting doctor/staff response",
                    "Patient Rating": "Not Rated Yet",
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }])
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.success(f"Grievance successfully registered! Unique Ticket ID: **{cid}**")

    # --- TAB 2: SMS GATEWAY ---
    with tab_sms:
        st.subheader("SMS / Feature Phone Gateway")
        with st.form("sms_form"):
            sms_district = st.selectbox("Select District", list(HOSPITAL_DATABASE.keys()), key="sms_dist")
            sms_taluka = st.selectbox("Select Taluka", list(HOSPITAL_DATABASE[sms_district].keys()), key="sms_tal")
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
                    "Doctor Action / Official Response": "Awaiting staff response",
                    "Patient Rating": "Not Rated Yet",
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }])
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.success(f"SMS registered successfully! Ticket ID: **{cid}**")

    # --- TAB 3: HELP DESK KIOSK ---
    with tab_kiosk:
        st.subheader("Assisted Hospital Helpdesk Kiosk")
        with st.form("kiosk_form"):
            k_district = st.selectbox("Select District", list(HOSPITAL_DATABASE.keys()), key="k_dist")
            k_taluka = st.selectbox("Select Taluka", list(HOSPITAL_DATABASE[k_district].keys()), key="k_tal")
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
                    "Doctor Action / Official Response": "Awaiting staff response",
                    "Patient Rating": "Not Rated Yet",
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }])
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.success(f"Helpdesk grievance logged! Ticket ID: **{cid}**")

    # --- TAB 4: TRACK STATUS & PATIENT FEEDBACK ---
    with tab_track:
        st.subheader("Track Status & Submit Feedback")
        search_id = st.text_input("Enter Unique Complaint ID (e.g., HOSP-CALL-...):")
        
        if st.button("Search Ticket"):
            df = load_data()
            if not df.empty:
                result = df[df["Complaint ID"] == search_id.strip()]
                if not result.empty:
                    st.dataframe(result[["Complaint ID", "Hospital", "Voice / Text Transcript", "Status", "Doctor Action / Official Response", "Patient Rating"]])
                    
                    status = result["Status"].values[0]
                    doc_response = result["Doctor Action / Official Response"].values[0]
                    
                    if status == "Resolved":
                        st.success(f"✅ **Doctor/Staff Response:** {doc_response}")
                        st.markdown("### 🌟 Rate the Hospital Staff Action")
                        rating = st.slider("Select Rating (1 = Poor, 5 = Excellent Stars)", 1, 5, 5)
                        
                        if st.button("Submit Rating"):
                            df.loc[df["Complaint ID"] == search_id.strip(), "Patient Rating"] = f"⭐ {rating} Stars"
                            df.to_csv(DATA_FILE, index=False)
                            st.success(f"Thank you! You rated the resolution {rating} Stars.")
                            st.rerun()
                    elif status == "In Progress":
                        st.info(f"⏳ **Status:** In Progress. Response: {doc_response}")
                        st.warning("Rating option will open once the doctor/staff marks this issue as Resolved.")
                    else:
                        st.warning("⏳ **Status:** Pending. Doctor/Staff have not reviewed this complaint yet.")
                        st.warning("Rating option will open after hospital action is taken.")
                else:
                    st.error("Complaint ID not found.")
            else:
                st.info("No records available.")

# ---------------------------------------------------------
# PORTAL 2: DOCTOR & HOSPITAL STAFF PORTAL ONLY
# ---------------------------------------------------------
elif portal_choice == "🩺 Doctor & Hospital Staff Portal":
    st.title("🩺 Doctor & Hospital Staff Action Portal")
    st.write("Exclusively for doctors and hospital staff to inspect patient complaints and record action taken.")
    
    df = load_data()
    
    staff_district = st.selectbox("Filter by District", ["All Districts"] + list(HOSPITAL_DATABASE.keys()))
    if staff_district != "All Districts":
        df_filtered = df[df["District"] == staff_district]
    else:
        df_filtered = df

    st.subheader("Pending Patient Complaints")
    if not df_filtered.empty:
        st.dataframe(df_filtered[["Complaint ID", "Hospital", "Department / Category", "Voice / Text Transcript", "Status", "Doctor Action / Official Response"]])
        
        active_ids = df_filtered["Complaint ID"].tolist()
        if active_ids:
            st.markdown("---")
            st.subheader("📝 Answer & Resolve Complaint")
            doc_selected_id = st.selectbox("Select Ticket ID to Answer", active_ids)
            
            patient_issue = df.loc[df["Complaint ID"] == doc_selected_id, "Voice / Text Transcript"].values[0]
            st.info(f"**Patient Complaint Message:** {patient_issue}")
            
            doctor_answer = st.text_area(
                "Doctor / Staff Action Remarks & Answer:", 
                placeholder="e.g., Attending physician deployed to Emergency Ward. Doctor is now available."
            )
            
            col_d1, col_d2 = st.columns(2)
            if col_d1.button("Mark In Progress"):
                df.loc[df["Complaint ID"] == doc_selected_id, "Status"] = "In Progress"
                df.loc[df["Complaint ID"] == doc_selected_id, "Doctor Action / Official Response"] = doctor_answer
                df.to_csv(DATA_FILE, index=False)
                st.success(f"Ticket {doc_selected_id} updated to In Progress.")
                st.rerun()
                
            if col_d2.button("Mark Resolved & Submit Answer"):
                if doctor_answer.strip():
                    df.loc[df["Complaint ID"] == doc_selected_id, "Status"] = "Resolved"
                    df.loc[df["Complaint ID"] == doc_selected_id, "Doctor Action / Official Response"] = doctor_answer
                    df.to_csv(DATA_FILE, index=False)
                    st.success(f"Ticket {doc_selected_id} answered and marked Resolved!")
                    st.rerun()
                else:
                    st.error("Please write your action remarks/answer before marking resolved.")
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
    col2.metric("Pending", len(df[df["Status"] == "Pending"]))
    col3.metric("In Progress", len(df[df["Status"] == "In Progress"]))
    col4.metric("Resolved", len(df[df["Status"] == "Resolved"]))

    st.markdown("---")
    st.subheader("Master Grievance & Patient Feedback Registry")
    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No grievances recorded yet.")
