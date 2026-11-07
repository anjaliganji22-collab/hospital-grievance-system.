import streamlit as st
import pandas as pd
import os
import datetime
import random

# Page configuration
st.set_page_config(
    page_title="Public Grievance System",
    page_icon="🏥",
    layout="wide"
)

DATA_FILE = "complaints.csv"

# Create local storage file if it does not exist
if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=[
        "Complaint ID", "Hospital", "Language", "Voice Transcript", 
        "Category", "Status", "Action Taken", "Timestamp"
    ])
    df_init.to_csv(DATA_FILE, index=False)

# Sidebar Navigation
st.sidebar.title("🏥 Navigation")
page = st.sidebar.radio(
    "Select Portal", 
    ["Citizen / Kiosk Portal", "Admin & Monitoring Portal"]
)

# ---------------------------------------------------------
# PORTAL 1: CITIZEN / KIOSK PORTAL
# ---------------------------------------------------------
if page == "Citizen / Kiosk Portal":
    st.title("🗣️ Hospital Public Grievance Portal")
    st.write("Report hospital service-related issues easily without a smartphone.")

    tab1, tab2 = st.tabs(["Submit New Grievance", "Track Status"])

    with tab1:
        st.subheader("Register a Complaint")
        
        # Use a form so mobile inputs are properly captured on submit
        with st.form("grievance_form"):
            hospital_name = st.selectbox(
                "Select Government Hospital",
                ["District Government Hospital Kalaburagi", "Taluk Hospital", "Community Health Centre"]
            )
            
            language = st.selectbox(
                "Select Language",
                ["Kannada", "English", "Hindi"]
            )

            transcript = st.text_area(
                "Grievance Description (Speak or type your issue):",
                placeholder="e.g., Doctors were unavailable at the emergency ward..."
            )

            submitted = st.form_submit_button("Submit Grievance")
            
            if submitted:
                if transcript.strip():
                    complaint_id = f"HOSP-{datetime.datetime.now().strftime('%Y%m%d')}-{random.randint(100, 999)}"
                    
                    category = "General Facilities"
                    text_lower = transcript.lower()
                    if "doctor" in text_lower or "staff" in text_lower:
                        category = "Doctors & Staff Availability"
                    elif "medicine" in text_lower or "tablet" in text_lower:
                        category = "Medicine Availability"
                    elif "clean" in text_lower or "water" in text_lower or "hygiene" in text_lower:
                        category = "Cleanliness & Sanitation"

                    new_data = pd.DataFrame([{
                        "Complaint ID": complaint_id,
                        "Hospital": hospital_name,
                        "Language": language,
                        "Voice Transcript": transcript,
                        "Category": category,
                        "Status": "Pending",
                        "Action Taken": "Awaiting review",
                        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }])
                    
                    new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
                    
                    st.success("Grievance Registered Successfully!")
                    st.info(f"Your Unique Complaint ID: **{complaint_id}**")
                else:
                    st.warning("Please provide a description of the issue.")

    with tab2:
        st.subheader("Track Complaint Status")
        search_id = st.text_input("Enter your Unique Complaint ID:")
        
        if st.button("Search"):
            if os.path.exists(DATA_FILE):
                df = pd.read_csv(DATA_FILE)
                result = df[df["Complaint ID"] == search_id.strip()]
                
                if not result.empty:
                    st.write("### Complaint Details")
                    st.dataframe(result)
                else:
                    st.error("No complaint found with this ID. Please verify.")
            else:
                st.info("No complaints registered yet.")

# ---------------------------------------------------------
# PORTAL 2: ADMIN & MONITORING PORTAL
# ---------------------------------------------------------
else:
    st.title("📊 Hospital Service Monitoring & Grievance Dashboard")
    
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame(columns=["Complaint ID", "Hospital", "Language", "Voice Transcript", "Category", "Status", "Action Taken", "Timestamp"])
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Grievances", len(df))
    col2.metric("Pending", len(df[df["Status"] == "Pending"]))
    col3.metric("Resolved", len(df[df["Status"] == "Resolved"]))

    st.markdown("---")
    st.subheader("All Grievance Records & Management")
    
    if not df.empty:
        st.dataframe(df)
        
        st.markdown("### Update Complaint Status")
        selected_id = st.selectbox("Select Complaint ID to Update", df["Complaint ID"].tolist())
        
        current_status = df.loc[df["Complaint ID"] == selected_id, "Status"].values[0]
        new_status = st.selectbox("Update Status", ["Pending", "In Progress", "Resolved"], index=["Pending", "In Progress", "Resolved"].index(current_status))
        
        action_note = st.text_input("Action Taken Note / Remarks", placeholder="e.g., Staff deployed to emergency ward.")
        
        if st.button("Save Changes"):
            df.loc[df["Complaint ID"] == selected_id, "Status"] = new_status
            df.loc[df["Complaint ID"] == selected_id, "Action Taken"] = action_note
            df.to_csv(DATA_FILE, index=False)
            st.success(f"Complaint {selected_id} updated successfully!")
            st.rerun()
    else:
        st.info("No grievances recorded yet.")
