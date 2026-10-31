
import os
import sqlite3
from datetime import date

import pandas as pd
import streamlit as st


# =====================================================
# PAGE CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="Digital Complaint Management System",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Use the database in the same folder as app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "complaints_new.db")

CATEGORIES = [
    "Academic",
    "Infrastructure",
    "Hostel",
    "Transport",
    "Fees",
    "Other"
]

STATUSES = ["Pending", "In Progress", "Resolved"]


# =====================================================
# DATABASE CONNECTION
# =====================================================
def get_connection():
    conn = sqlite3.connect(DB_NAME, timeout=10)
    conn.execute("PRAGMA busy_timeout = 10000")
    return conn


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                date TEXT NOT NULL,
                status TEXT DEFAULT 'Pending'
            )
        """)
        conn.commit()


initialize_database()


# =====================================================
# PROFESSIONAL DARK THEME
# =====================================================
st.markdown("""
<style>

/* ===== GLOBAL BACKGROUND ===== */
:root {
    color-scheme: dark;
}

html,
body,
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stBottom"],
[data-testid="stBottomBlockContainer"] {
    background: #080B14 !important;
    color: #F1F5F9 !important;
}

/* Main content spacing */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 1500px !important;
}

/* ===== TEXT ===== */
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp p,
.stApp label,
.stApp li,
.stApp strong,
.stMarkdown,
[data-testid="stWidgetLabel"] {
    color: #F1F5F9 !important;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"],
[data-testid="stSidebarContent"] {
    background: #0D1220 !important;
    color: #F1F5F9 !important;
}

/* ===== MAIN TITLE ===== */
.main-title {
    background: linear-gradient(120deg, #171044, #351078 55%, #641BEA);
    padding: 28px 30px;
    border-radius: 16px;
    border: 1px solid #493080;
    margin-bottom: 28px;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.25);
}

.main-title h1 {
    color: #FFFFFF !important;
    font-size: 34px;
    font-weight: 750;
    margin: 0;
}

.main-title p {
    color: #E9D5FF !important;
    font-size: 15px;
    margin-top: 10px;
    margin-bottom: 0;
}

/* ===== SECTION CARDS ===== */
[data-testid="stForm"],
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stExpander"] {
    background: #101625 !important;
    border: 1px solid #293449 !important;
    border-radius: 14px !important;
}

/* ===== INPUT FIELDS ===== */
.stApp input,
.stApp textarea,
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea {
    background-color: #151D2E !important;
    color: #F8FAFC !important;
    -webkit-text-fill-color: #F8FAFC !important;
    border-color: #374151 !important;
    border-radius: 8px !important;
}

/* ===== SELECTBOX ===== */
[data-baseweb="select"] > div {
    background-color: #151D2E !important;
    border: 1px solid #374151 !important;
    color: #F8FAFC !important;
    border-radius: 8px !important;
}

[data-baseweb="select"] input {
    color: #F8FAFC !important;
    -webkit-text-fill-color: #F8FAFC !important;
}

[data-baseweb="select"] span {
    color: #F8FAFC !important;
}

[data-baseweb="select"] svg {
    fill: #F8FAFC !important;
    color: #F8FAFC !important;
}

/* Dropdown popup */
[data-baseweb="popover"],
[data-baseweb="popover"] > div,
[data-baseweb="menu"],
[role="listbox"],
[role="option"] {
    background-color: #151D2E !important;
    color: #F8FAFC !important;
}

[role="option"]:hover {
    background-color: #293449 !important;
}

/* ===== BUTTONS ===== */
.stApp button,
.stApp [data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, #7C3AED, #6D28D9) !important;
    color: #FFFFFF !important;
    border: 1px solid #8B5CF6 !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
    min-height: 42px;
}

.stApp button p,
.stApp button span {
    color: #FFFFFF !important;
}

.stApp button:hover {
    background: #5B21B6 !important;
    border-color: #A78BFA !important;
}

/* ===== METRIC CARDS ===== */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #151D31, #101626) !important;
    border: 1px solid #293449 !important;
    border-radius: 14px !important;
    padding: 18px !important;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricValue"],
[data-testid="stMetricDelta"] {
    color: #F1F5F9 !important;
}

/* ===== TABS ===== */
[data-testid="stTabs"] [role="tablist"] {
    background: #0D1220 !important;
    border-bottom: 1px solid #293449 !important;
}

[data-testid="stTabs"] button {
    background: transparent !important;
    color: #CBD5E1 !important;
    border: none !important;
}

[data-testid="stTabs"] button[aria-selected="true"] {
    color: #C4B5FD !important;
    border-bottom: 2px solid #8B5CF6 !important;
}

/* ===== DATAFRAME CONTAINER ===== */
[data-testid="stDataFrame"],
[data-testid="stDataFrame"] > div,
[data-testid="stTable"] {
    background: #111827 !important;
    color: #F1F5F9 !important;
    border: 1px solid #293449 !important;
    border-radius: 10px !important;
    overflow: hidden;
}

/* ===== DIVIDERS ===== */
hr {
    border-color: #293449 !important;
}

/* ===== LINKS ===== */
.stApp a {
    color: #A78BFA !important;
}

/* ===== ALERTS ===== */
[data-testid="stAlert"] {
    background: #111827 !important;
    border: 1px solid #374151 !important;
    color: #F1F5F9 !important;
}

/* ===== FOOTER ===== */
footer {
    visibility: hidden;
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar {
    width: 9px;
    height: 9px;
}

::-webkit-scrollbar-track {
    background: #080B14;
}

::-webkit-scrollbar-thumb {
    background: #374151;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# PAGE HEADER
# =====================================================
st.markdown("""
<div class="main-title">
    <h1>📋 Digital Complaint Management System</h1>
    <p>Submit, track and manage complaints through one central platform.</p>
</div>
""", unsafe_allow_html=True)


# =====================================================
# LOAD COMPLAINTS
# =====================================================
def load_complaints():
    with get_connection() as conn:
        return pd.read_sql_query(
            """
            SELECT id, name, category, description, date, status
            FROM complaints
            ORDER BY id DESC
            """,
            conn
        )


def get_complaint_count():
    with get_connection() as conn:
        result = conn.execute(
            "SELECT COUNT(*) FROM complaints"
        ).fetchone()
        return result[0]


def add_complaint(name, category, description):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO complaints
                (name, category, description, date, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, category, description, str(date.today()), "Pending")
        )
        conn.commit()


def update_complaint_status(complaint_id, status):
    with get_connection() as conn:
        conn.execute(
            "UPDATE complaints SET status = ? WHERE id = ?",
            (status, complaint_id)
        )
        conn.commit()


def update_complaint_details(complaint_id, name, category, description):
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE complaints
            SET name = ?, category = ?, description = ?
            WHERE id = ?
            """,
            (name, category, description, complaint_id)
        )
        conn.commit()


def delete_complaint(complaint_id):
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM complaints WHERE id = ?",
            (complaint_id,)
        )
        conn.commit()


df = load_complaints()


# =====================================================
# DASHBOARD METRICS
# =====================================================
total = len(df)
pending = int((df["status"] == "Pending").sum()) if total else 0
in_progress = int((df["status"] == "In Progress").sum()) if total else 0
resolved = int((df["status"] == "Resolved").sum()) if total else 0

st.subheader("📊 Dashboard Overview")

m1, m2, m3, m4 = st.columns(4)

m1.metric("Total Complaints", total)
m2.metric("Pending", pending)
m3.metric("In Progress", in_progress)
m4.metric("Resolved", resolved)

st.markdown("---")


# =====================================================
# SUBMIT COMPLAINT
# =====================================================
st.subheader("📝 Submit a Complaint")

with st.form("complaint_submission_form", clear_on_submit=True):

    name = st.text_input(
        "Student Name",
        placeholder="Enter your full name"
    )

    category = st.selectbox(
        "Category",
        CATEGORIES
    )

    description = st.text_area(
        "Complaint Description",
        placeholder="Describe your complaint in detail...",
        height=130
    )

    submitted = st.form_submit_button(
        "➕ Submit Complaint",
        use_container_width=True
    )

    if submitted:
        if not name.strip():
            st.error("Please enter your name.")
        elif not description.strip():
            st.error("Please enter the complaint description.")
        else:
            add_complaint(
                name.strip(),
                category,
                description.strip()
            )
            st.success("Complaint submitted successfully!")
            st.rerun()


st.markdown("---")


# =====================================================
# COMPLAINT RECORDS
# =====================================================
st.subheader("📂 Complaint Records")

df = load_complaints()

if df.empty:
    st.info("No complaints have been submitted yet.")
else:

    # Search and filters
    search_col, status_col, category_col = st.columns([2, 1, 1])

    with search_col:
        search_text = st.text_input(
            "Search complaints",
            placeholder="Search name, category, description, ID..."
        )

    with status_col:
        selected_status = st.selectbox(
            "Filter by status",
            ["All"] + STATUSES
        )

    with category_col:
        selected_category = st.selectbox(
            "Filter by category",
            ["All"] + CATEGORIES
        )

    filtered_df = df.copy()

    if search_text.strip():
        query = search_text.strip()

        search_mask = (
            filtered_df.astype(str)
            .apply(
                lambda column: column.str.contains(
                    query,
                    case=False,
                    na=False,
                    regex=False
                )
            )
            .any(axis=1)
        )

        filtered_df = filtered_df[search_mask]

    if selected_status != "All":
        filtered_df = filtered_df[
            filtered_df["status"] == selected_status
        ]

    if selected_category != "All":
        filtered_df = filtered_df[
            filtered_df["category"] == selected_category
        ]

    # Display friendly column names
    display_df = filtered_df.rename(columns={
        "id": "ID",
        "name": "Student Name",
        "category": "Category",
        "description": "Description",
        "date": "Date",
        "status": "Status"
    })

      # ===== PROFESSIONAL DARK HTML TABLE =====

    safe_df = display_df.fillna("").astype(str)

    table_html = safe_df.to_html(
        index=False,
        escape=True,
        border=0,
        classes="complaint-table"
    )

    st.markdown("""
    <style>
    .complaint-table-wrapper {
        width: 100%;
        overflow-x: auto;
        border: 1px solid #334155;
        border-radius: 12px;
        margin-top: 12px;
    }

    table.complaint-table {
        width: 100%;
        min-width: 850px;
        border-collapse: collapse;
        background: #111827 !important;
        color: #F1F5F9 !important;
        font-size: 14px;
    }

    table.complaint-table thead th {
        background: #1E293B !important;
        color: #C4B5FD !important;
        padding: 15px 12px;
        text-align: left;
        border-bottom: 1px solid #475569;
        white-space: nowrap;
    }

    table.complaint-table tbody td {
        background: #111827 !important;
        color: #F1F5F9 !important;
        padding: 13px 12px;
        border-bottom: 1px solid #293449;
        text-align: left;
        overflow-wrap: anywhere;
    }

    table.complaint-table tbody tr:hover td {
        background: #1E293B !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(
        f'<div class="complaint-table-wrapper">{table_html}</div>',
        unsafe_allow_html=True
    )
    st.caption(
        f"Showing {len(filtered_df)} of {len(df)} complaint(s)."
    )


st.markdown("---")


# =====================================================
# MANAGE A COMPLAINT
# =====================================================
st.subheader("⚙️ Manage a Complaint")

df = load_complaints()

if df.empty:
    st.info("There are no complaints to manage.")
else:

    complaint_options = {
        f"ID {row['id']} — {row['name']} ({row['status']})": int(row["id"])
        for _, row in df.iterrows()
    }

    selected_label = st.selectbox(
        "Select Complaint ID",
        list(complaint_options.keys())
    )

    selected_id = complaint_options[selected_label]

    selected_row = df[df["id"] == selected_id].iloc[0]

    st.markdown("### Complaint Details")

    info1, info2, info3 = st.columns(3)

    info1.write(f"**Student:** {selected_row['name']}")
    info2.write(f"**Category:** {selected_row['category']}")
    info3.write(f"**Current Status:** {selected_row['status']}")

    st.write(f"**Description:** {selected_row['description']}")
    st.write(f"**Date:** {selected_row['date']}")

    st.markdown("---")

    edit_tab, status_tab, delete_tab = st.tabs([
        "✏️ Edit Complaint",
        "🔄 Update Status",
        "🗑️ Delete Complaint"
    ])

    # -------------------------------------------------
    # EDIT COMPLAINT
    # -------------------------------------------------
    with edit_tab:

        st.markdown("#### Edit Complaint Details")

        with st.form("edit_complaint_form"):

            edit_name = st.text_input(
                "Student Name",
                value=str(selected_row["name"])
            )

            current_category = str(selected_row["category"])

            edit_category = st.selectbox(
                "Category",
                CATEGORIES,
                index=(
                    CATEGORIES.index(current_category)
                    if current_category in CATEGORIES
                    else 0
                )
            )

            edit_description = st.text_area(
                "Description",
                value=str(selected_row["description"]),
                height=130
            )

            save_changes = st.form_submit_button(
                "💾 Save Changes",
                use_container_width=True
            )

            if save_changes:
                if not edit_name.strip():
                    st.error("Student name cannot be empty.")
                elif not edit_description.strip():
                    st.error("Description cannot be empty.")
                else:
                    update_complaint_details(
                        selected_id,
                        edit_name.strip(),
                        edit_category,
                        edit_description.strip()
                    )
                    st.success("Complaint details updated successfully!")
                    st.rerun()

    # -------------------------------------------------
    # UPDATE STATUS
    # -------------------------------------------------
    with status_tab:

        st.markdown("#### Update Complaint Status")

        current_status = str(selected_row["status"])

        new_status = st.selectbox(
            "Choose New Status",
            STATUSES,
            index=(
                STATUSES.index(current_status)
                if current_status in STATUSES
                else 0
            ),
            key="new_complaint_status"
        )

        if st.button(
            "🔄 Update Status",
            use_container_width=True
        ):
            update_complaint_status(selected_id, new_status)
            st.success("Complaint status updated successfully!")
            st.rerun()

    # -------------------------------------------------
    # DELETE COMPLAINT
    # -------------------------------------------------
    with delete_tab:

        st.markdown("#### Delete Complaint")

        st.warning(
            f"You are about to delete complaint ID {selected_id}. "
            "This action cannot be undone."
        )

        confirm_delete = st.checkbox(
            "I confirm that I want to delete this complaint.",
            key="confirm_delete_complaint"
        )

        if st.button(
            "🗑️ Delete Complaint",
            use_container_width=True
        ):
            if confirm_delete:
                delete_complaint(selected_id)
                st.success("Complaint deleted successfully!")
                st.rerun()
            else:
                st.error("Please confirm before deleting the complaint.")


# =====================================================
# FOOTER
# =====================================================
st.markdown("---")

st.markdown("""
<div style="
    text-align: center;
    padding: 18px;
    color: #94A3B8;
    font-size: 13px;
">
    Digital Complaint Management System
    <br>
    Built with Python, Streamlit and SQLite
</div>
""", unsafe_allow_html=True)
