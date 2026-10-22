import streamlit as st
import pandas as pd
from datetime import datetime

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
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Prepare the data to append to the Google Sheet
    data = {
        "Timestamp": [timestamp],
        "Teacher Name": [teacher],
        "Daily Comments": [daily_comments],
        "Good Day": [good_day],
        "Completed Tasks": [completed_tasks],
        "Followed Directions": [followed_directions],
        "Disrupted Others": [disrupted_others],
        "Late to class": [late_to_class],
        "Left class": [left_class],
        "Curse Words": [curse_words],
        "Defied Authority": [defied_authority]
    }
    
    # Convert the data to a DataFrame
    df = pd.DataFrame(data)
    
    # Connect to the Google Sheet
    conn = st.connection("gsheets", type="sheet")
    
    # Append the new row to the Google Sheet
    conn.append(df, sheet_url="https://docs.google.com/spreadsheets/d/1xs-j1mCz6QEV2_-PFffxfI0TqnRhNzZskrE1pvhENOU/edit?usp=sharing", index=False)
    
    # Show a success message
    st.success("Entry submitted successfully!")
