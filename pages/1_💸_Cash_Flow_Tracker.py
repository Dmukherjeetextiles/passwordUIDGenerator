import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
from utils import check_authentication, load_data, save_data, CASHFLOW_FILE

st.set_page_config(page_title="Cash Flow Tracker", page_icon="💸", layout="wide")
key = check_authentication()

st.title("💸 Cash Flow Tracker")
st.write("Log your income and expenses to visualize your financial health.")

# --- Data Loading ---
CASHFLOW_COLUMNS = ["Date", "Description", "Type", "Amount"]
df_cash = load_data(CASHFLOW_FILE, key, CASHFLOW_COLUMNS)
if df_cash is not None and not df_cash.empty:
    df_cash['Date'] = pd.to_datetime(df_cash['Date'])

# --- Input Form ---
with st.form("cash_flow_form", clear_on_submit=True):
    st.header("Add New Transaction")
    col1, col2, col3 = st.columns(3)
    with col1:
        date = st.date_input("Date", datetime.now())
    with col2:
        trans_type = st.selectbox("Type", ["Income", "Expense"])
    with col3:
        amount = st.number_input("Amount", min_value=0.01, step=0.01)
    
    description = st.text_input("Description")
    submitted = st.form_submit_button("Add Transaction")

    if submitted and description:
        new_entry = pd.DataFrame([{
            "Date": pd.to_datetime(date),
            "Description": description,
            "Type": trans_type,
            "Amount": amount
        }])
        df_cash = pd.concat([df_cash, new_entry], ignore_index=True)
        save_data(df_cash, CASHFLOW_FILE, key)
        st.success("Transaction added successfully!")
        st.rerun()

# --- Dashboard ---
st.header("Dashboard")
if df_cash is None or df_cash.empty:
    st.info("No transactions logged yet. Add a transaction to see your dashboard.")
else:
    # --- Metrics ---
    total_income = df_cash[df_cash['Type'] == 'Income']['Amount'].sum()
    total_expense = df_cash[df_cash['Type'] == 'Expense']['Amount'].sum()
    net_flow = total_income - total_expense

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"${total_income:,.2f}")
    col2.metric("Total Expense", f"${total_expense:,.2f}")
    col3.metric("Net Cash Flow", f"${net_flow:,.2f}", delta=f"{net_flow:,.2f}")

    st.divider()

    # --- Charts ---
    df_chart = df_cash.copy()
    df_chart['Flow'] = df_chart.apply(lambda row: row['Amount'] if row['Type'] == 'Income' else -row['Amount'], axis=1)

    st.write("##### Monthly Cash Flow")
    monthly_chart = alt.Chart(df_chart).mark_bar().encode(
        x=alt.X('yearmonth(Date):T', title='Month'),
        y=alt.Y('sum(Flow):Q', title='Net Flow ($)'),
        color=alt.condition(
            'sum(Flow) > 0',
            alt.value('seagreen'), # The positive color
            alt.value('tomato')   # The negative color
        )
    ).properties(height=350)
    st.altair_chart(monthly_chart, use_container_width=True)

    # --- Data Table ---
    st.write("##### Recent Transactions")
    st.dataframe(df_cash.sort_values("Date", ascending=False), use_container_width=True, hide_index=True)