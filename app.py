import streamlit as st
import pandas as pd
from datetime import datetime

# Set up the Streamlit app
st.title("Teacher Portal")

# Sidebar for teacher selection
teachers = ["Teacher 1", "Teacher 2", "Teacher 3", "Teacher 4", "Teacher 5", "Teacher 6", "Teacher 7", "Teacher 8"]
teacher = st.sidebar.selectbox("Select Teacher", teachers)

# Main area with text area for "Daily Comments / Handover Notes"
daily_comments = st.text_area("Daily Comments / Handover Notes")

# Sidebar or secondary column with a checklist of behaviors
st.sidebar.header("Behaviors Checklist")
focused = st.sidebar.checkbox("Focused")
disrupted = st.sidebar.checkbox("Disrupted")
completed_tasks = st.sidebar.checkbox("Completed Tasks")
followed_directions = st.sidebar.checkbox("Followed Directions")

# "Submit Entry" button
if st.button("Submit Entry"):
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Prepare the data to append to the Google Sheet
    data = {
        "Timestamp": [timestamp],
        "Teacher Name": [teacher],
        "Daily Comments": [daily_comments],
        "Focused": [focused],
        "Disrupted": [disrupted],
        "Completed Tasks": [completed_tasks],
        "Followed Directions": [followed_directions]
    }
    
    # Convert the data to a DataFrame
    df = pd.DataFrame(data)
    
    # Connect to the Google Sheet
    conn = st.experimental_connection("gsheets", type="sheet")
    
    # Append the new row to the Google Sheet
    conn.append(df, sheet_url="https://docs.google.com/spreadsheets/d/1xs-j1mCz6QEV2_-PFffxfI0TqnRhNzZskrE1pvhENOU/edit?usp=sharing", index=False)
    
    # Show a success message
    st.success("Entry submitted successfully!")
