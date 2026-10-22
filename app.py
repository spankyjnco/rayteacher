import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# Set up the Streamlit app
st.title("Teacher Portal")

# Your exact spreadsheet ID extracted safely to avoid the link filter glitch
REAL_SHEET_URL = "https://docs.google.com/spreadsheets/d/1xs-j1mCz6QEV2_-PFffxfI0TqnRhNzZskrE1pvhENOU/edit?hl=en-GB&gid=0#gid=0"

# Sidebar for teacher selection
teachers = ["Teacher 1", "Teacher 2", "Teacher 3", "Teacher 4", "Teacher 5", "Teacher 6", "Teacher 7", "Teacher 8"]
teacher = st.sidebar.selectbox("Select Teacher", teachers)

# Sidebar with checklist of behaviors
st.sidebar.header("Behaviors Checklist")
good_day = st.sidebar.checkbox("Good Day")
completed_tasks = st.sidebar.checkbox("Completed Tasks")
followed_directions = st.sidebar.checkbox("Followed Directions")
disrupted_others = st.sidebar.checkbox("Disrupted Others")
late_to_class = st.sidebar.checkbox("Late to class")
left_class = st.sidebar.checkbox("Left class")
curse_words = st.sidebar.checkbox("Curse Words")
defied_authority = st.sidebar.checkbox("Defied Authority")

# Main area with text area for "Daily Comments / Handover Notes"
daily_comments = st.text_area("Daily Comments / Handover Notes")

# "Submit Entry" button
if st.button("Submit Entry"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    data = {
        "Timestamp": [timestamp],
        "Teacher Name": [teacher],
        "Daily Comments": [daily_comments],
        "Good Day": ["Yes" if good_day else "No"],
        "Completed Tasks": ["Yes" if completed_tasks else "No"],
        "Followed Directions": ["Yes" if followed_directions else "No"],
        "Disrupted Others": ["Yes" if disrupted_others else "No"],
        "Late to class": ["Yes" if late_to_class else "No"],
        "Left class": ["Yes" if left_class else "No"],
        "Curse Words": ["Yes" if curse_words else "No"],
        "Defied Authority": ["Yes" if defied_authority else "No"]
    }
    
    new_df = pd.DataFrame(data)
    
    try:
        # Connect using the security credentials in secrets
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        # Explicitly pass the full URL directly here so it never looks at the broken secrets link
        existing_df = conn.read(spreadsheet=REAL_SHEET_URL)
        
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        
        # Explicitly update using the hardcoded URL
        conn.update(spreadsheet=REAL_SHEET_URL, data=updated_df)
        
        st.success("Entry submitted successfully!")
        st.balloons()
        
    except Exception as e:
        st.error(f"Error saving to Google Sheets: {e}")
