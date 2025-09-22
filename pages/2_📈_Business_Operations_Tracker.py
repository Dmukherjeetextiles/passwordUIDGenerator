import streamlit as st
import pandas as pd
import altair as alt
from datetime import date
from utils import check_authentication, load_data, save_data, OPERATIONS_FILE

st.set_page_config(page_title="Business Operations Tracker", page_icon="📈", layout="wide")
key = check_authentication()

st.title("📈 Business Operations Tracker")
st.write("A centralized dashboard to track real-time updates across different business functions.")

# --- Data Loading ---
OPERATIONS_COLUMNS = ["ID", "Category", "Update", "Status", "Priority", "Date Logged"]
df_ops = load_data(OPERATIONS_FILE, key, OPERATIONS_COLUMNS)
if df_ops is not None and not df_ops.empty:
    df_ops['Date Logged'] = pd.to_datetime(df_ops['Date Logged'])

# --- Input Form ---
st.header("Log a New Update")
categories = [
    "Lead Contacted", "Client Payment Received", "Client Feedback", "Software Update", 
    "App Update", "Digital Marketing Update", "Operations Update", "Custom"
]

with st.form("add_update_form", clear_on_submit=True):
    category_selection = st.selectbox("Category", categories)
    custom_category = ""
    if category_selection == "Custom":
        custom_category = st.text_input("Enter Custom Category Name")
    update_description = st.text_area("Update Description")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"], index=1)
    submitted = st.form_submit_button("Submit")

    if submitted and update_description:
        final_category = custom_category if category_selection == "Custom" and custom_category else category_selection
        if final_category == "Custom":
            st.warning("Please enter a name for the custom category.")
        else:
            if df_ops is None or df_ops.empty:
                new_id_num = 1001
            else:
                numeric_ids = pd.to_numeric(df_ops['ID'].str.replace('UPDATE-', ''), errors='coerce').dropna()
                new_id_num = 1001 if numeric_ids.empty else int(numeric_ids.max()) + 1

            new_update = pd.DataFrame([{
                "ID": f"UPDATE-{new_id_num}",
                "Category": final_category,
                "Update": update_description,
                "Status": "Not Started",
                "Priority": priority,
                "Date Logged": pd.to_datetime(date.today()),
            }])
            df_ops = pd.concat([new_update, df_ops], ignore_index=True)
            save_data(df_ops, OPERATIONS_FILE, key)
            st.success("Update logged successfully!")
            st.rerun()

# --- Activity Log & Dashboard ---
if df_ops is None or df_ops.empty:
    st.info("No updates logged yet. Use the form above to get started.")
else:
    st.header("Activity Log")
    edited_df = st.data_editor(
        df_ops,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Status": st.column_config.SelectboxColumn("Status", options=["Not Started", "In Progress", "Completed", "On Hold"], required=True),
            "Priority": st.column_config.SelectboxColumn("Priority", options=["High", "Medium", "Low"], required=True),
            "ID": st.column_config.TextColumn("ID", disabled=True),
            "Category": st.column_config.TextColumn("Category", disabled=True),
        },
    )
    if not df_ops.equals(edited_df):
        save_data(edited_df, OPERATIONS_FILE, key)
        st.success("Changes saved!")
        st.rerun()

    st.header("Dashboard")
    col1, col2, col3 = st.columns(3)
    col1.metric("Completed", len(df_ops[df_ops["Status"] == "Completed"]))
    col2.metric("In Progress", len(df_ops[df_ops["Status"] == "In Progress"]))
    col3.metric("Not Started", len(df_ops[df_ops["Status"] == "Not Started"]))

    st.divider()
    
    category_chart = alt.Chart(df_ops).mark_bar().encode(
        x=alt.X("Category:N", sort='-y', title="Category"),
        y=alt.Y("count():Q", title="Number of Updates"),
    ).properties(height=350)
    st.altair_chart(category_chart, use_container_width=True)