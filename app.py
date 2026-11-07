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
        "Category", "Status", "Timestamp"
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
    st.write("Report hospital service-related issues easily without a smartphone.")[span_0](start_span)[span_0](end_span)

    tab1, tab2 = st.tabs(["Submit New Grievance", "Track Status"])[span_1](start_span)[span_1](end_span)

    with tab1:
        st.subheader("Register a Complaint")[span_2](start_span)[span_2](end_span)
        
        hospital_name = st.selectbox(
            "Select Government Hospital",
            ["District Government Hospital Kalaburagi", "Taluk Hospital", "Community Health Centre"]
        )
        
        language = st.selectbox(
            "Select Language",
            ["Kannada", "English", "Hindi"]
        )[span_3](start_span)[span_3](end_span)

        transcript = st.text_area(
            "Grievance Description (Speak or type your issue):",
            placeholder="e.g., Doctors were unavailable at the emergency ward..."
        )[span_4](start_span)[span_4](end_span)

        if st.button("Submit Grievance"):
            if transcript.strip():
                # Auto-generate unique Complaint ID[span_5](start_span)[span_5](end_span)
                complaint_id = f"HOSP-{datetime.datetime.now().strftime('%Y%m%d')}-{random.randint(100, 999)}"
                
                # Rule-based auto categorization[span_6](start_span)[span_6](end_span)
                category = "General Facilities"
                text_lower = transcript.lower()
                if "doctor" in text_lower or "staff" in text_lower:
                    category = "Doctors & Staff Availability[span_7](start_span)"[span_7](end_span)
                elif "medicine" in text_lower or "tablet" in text_lower:
                    category = "Medicine Availability[span_8](start_span)"[span_8](end_span)
                elif "clean" in text_lower or "water" in text_lower or "hygiene" in text_lower:
                    category = "Cleanliness & Sanitation[span_9](start_span)"[span_9](end_span)

                # Save grievance record
                new_data = pd.DataFrame([{
                    "Complaint ID": complaint_id,
                    "Hospital": hospital_name,
                    "Language": language,
                    "Voice Transcript": transcript,
                    "Category": category,
                    "Status": "Pending",
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }])
                
                new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
                
                st.success("Grievance Registered Successfully!")
                st.info(f"Your Unique Complaint ID: **{complaint_id}**")[span_10](start_span)[span_10](end_span)
            else:
                st.warning("Please provide a description of the issue.")

    with tab2:
        st.subheader("Track Complaint Status")[span_11](start_span)[span_11](end_span)
        search_id = st.text_input("Enter your Unique Complaint ID:")[span_12](start_span)[span_12](end_span)
        
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
    st.title("📊 Hospital Service Monitoring & Grievance Dashboard")[span_13](start_span)[span_13](end_span)
    
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame(columns=["Complaint ID", "Hospital", "Language", "Voice Transcript", "Category", "Status", "Timestamp"])
    
    # Overview Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Grievances", len(df))
    col2.metric("Pending", len(df[df["Status"] == "Pending"]))[span_14](start_span)[span_14](end_span)
    col3.metric("Resolved", len(df[df["Status"] == "Resolved"]))

    st.markdown("---")
    st.subheader("All Grievance Records")[span_15](start_span)[span_15](end_span)
    
    if not df.empty:
        st.dataframe(df)
    else:
        st.info("No grievances recorded yet.")
