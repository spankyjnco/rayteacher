import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# Set up the Streamlit app
st.title("Teacher Portal")

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
        import gspread
        from google.oauth2.service_account import Credentials

        # 1. Fetch your unchangeable credentials block from secrets
        gcp_config = dict(st.secrets["gcp_service_account"])
        sheet_url = gcp_config["spreadsheet"]

        # Define OAuth scopes for Google Sheets read/write access
        scopes = ["https://googleapis.com"]

        # 2. Authenticate directly using your custom dictionary payload
        creds = Credentials.from_service_account_info(gcp_config, scopes=scopes)
        gc = gspread.authorize(creds)

        # 3. Open your specific spreadsheet and target the first worksheet tab
        sh = gc.open_by_url(sheet_url)
        worksheet = sh.get_worksheet(0) 

        # 4. Directly append the single form submission row to the bottom of the sheet
        row_to_append = new_df.values.tolist()[0]
        worksheet.append_row(row_to_append)
        
        st.success("Entry submitted successfully!")
        st.balloons()
        
    except Exception as e:
        st.error(f"Error saving to Google Sheets: {e}")
