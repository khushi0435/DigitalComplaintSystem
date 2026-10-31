import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import date
import os

# ---------------- DATABASE ----------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "complaints_new.db")

conn = sqlite3.connect(DB_NAME, timeout=10)
conn.execute("PRAGMA busy_timeout = 10000")
cursor = conn.cursor()

cursor.execute("""
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

# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("Digital Complaint Management System")
root.geometry("1150x750")
root.minsize(1000, 650)
root.configure(bg="#f1f5f9")

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background="white",
    foreground="#1e293b",
    rowheight=30,
    fieldbackground="white",
    font=("Arial", 10)
)

style.configure(
    "Treeview.Heading",
    background="#e2e8f0",
    foreground="#1e293b",
    font=("Arial", 10, "bold")
)

style.map(
    "Treeview",
    background=[("selected", "#bfdbfe")]
)

# ---------------- HEADER ----------------

header = tk.Frame(root, bg="#172554", height=85)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="DCMS | Complaint Management",
    font=("Arial", 21, "bold"),
    bg="#172554",
    fg="white"
).pack(anchor="w", padx=25, pady=(15, 0))

tk.Label(
    header,
    text="Digital Complaint Management System",
    font=("Arial", 10),
    bg="#172554",
    fg="#cbd5e1"
).pack(anchor="w", padx=27)

# ---------------- DASHBOARD CARDS ----------------

stats_frame = tk.Frame(root, bg="#f1f5f9")
stats_frame.pack(fill="x", padx=20, pady=15)


def create_card(parent, title, color):
    card = tk.Frame(
        parent,
        bg="white",
        padx=18,
        pady=12,
        highlightbackground="#e2e8f0",
        highlightthickness=1
    )

    card.pack(
        side="left",
        fill="x",
        expand=True,
        padx=6
    )

    tk.Label(
        card,
        text=title,
        bg="white",
        fg="#64748b",
        font=("Arial", 10)
    ).pack(anchor="w")

    value = tk.Label(
        card,
        text="0",
        bg="white",
        fg=color,
        font=("Arial", 22, "bold")
    )

    value.pack(anchor="w", pady=(5, 0))

    return value


total_value = create_card(
    stats_frame,
    "TOTAL COMPLAINTS",
    "#1d4ed8"
)

pending_value = create_card(
    stats_frame,
    "PENDING",
    "#d97706"
)

progress_value = create_card(
    stats_frame,
    "IN PROGRESS",
    "#7c3aed"
)

resolved_value = create_card(
    stats_frame,
    "RESOLVED",
    "#15803d"
)

# ---------------- CONTENT AREA ----------------

content = tk.Frame(root, bg="#f1f5f9")

content.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=(0, 10)
)

# ---------------- COMPLAINT FORM ----------------

form = tk.LabelFrame(
    content,
    text="  Submit New Complaint  ",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#172554",
    padx=12,
    pady=10
)

form.pack(fill="x", pady=(0, 12))

tk.Label(
    form,
    text="Student Name",
    bg="white"
).grid(
    row=0,
    column=0,
    sticky="w",
    padx=5,
    pady=5
)

name_entry = ttk.Entry(form, width=27)

name_entry.grid(
    row=1,
    column=0,
    sticky="ew",
    padx=5,
    pady=3
)

tk.Label(
    form,
    text="Category",
    bg="white"
).grid(
    row=0,
    column=1,
    sticky="w",
    padx=5,
    pady=5
)

category_box = ttk.Combobox(
    form,
    values=[
        "Academic",
        "Infrastructure",
        "Hostel",
        "Transport",
        "Fees",
        "Other"
    ],
    state="readonly",
    width=24
)

category_box.grid(
    row=1,
    column=1,
    sticky="ew",
    padx=5,
    pady=3
)

category_box.set("Academic")

tk.Label(
    form,
    text="Complaint Description",
    bg="white"
).grid(
    row=0,
    column=2,
    sticky="w",
    padx=5,
    pady=5
)

description_entry = ttk.Entry(form, width=42)

description_entry.grid(
    row=1,
    column=2,
    sticky="ew",
    padx=5,
    pady=3
)

form.columnconfigure(0, weight=1)
form.columnconfigure(1, weight=1)
form.columnconfigure(2, weight=2)

# ---------------- SEARCH AND FILTER ----------------

filter_frame = tk.Frame(content, bg="#f1f5f9")
filter_frame.pack(fill="x", pady=(0, 8))

tk.Label(
    filter_frame,
    text="Search:",
    bg="#f1f5f9",
    font=("Arial", 10, "bold")
).pack(side="left", padx=(0, 7))

search_entry = ttk.Entry(filter_frame, width=32)

search_entry.pack(
    side="left",
    padx=(0, 12)
)

tk.Label(
    filter_frame,
    text="Status:",
    bg="#f1f5f9"
).pack(
    side="left",
    padx=(0, 7)
)

status_filter = ttk.Combobox(
    filter_frame,
    values=[
        "All",
        "Pending",
        "In Progress",
        "Resolved"
    ],
    state="readonly",
    width=16
)

status_filter.set("All")

status_filter.pack(
    side="left",
    padx=(0, 10)
)

# ---------------- COMPLAINT TABLE ----------------

table_frame = tk.Frame(content, bg="white")
table_frame.pack(fill="both", expand=True)

columns = (
    "ID",
    "Name",
    "Category",
    "Description",
    "Date",
    "Status"
)

table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    selectmode="browse"
)

widths = {
    "ID": 55,
    "Name": 140,
    "Category": 125,
    "Description": 300,
    "Date": 110,
    "Status": 120
}

for col in columns:
    table.heading(col, text=col)

    table.column(
        col,
        width=widths[col],
        anchor="w"
    )

table.column("ID", anchor="center")

scrollbar_y = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=table.yview
)

scrollbar_x = ttk.Scrollbar(
    table_frame,
    orient="horizontal",
    command=table.xview
)

table.configure(
    yscrollcommand=scrollbar_y.set,
    xscrollcommand=scrollbar_x.set
)

table.grid(
    row=0,
    column=0,
    sticky="nsew"
)

scrollbar_y.grid(
    row=0,
    column=1,
    sticky="ns"
)

scrollbar_x.grid(
    row=1,
    column=0,
    sticky="ew"
)

table_frame.rowconfigure(0, weight=1)
table_frame.columnconfigure(0, weight=1)

# ---------------- DASHBOARD REFRESH ----------------

def refresh_dashboard():
    cursor.execute("SELECT COUNT(*) FROM complaints")

    total_value.config(
        text=str(cursor.fetchone()[0])
    )

    for status, label in [
        ("Pending", pending_value),
        ("In Progress", progress_value),
        ("Resolved", resolved_value)
    ]:
        cursor.execute(
            "SELECT COUNT(*) FROM complaints WHERE status = ?",
            (status,)
        )

        label.config(
            text=str(cursor.fetchone()[0])
        )


# ---------------- REFRESH TABLE ----------------

def refresh_table():
    for item in table.get_children():
        table.delete(item)

    keyword = search_entry.get().strip().lower()
    selected_status = status_filter.get()

    try:
        cursor.execute(
            "SELECT * FROM complaints ORDER BY id DESC"
        )

        records = cursor.fetchall()

        for row in records:
            searchable_text = " ".join(
                str(value) for value in row
            ).lower()

            if keyword and keyword not in searchable_text:
                continue

            if (
                selected_status != "All"
                and row[5] != selected_status
            ):
                continue

            table.insert(
                "",
                "end",
                values=row
            )

        refresh_dashboard()

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            str(error)
        )


# ---------------- CREATE: ADD COMPLAINT ----------------

def add_complaint():
    name = name_entry.get().strip()
    category = category_box.get()
    description = description_entry.get().strip()

    if not name or not category or not description:
        messagebox.showwarning(
            "Validation Error",
            "Please fill in all complaint details."
        )
        return

    try:
        cursor.execute("""
            INSERT INTO complaints
            (name, category, description, date, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            category,
            description,
            date.today().isoformat(),
            "Pending"
        ))

        conn.commit()

        name_entry.delete(0, "end")
        description_entry.delete(0, "end")
        category_box.set("Academic")

        search_entry.delete(0, "end")
        status_filter.set("All")

        refresh_table()

        messagebox.showinfo(
            "Success",
            "Complaint submitted successfully!"
        )

    except sqlite3.Error as error:
        conn.rollback()

        messagebox.showerror(
            "Database Error",
            str(error)
        )


# ---------------- SELECTED COMPLAINT ----------------

def get_selected_id():
    selected = table.selection()

    if not selected:
        messagebox.showwarning(
            "No Selection",
            "Please select a complaint from the table."
        )
        return None

    return table.item(
        selected[0],
        "values"
    )[0]


# ---------------- UPDATE: EDIT COMPLAINT ----------------

def edit_complaint():
    complaint_id = get_selected_id()

    if complaint_id is None:
        return

    try:
        cursor.execute(
            "SELECT * FROM complaints WHERE id = ?",
            (complaint_id,)
        )

        record = cursor.fetchone()

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            str(error)
        )
        return

    if record is None:
        messagebox.showerror(
            "Error",
            "Complaint record not found."
        )

        refresh_table()
        return

    window = tk.Toplevel(root)
    window.title("Edit Complaint")
    window.geometry("430x330")
    window.configure(bg="white")
    window.transient(root)
    window.grab_set()

    tk.Label(
        window,
        text="Edit Complaint Details",
        font=("Arial", 15, "bold"),
        bg="white"
    ).pack(pady=12)

    tk.Label(
        window,
        text="Student Name",
        bg="white"
    ).pack()

    edit_name = ttk.Entry(window, width=42)
    edit_name.pack(pady=5)
    edit_name.insert(0, record[1])

    tk.Label(
        window,
        text="Category",
        bg="white"
    ).pack()

    edit_category = ttk.Combobox(
        window,
        values=[
            "Academic",
            "Infrastructure",
            "Hostel",
            "Transport",
            "Fees",
            "Other"
        ],
        state="readonly",
        width=39
    )

    edit_category.pack(pady=5)
    edit_category.set(record[2])

    tk.Label(
        window,
        text="Description",
        bg="white"
    ).pack()

    edit_description = ttk.Entry(window, width=42)
    edit_description.pack(pady=5)
    edit_description.insert(0, record[3])

    def save_changes():
        name = edit_name.get().strip()
        category = edit_category.get()
        description = edit_description.get().strip()

        if not name or not category or not description:
            messagebox.showwarning(
                "Validation Error",
                "All fields are required.",
                parent=window
            )
            return

        try:
            cursor.execute("""
                UPDATE complaints
                SET name = ?, category = ?, description = ?
                WHERE id = ?
            """, (
                name,
                category,
                description,
                complaint_id
            ))

            conn.commit()

            window.destroy()
            refresh_table()

            messagebox.showinfo(
                "Success",
                "Complaint updated."
            )

        except sqlite3.Error as error:
            conn.rollback()

            messagebox.showerror(
                "Database Error",
                str(error),
                parent=window
            )

    ttk.Button(
        window,
        text="Save Changes",
        command=save_changes
    ).pack(pady=12)


# ---------------- UPDATE: STATUS ----------------

def update_status():
    complaint_id = get_selected_id()

    if complaint_id is None:
        return

    try:
        cursor.execute(
            "SELECT status FROM complaints WHERE id = ?",
            (complaint_id,)
        )

        record = cursor.fetchone()

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            str(error)
        )
        return

    if record is None:
        messagebox.showerror(
            "Error",
            "Complaint record not found."
        )
        refresh_table()
        return

    window = tk.Toplevel(root)
    window.title("Update Status")
    window.geometry("320x180")
    window.configure(bg="white")
    window.transient(root)
    window.grab_set()

    tk.Label(
        window,
        text="Update Complaint Status",
        font=("Arial", 13, "bold"),
        bg="white"
    ).pack(pady=15)

    status_box = ttk.Combobox(
        window,
        values=[
            "Pending",
            "In Progress",
            "Resolved"
        ],
        state="readonly",
        width=22
    )

    status_box.pack(pady=5)
    status_box.set(record[0])

    def save_status():
        new_status = status_box.get()

        if new_status not in [
            "Pending",
            "In Progress",
            "Resolved"
        ]:
            messagebox.showwarning(
                "Validation Error",
                "Please select a valid status.",
                parent=window
            )
            return

        try:
            cursor.execute(
                "UPDATE complaints SET status = ? WHERE id = ?",
                (new_status, complaint_id)
            )

            conn.commit()

            window.destroy()
            refresh_table()

        except sqlite3.Error as error:
            conn.rollback()

            messagebox.showerror(
                "Database Error",
                str(error),
                parent=window
            )

    ttk.Button(
        window,
        text="Save Status",
        command=save_status
    ).pack(pady=12)


# ---------------- DELETE: REMOVE COMPLAINT ----------------

def delete_complaint():
    complaint_id = get_selected_id()

    if complaint_id is None:
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Delete complaint ID {complaint_id} permanently?"
    )

    if not confirm:
        return

    try:
        cursor.execute(
            "DELETE FROM complaints WHERE id = ?",
            (complaint_id,)
        )

        conn.commit()

        refresh_table()

        messagebox.showinfo(
            "Deleted",
            "Complaint deleted successfully."
        )

    except sqlite3.Error as error:
        conn.rollback()

        messagebox.showerror(
            "Database Error",
            str(error)
        )


# ---------------- RESET SEARCH AND FILTER ----------------

def reset_filters():
    search_entry.delete(0, "end")
    status_filter.set("All")
    refresh_table()


# ---------------- BUTTONS ----------------

ttk.Button(
    filter_frame,
    text="Search / Filter",
    command=refresh_table
).pack(
    side="left",
    padx=5
)

ttk.Button(
    filter_frame,
    text="Reset",
    command=reset_filters
).pack(
    side="left",
    padx=5
)

# ---------------- ACTION BUTTONS ----------------

actions = tk.Frame(root, bg="#f1f5f9")

actions.pack(
    fill="x",
    padx=20,
    pady=(0, 15)
)

tk.Button(
    actions,
    text="Submit Complaint",
    command=add_complaint,
    bg="#15803d",
    fg="white",
    activebackground="#166534",
    font=("Arial", 10, "bold"),
    padx=12,
    pady=8,
    relief="flat"
).pack(
    side="left",
    padx=(0, 8)
)

tk.Button(
    actions,
    text="Edit Complaint",
    command=edit_complaint,
    bg="#1d4ed8",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=12,
    pady=8,
    relief="flat"
).pack(
    side="left",
    padx=8
)

tk.Button(
    actions,
    text="Update Status",
    command=update_status,
    bg="#7c3aed",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=12,
    pady=8,
    relief="flat"
).pack(
    side="left",
    padx=8
)

tk.Button(
    actions,
    text="Delete Complaint",
    command=delete_complaint,
    bg="#b91c1c",
    fg="white",
    font=("Arial", 10, "bold"),
    padx=12,
    pady=8,
    relief="flat"
).pack(
    side="left",
    padx=8
)

tk.Button(
    actions,
    text="Refresh",
    command=refresh_table,
    padx=12,
    pady=8
).pack(
    side="right",
    padx=5
)

# ---------------- CLOSE APPLICATION ----------------

def close_application():
    if messagebox.askyesno(
        "Exit",
        "Do you want to close the application?"
    ):
        try:
            conn.close()
        finally:
            root.destroy()


root.protocol(
    "WM_DELETE_WINDOW",
    close_application
)

# ---------------- START APPLICATION ----------------

refresh_table()
root.mainloop()
