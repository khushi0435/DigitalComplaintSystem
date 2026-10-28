import sqlite3
from datetime import date
import streamlit as st
import pandas as pd

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="Digital Complaint Management System",
    page_icon="📋",
    layout="wide"
)

DB_NAME = "complaints.db"
CATEGORIES = ["Academic", "Infrastructure", "Hostel", "Transport", "Fees", "Other"]
STATUSES = ["Pending", "In Progress", "Resolved"]


# ---------------- DATABASE BACKEND ----------------
def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


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


def fetch_complaints():
    with get_connection() as conn:
        return pd.read_sql_query(
            "SELECT id, name, category, description, date, status "
            "FROM complaints ORDER BY id DESC",
            conn
        )


def add_complaint(name, category, description):
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO complaints (name, category, description, date, status)
               VALUES (?, ?, ?, ?, ?)""",
            (name, category, description, date.today().isoformat(), "Pending")
        )
        conn.commit()


def update_complaint(complaint_id, name, category, description):
    with get_connection() as conn:
        conn.execute(
            """UPDATE complaints
               SET name = ?, category = ?, description = ?
               WHERE id = ?""",
            (name, category, description, int(complaint_id))
        )
        conn.commit()


def update_complaint_status(complaint_id, status):
    with get_connection() as conn:
        conn.execute(
            "UPDATE complaints SET status = ? WHERE id = ?",
            (status, int(complaint_id))
        )
        conn.commit()


def delete_complaint(complaint_id):
    with get_connection() as conn:
        conn.execute("DELETE FROM complaints WHERE id = ?", (int(complaint_id),))
        conn.commit()


initialize_database()



# ---------------- STYLING ----------------
st.markdown("""
<style>
    /* Entire Website Background */
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    [data-testid="stMainBlockContainer"] {
        background-color: #EDE9FE !important;
    }

    /* Main Heading */
    .main-title {
        background: linear-gradient(135deg, #312E81, #6D28D9);
        padding: 1.4rem 1.6rem;
        border-radius: 14px;
        color: #FFFFFF;
        margin-bottom: 1.5rem;
    }

    .main-title h1 {
        color: #FFFFFF;
        margin: 0;
        font-size: 1.8rem;
    }

    .main-title p {
        color: #E9D5FF;
        margin: .4rem 0 0 0;
    }

    /* Dashboard Cards - Lavender, Not White */
    div[data-testid="stMetric"] {
        background-color: #DDD6FE !important;
        padding: 1.2rem;
        border: 1px solid #C4B5FD;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(49, 46, 129, 0.08);
    }

    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #312E81 !important;
    }

    /* Input Fields */
    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox [data-baseweb="select"] > div {
        background-color: #F5F3FF !important;
        color: #312E81 !important;
        border-color: #C4B5FD !important;
    }

    /* Buttons */
    .stButton > button,
    .stFormSubmitButton > button {
        border-radius: 8px;
        font-weight: 600;
    }

    /* Top Header */
    [data-testid="stHeader"] {
        background-color: #EDE9FE !important;
    }

    /* Dividers */
    hr {
        border-color: #C4B5FD !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-title">
    <h1>DCMS | Complaint Management</h1>
    <p>Digital Complaint Management System</p>
</div>
""", unsafe_allow_html=True)


# ---------------- DASHBOARD ----------------
df = fetch_complaints()
total = len(df)
pending = int((df["status"] == "Pending").sum()) if not df.empty else 0
in_progress = int((df["status"] == "In Progress").sum()) if not df.empty else 0
resolved = int((df["status"] == "Resolved").sum()) if not df.empty else 0

m1, m2, m3, m4 = st.columns(4)
m1.metric("TOTAL COMPLAINTS", total)
m2.metric("PENDING", pending)
m3.metric("IN PROGRESS", in_progress)
m4.metric("RESOLVED", resolved)

st.divider()

# ---------------- DASHBOARD ----------------
df = fetch_complaints()
total = len(df)
pending = int((df["status"] == "Pending").sum()) if not df.empty else 0
in_progress = int((df["status"] == "In Progress").sum()) if not df.empty else 0
resolved = int((df["status"] == "Resolved").sum()) if not df.empty else 0

m1, m2, m3, m4 = st.columns(4)
m1.metric("TOTAL COMPLAINTS", total)
m2.metric("PENDING", pending)
m3.metric("IN PROGRESS", in_progress)
m4.metric("RESOLVED", resolved)

st.divider()


# ---------------- SUBMIT COMPLAINT ----------------
st.subheader("📝 Submit New Complaint")
with st.form("add_complaint_form", clear_on_submit=True):
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Student Name")
        category = st.selectbox("Category", CATEGORIES)
    with c2:
        description = st.text_area("Complaint Description", height=105)

    submitted = st.form_submit_button("Submit Complaint", type="primary")

    if submitted:
        if not name.strip() or not description.strip():
            st.error("Please fill in the student name and complaint description.")
        else:
            try:
                add_complaint(name.strip(), category, description.strip())
                st.success("Complaint submitted successfully!")
                st.rerun()
            except sqlite3.Error as error:
                st.error(f"Database error: {error}")

st.divider()


# ---------------- SEARCH AND FILTER ----------------
st.subheader("📂 Complaint Records")
f1, f2, f3 = st.columns([2, 1, 1])
with f1:
    keyword = st.text_input("Search complaints", placeholder="Search name, category, description, ID...")
with f2:
    status_filter = st.selectbox("Filter by status", ["All"] + STATUSES)
with f3:
    category_filter = st.selectbox("Filter by category", ["All"] + CATEGORIES)

df = fetch_complaints()
filtered = df.copy()

if keyword.strip():
    mask = filtered.astype(str).apply(
        lambda col: col.str.contains(keyword.strip(), case=False, na=False, regex=False)
    ).any(axis=1)
    filtered = filtered[mask]

if status_filter != "All":
    filtered = filtered[filtered["status"] == status_filter]

if category_filter != "All":
    filtered = filtered[filtered["category"] == category_filter]

if filtered.empty:
    st.info("No complaints match your search or filters.")
else:
    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True,
        column_config={
            "id": st.column_config.NumberColumn("ID", format="%d"),
            "name": st.column_config.TextColumn("Student Name"),
            "category": st.column_config.TextColumn("Category"),
            "description": st.column_config.TextColumn("Description", width="large"),
            "date": st.column_config.TextColumn("Date"),
            "status": st.column_config.TextColumn("Status")
        }
    )

st.caption(f"Showing {len(filtered)} of {len(df)} complaint(s).")


# ---------------- EDIT / UPDATE STATUS / DELETE ----------------
st.divider()
st.subheader("⚙️ Manage a Complaint")

if df.empty:
    st.info("Submit a complaint first to enable edit, status update, and delete.")
else:
    available_ids = df["id"].astype(int).tolist()
    selected_id = st.selectbox(
        "Select Complaint ID",
        available_ids,
        format_func=lambda value: (
            f"ID {value} — " +
            str(df.loc[df["id"] == value, "name"].iloc[0]) +
            " (" + str(df.loc[df["id"] == value, "status"].iloc[0]) + ")"
        )
    )

    selected_record = df.loc[df["id"] == selected_id].iloc[0]
    tab_edit, tab_status, tab_delete = st.tabs(
        ["✏️ Edit Details", "🔄 Update Status", "🗑️ Delete Complaint"]
    )

    with tab_edit:
        st.write("Update the selected complaint's name, category, or description.")
        with st.form("edit_complaint_form"):
            edit_name = st.text_input("Student Name", value=str(selected_record["name"]))
            current_category = str(selected_record["category"])
            category_index = CATEGORIES.index(current_category) if current_category in CATEGORIES else 0
            edit_category = st.selectbox("Category", CATEGORIES, index=category_index)
            edit_description = st.text_area(
                "Description", value=str(selected_record["description"]), height=100
            )
            save_edit = st.form_submit_button("Save Changes", type="primary")

            if save_edit:
                if not edit_name.strip() or not edit_description.strip():
                    st.error("All fields are required.")
                else:
                    try:
                        update_complaint(
                            selected_id, edit_name.strip(),
                            edit_category, edit_description.strip()
                        )
                        st.success("Complaint updated successfully.")
                        st.rerun()
                    except sqlite3.Error as error:
                        st.error(f"Database error: {error}")

    with tab_status:
        current_status = str(selected_record["status"])
        status_index = STATUSES.index(current_status) if current_status in STATUSES else 0
        new_status = st.selectbox("Choose new status", STATUSES, index=status_index)
        if st.button("Save Status", type="primary"):
            try:
                update_complaint_status(selected_id, new_status)
                st.success("Complaint status updated.")
                st.rerun()
            except sqlite3.Error as error:
                st.error(f"Database error: {error}")

    with tab_delete:
        st.warning(
            f"You are about to permanently delete complaint ID {selected_id}. "
            "This action cannot be undone."
        )
        confirm_delete = st.checkbox("I confirm that I want to delete this complaint.")
        if st.button("Delete Complaint", type="primary", disabled=not confirm_delete):
            try:
                delete_complaint(selected_id)
                st.success("Complaint deleted successfully.")
                st.rerun()
            except sqlite3.Error as error:
                st.error(f"Database error: {error}")


# ---------------- FOOTER ----------------
st.divider()
st.caption("Digital Complaint Management System • Python + Streamlit + SQLite")
