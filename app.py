import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

st.title("Teacher Portal")

teachers = ["Teacher 1", "Teacher 2", "Teacher 3", "Teacher 4",
            "Teacher 5", "Teacher 6", "Teacher 7", "Teacher 8"]
teacher = st.sidebar.selectbox("Select Teacher", teachers)

st.sidebar.header("Behaviors Checklist")
good_day = st.sidebar.checkbox("Good Day")
completed_tasks = st.sidebar.checkbox("Completed Tasks")
followed_directions = st.sidebar.checkbox("Followed Directions")
disrupted_others = st.sidebar.checkbox("Disrupted Others")
late_to_class = st.sidebar.checkbox("Late to class")
left_class = st.sidebar.checkbox("Left class")
curse_words = st.sidebar.checkbox("Curse Words")
defied_authority = st.sidebar.checkbox("Defied Authority")

daily_comments = st.text_area("Daily Comments / Handover Notes")

if st.button("Submit Entry"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    row = [
        timestamp,
        teacher,
        daily_comments,
        "Yes" if good_day else "No",
        "Yes" if completed_tasks else "No",
        "Yes" if followed_directions else "No",
        "Yes" if disrupted_others else "No",
        "Yes" if late_to_class else "No",
        "Yes" if left_class else "No",
        "Yes" if curse_words else "No",
        "Yes" if defied_authority else "No",
    ]

    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        # Copy secrets and force proper newlines
        creds_info = dict(st.secrets["gcp_service_account"])
        creds_info["private_key"] = creds_info["private_key"].replace("\\n", "\n")

        creds = Credentials.from_service_account_info(
            creds_info,
            scopes=scopes
        )

        gc = gspread.authorize(creds)
        sh = gc.open_by_url(st.secrets["gcp_service_account"]["spreadsheet"])
        worksheet = sh.get_worksheet(0)

        worksheet.append_row(row)

        st.success("Entry submitted successfully!")
        st.balloons()

    except Exception as e:
        st.error(f"Error saving to Google Sheets: {e}")
