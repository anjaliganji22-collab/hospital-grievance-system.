import streamlit as st
import pandas as pd
import os
import datetime
import random

st.set_page_config(
    page_title="Accessible Voice-Based Public Grievance System",
    page_icon="🏥",
    layout="wide"
)

DATA_FILE = "complaints.csv"

# Robust initialization: always ensure file exists with correct columns
def load_data():
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        df_init = pd.DataFrame(columns=[
            "Complaint ID", "Intake Channel", "Hospital", "Department / Category", 
            "Language", "Voice Transcript / Message", "Status", "Action Taken", "Timestamp"
        ])
        df_init.to_csv(DATA_FILE, index=False)
    try:
        return pd.read_csv(DATA_FILE)
    except Exception:
        df_init = pd.DataFrame(columns=[
            "Complaint ID", "Intake Channel", "Hospital", "Department / Category", 
            "Language", "Voice Transcript / Message", "Status", "Action Taken", "Timestamp"
        ])
        df_init.to_csv(DATA_FILE, index=False)
        return df_init

st.sidebar.title("🏥 Solvathon 2026 Navigation")
portal_choice = st.sidebar.radio(
    "Select Portal", 
    [
        "🗣️ Citizen Intake (IVR, SMS & Kiosk)", 
        "🩺 Doctor & Department Portal", 
        "📊 Admin & Authority Dashboard"
    ]
)

if portal_choice == "🗣️ Citizen Intake (IVR, SMS & Kiosk)":
    st.title("🗣️ Accessible Public Grievance & Hospital Monitoring System")
    st.write("Designed for rural citizens without smartphones via IVR voice calls, SMS, or assisted kiosk registration.")

    tab_ivr, tab_sms, tab_kiosk, tab_track = st.tabs([
        "📞 IVR / Voice Call", 
        "📱 SMS Portal", 
        "🏥 Helpdesk Kiosk", 
        "🔍 Track Status & Feedback"
    ])

    with tab_ivr:
        st.subheader("Interactive Voice Response (IVR) Simulation")
        with st.form("ivr_form"):
            ivr_hospital = st.selectbox(
                "Select Hospital",
                ["District Government Hospital Kalaburagi", "Taluk Hospital Shahabad", "Community Health Centre Aland"]
            )
            ivr_lang = st.selectbox("Select Language", ["Kannada (ಕನ್ನಡ)", "Hindi (हिन्दी)", "English"])
            
            ivr_transcript = st.text_area(
                "Grievance Voice Transcript:", 
                placeholder="ಆಸ್ಪತ್ರೆಯಲ್ಲಿ ವೈದ್ಯರು ಇಲ್ಲ / Doctors not available..."
            )

            submitted_ivr = st.form_submit_button("Submit Voice Grievance")
            
            if submitted_ivr and ivr_transcript.strip():
                df = load_data()
                cid = f"HOSP-IVR-{datetime.datetime.now().strftime('%Y%m%d')}-{random.randint(100, 999)}"
                
                cat = "General Facilities"
                txt = ivr_transcript.lower()
                if "doctor" in txt or "ವೈದ್ಯ" in txt or "staff" in txt:
                    cat = "Doctors & Staff Availability"
                elif "medicine" in txt or "tablet" in txt or "ಔಷಧಿ" in txt:
                    cat = "Medicine Availability"
                elif "clean" in txt or "water" in txt or "hygiene" in txt:
                    cat = "Cleanliness & Sanitation"

                new_row = pd.DataFrame([{
                    "Complaint ID": cid,
                    "Intake Channel": "Voice Call / IVR",
                    "Hospital": ivr_hospital,
                    "Department / Category": cat,
                    "Language": ivr_lang,
                    "Voice Transcript / Message": ivr_transcript,
                    "Status": "Pending",
                    "Action Taken": "Forwarded to Medical Superintendent",
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }])
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.success(f"Voice grievance successfully registered! Unique ID: **{cid}**")

    with tab_sms:
        st.subheader("SMS / USSD Gateway (For Feature Phones)")
        with st.form("sms_form"):
            sms_hospital = st.selectbox(
                "Select Hospital",
                ["District Government Hospital Kalaburagi", "Taluk Hospital Shahabad", "Community Health Centre Aland"],
                key="sms_hosp"
            )
            sms_body = st.text_area("SMS Text Message", placeholder="MEDICINE SHORTAGE IN WARD 2")
            submitted_sms = st.form_submit_button("Send SMS Grievance")
            
            if submitted_sms and sms_body.strip():
                df = load_data()
                cid = f"HOSP-SMS-{datetime.datetime.now().strftime('%Y%m%d')}-{random.randint(100, 999)}"
                new_row = pd.DataFrame([{
                    "Complaint ID": cid,
                    "Intake Channel": "SMS / Feature Phone",
                    "Hospital": sms_hospital,
                    "Department / Category": "Medicine Availability",
                    "Language": "Regional Code",
                    "Voice Transcript / Message": sms_body,
                    "Status": "Pending",
                    "Action Taken": "Forwarded to Pharmacist",
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }])
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.success(f"SMS registered successfully! Ticket ID: **{cid}**")

    with tab_kiosk:
        st.subheader("Hospital Helpdesk / Assisted Kiosk Portal")
        with st.form("kiosk_form"):
            kiosk_hosp = st.selectbox(
                "Select Hospital",
                ["District Government Hospital Kalaburagi", "Taluk Hospital Shahabad", "Community Health Centre Aland"],
                key="kiosk_hosp"
            )
            issue_desc = st.text_area("Detailed Issue Description", placeholder="Describe cleanliness, doctor availability, or equipment failure...")
            submitted_kiosk = st.form_submit_button("Submit Assisted Grievance")
            
            if submitted_kiosk and issue_desc.strip():
                df = load_data()
                cid = f"HOSP-KIOSK-{datetime.datetime.now().strftime('%Y%m%d')}-{random.randint(100, 999)}"
                new_row = pd.DataFrame([{
                    "Complaint ID": cid,
                    "Intake Channel": "Assisted Helpdesk Kiosk",
                    "Hospital": kiosk_hosp,
                    "Department / Category": "General Facilities",
                    "Language": "Assisted Entry",
                    "Voice Transcript / Message": issue_desc,
                    "Status": "Pending",
                    "Action Taken": "Forwarded to Hospital Administration",
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }])
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_csv(DATA_FILE, index=False)
                st.success(f"Assisted grievance logged! Ticket ID: **{cid}**")

    with tab_track:
        st.subheader("Track Complaint Status & Feedback")
        search_id = st.text_input("Enter Unique Complaint ID:")
        
        if st.button("Search Ticket"):
            df = load_data()
            if not df.empty:
                result = df[df["Complaint ID"] == search_id.strip()]
                if not result.empty:
                    st.dataframe(result)
                    if result["Status"].values[0] == "Resolved":
                        st.info("Your issue has been marked resolved.")
                        st.slider("Patient Satisfaction Rating (1 to 5 Stars)", 1, 5, 5)
                        if st.button("Submit Feedback"):
                            st.success("Thank you for your feedback!")
                else:
                    st.error("Complaint ID not found.")
            else:
                st.info("No records available.")

elif portal_choice == "🩺 Doctor & Department Portal":
    st.title("🩺 Doctor & Departmental Staff Portal")
    st.write("Allows medical officers and department heads to view and address department-specific issues.")
    
    df = load_data()
    selected_dept = st.selectbox(
        "Select Your Department / Focus Area",
        ["All Departments", "Doctors & Staff Availability", "Medicine Availability", "Cleanliness & Sanitation", "General Facilities"]
    )

    dept_df = df if selected_dept == "All Departments" else df[df["Department / Category"] == selected_dept]

    st.subheader(f"Grievances for: {selected_dept}")
    if not dept_df.empty:
        st.dataframe(dept_df)
        active_ids = dept_df["Complaint ID"].tolist()
        if active_ids:
            doc_selected_id = st.selectbox("Select Ticket ID to Resolve", active_ids)
            doc_action = st.text_input("Action Taken / Clinical Remarks", placeholder="e.g., Staff deployed to emergency ward.")
            
            col_d1, col_d2 = st.columns(2)
            if col_d1.button("Mark as In Progress"):
                df.loc[df["Complaint ID"] == doc_selected_id, "Status"] = "In Progress"
                df.loc[df["Complaint ID"] == doc_selected_id, "Action Taken"] = doc_action
                df.to_csv(DATA_FILE, index=False)
                st.success("Updated to In Progress.")
                st.rerun()
                
            if col_d2.button("Mark as Resolved"):
                df.loc[df["Complaint ID"] == doc_selected_id, "Status"] = "Resolved"
                df.loc[df["Complaint ID"] == doc_selected_id, "Action Taken"] = doc_action
                df.to_csv(DATA_FILE, index=False)
                st.success("Marked as Resolved.")
                st.rerun()
    else:
        st.info("No issues found for this department.")

else:
    st.title("📊 Hospital Service Monitoring & Authority Dashboard")
    df = load_data()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Grievances", len(df))
    col2.metric("Pending", len(df[df["Status"] == "Pending"]))
    col3.metric("In Progress", len(df[df["Status"] == "In Progress"]))
    col4.metric("Resolved", len(df[df["Status"] == "Resolved"]))

    st.markdown("---")
    st.subheader("Master Grievance Registry")
    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No grievances recorded yet.")
    
