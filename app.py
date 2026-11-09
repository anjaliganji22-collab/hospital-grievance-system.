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
    st.write("For rural patients and citizens to lodge complaints and track doctor responses.")

    tab_call, tab_sms, tab_kiosk, tab_track = st.tabs([
        "📞 Live Audio Call / IVR", 
        "📱 SMS Gateway", 
        "🏥 Hospital Helpdesk Kiosk", 
        "🔍 Track Status & Escalate"
    ])

    with tab_call:
        st.subheader("Interactive Voice Response (IVR) & Call Portal")
        with st.form("call_form"):
            selected_district = st.selectbox("Select District", list(HOSPITAL_DATABASE.keys()))
            available_talukas = list(HOSPITAL_DATABASE[selected_district].keys())
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
                        st.warning("⚠️ **Notice:** Hospital staff have **not taken any action yet** on this complaint.")
                        
                        if escalation == "Normal":
                            if st.button("🚨 Escalate to District Medical Officer (No Action Taken)"):
                                df.loc[df["Complaint ID"] == search_id.strip(), "Escalation Status"] = "ESCALATED TO DMO ⚠️"
                                df.to_csv(DATA_FILE, index=False)
                                st.error("Complaint has been escalated to district health authorities due to lack of action!")
                                st.rerun()
                        else:
                            st.error("🚨 This complaint is currently **Escalated** to higher authorities due to delayed staff response.")
                            
                    elif status == "Resolved":
                        st.success("✅ This complaint has been resolved and answered by hospital staff.")
                        rating = st.slider("Rate Hospital Staff Resolution (1 to 5 Stars)", 1, 5, 5)
                        if st.button("Submit Rating"):
                            df.loc[df["Complaint ID"] == search_id.strip(), "Patient Rating"] = f"⭐ {rating} Stars"
                            df.to_csv(DATA_FILE, index=False)
                            st.success("Thank you for your feedback!")
                            st.rerun()
                else:
                    st.error("Complaint ID not found.")
            else:
                st.info("No records available.")

# ---------------------------------------------------------
# PORTAL 2: DOCTOR & HOSPITAL STAFF PORTAL
# ---------------------------------------------------------
elif portal_choice == "🩺 Doctor & Hospital Staff Portal":
    st.title("🩺 Doctor & Hospital Staff Action Portal")
    st.write("Review pending patient complaints, verify unaddressed issues, and record official actions.")
    
    df = load_data()
    staff_district = st.selectbox("Filter by District", ["All Districts"] + list(HOSPITAL_DATABASE.keys()))
    if staff_district != "All Districts":
        df_filtered = df[df["District"] == staff_district]
    else:
        df_filtered = df

    st.subheader("Patient Grievances")
    if not df_filtered.empty:
        st.dataframe(df_filtered[["Complaint ID", "Hospital", "Department / Category", "Voice / Text Transcript", "Status", "Escalation Status"]])
        
        active_ids = df_filtered["Complaint ID"].tolist()
        if active_ids:
            st.markdown("---")
            st.subheader("📝 Take Action & Answer Complaint")
            doc_selected_id = st.selectbox("Select Ticket ID", active_ids)
            
            curr_status = df.loc[df["Complaint ID"] == doc_selected_id, "Status"].values[0]
            if curr_status == "Pending":
                st.error("⚠️ Status: No action taken yet by staff.")
            
            doctor_answer = st.text_area("Official Staff Response / Action Taken:", placeholder="Describe the action taken...")
            
            col_d1, col_d2 = st.columns(2)
            if col_d1.button("Mark In Progress"):
                df.loc[df["Complaint ID"] == doc_selected_id, "Status"] = "In Progress"
                df.loc[df["Complaint ID"] == doc_selected_id, "Doctor Action / Official Response"] = doctor_answer
                df.to_csv(DATA_FILE, index=False)
                st.success("Updated to In Progress.")
                st.rerun()
                
            if col_d2.button("Mark Resolved & Submit Answer"):
                if doctor_answer.strip():
                    df.loc[df["Complaint ID"] == doc_selected_id, "Status"] = "Resolved"
                    df.loc[df["Complaint ID"] == doc_selected_id, "Doctor Action / Official Response"] = doctor_answer
                    df.loc[df["Complaint ID"] == doc_selected_id, "Escalation Status"] = "Resolved & Closed"
                    df.to_csv(DATA_FILE, index=False)
                    st.success("Marked as Resolved!")
                    st.rerun()
                else:
                    st.error("Please enter the action remarks before resolving.")
    else:
        st.info("No complaints found.")

# ---------------------------------------------------------
# PORTAL 3: ADMIN & AUTHORITY DASHBOARD
# ---------------------------------------------------------
else:
    st.title("📊 Health Authority Monitoring & Escalation Dashboard")
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
        st.info("No escalated complaints due to staff inaction.")

    st.markdown("---")
    st.subheader("Master Registry")
    if not df.empty:
        st.dataframe(df)
