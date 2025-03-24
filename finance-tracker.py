import streamlit as st
import mysql.connector
import pandas as pd
import time

# Function to create database connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # Default XAMPP user
        password="",  # Default XAMPP password (empty)
        database="finance_tracker"
    )

# Function to add a transaction
def add_transaction(date, category, type_, amount, description):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO transactions (date, category, type, amount, description) VALUES (%s, %s, %s, %s, %s)"
    values = (date, category, type_, amount, description)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

# Function to fetch transactions
def fetch_transactions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, date, category, type, amount, description FROM transactions ORDER BY date DESC")
    transactions = cursor.fetchall()
    conn.close()
    return transactions

# Function to delete a transaction
def delete_transaction(transaction_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE id = %s", (transaction_id,))
    conn.commit()
    cursor.close()
    conn.close()

# ✅ Initialize session state variables if they don't exist
if "date" not in st.session_state:
    st.session_state.date = None
if "category" not in st.session_state:
    st.session_state.category = "Food"
if "type" not in st.session_state:
    st.session_state.type = "Income"
if "amount" not in st.session_state:
    st.session_state.amount = 0.0
if "description" not in st.session_state:
    st.session_state.description = ""

# UI for Personal Finance Tracker
st.title("💰 Personal Finance Tracker")

# Input fields for transactions
date = st.date_input("📅 Date", value=st.session_state.date)
category = st.selectbox("📂 Category", ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Salary", "Others"], index=0)
type_ = st.radio("💸 Type", ["Income", "Expense"])
amount = st.number_input("💰 Amount", min_value=0.0, format="%.2f")
description = st.text_area("📝 Description")

if st.button("➕ Add Transaction"):
    add_transaction(date, category, type_, amount, description)
    st.success("✅ Transaction Added!")
    
    # Wait for 1 second before refreshing
    time.sleep(1)
    
    # ✅ Reset session state to clear inputs
    st.session_state.date = None
    st.session_state.category = "Food"
    st.session_state.type = "Income"
    st.session_state.amount = 0.0
    st.session_state.description = ""
    
    # ✅ Force rerun of the script to refresh the page
    st.rerun()

# Display transactions
st.subheader("📜 Transaction History")
transactions = fetch_transactions()

if transactions:
    for transaction in transactions:
        transaction_id, date, category, type_, amount, description = transaction
        with st.expander(f"📅 {date} | {category} | {type_} | ₹{amount}"):
            st.write(f"**Description:** {description}")
            if st.button(f"🗑️ Delete", key=f"delete_{transaction_id}"):
                delete_transaction(transaction_id)
                st.warning("⚠️ Transaction Deleted!")
                time.sleep(1)
                st.rerun()
else:
    st.write("⚠️ No transactions found.")
