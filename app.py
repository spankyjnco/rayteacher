import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# Set up the Streamlit app
st.title("Teacher Portal")

# URL of your Google Sheet
SHEET_URL = "https://docs.google.com/spreadsheets/d/1xs-j1mCz6QEV2_-PFffxfI0TqnRhNzZskrE1pvhENOU/edit?usp=sharing"

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
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Prepare the data to append to the Google Sheet (using 'Yes'/'No' instead of True/False for clean sheet data)
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
    
    # Convert the data to a DataFrame
    new_df = pd.DataFrame(data)
    
    try:
        # Establish connection correctly using the standard gsheets provider
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        # Read the current sheet data
        existing_df = conn.read(spreadsheet=SHEET_URL)
        
        # Combine the old data with the new submission row
        updated_df = pd.concat([existing_df, new_df], ignore_index=True)
        
        # Write everything back to update your Google Sheet
        conn.update(spreadsheet=SHEET_URL, data=updated_df)
        
        # Show a success message
        st.success("Entry submitted successfully!")
        st.balloons()
        
    except Exception as e:
        st.error(f"Error saving to Google Sheets: {e}")
        st.info("Make sure your Google Sheet sharing settings are set to 'Anyone with the link can edit'.")
