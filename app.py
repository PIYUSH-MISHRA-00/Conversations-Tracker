import streamlit as st
import pandas as pd
import sqlite3

# Database setup
def init_db():
    conn = sqlite3.connect('call_tracker.db')
    cursor = conn.cursor()
    # Create table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS business_calls (
            id INTEGER PRIMARY KEY,
            business_name TEXT,
            phone_number TEXT,
            call_status TEXT DEFAULT 'To Call',
            notes TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_data(df):
    conn = sqlite3.connect('call_tracker.db')
    cursor = conn.cursor()

    # Check if necessary columns are present
    if 'business name' not in df.columns or 'phone number' not in df.columns:
        st.error("Error: Columns 'business name' or 'phone number' not found in the uploaded file.")
        return

    # Insert rows into the database
    for i, row in df.iterrows():
        cursor.execute('''
            INSERT INTO business_calls (business_name, phone_number, call_status, notes)
            VALUES (?, ?, ?, ?)
        ''', (row['business name'], row['phone number'], 'To Call', ''))
    
    conn.commit()
    conn.close()

def get_data():
    conn = sqlite3.connect('call_tracker.db')
    df = pd.read_sql_query('SELECT * FROM business_calls', conn)
    conn.close()
    return df

def update_call_status(business_id, status, notes):
    conn = sqlite3.connect('call_tracker.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE business_calls 
        SET call_status = ?, notes = ?
        WHERE id = ?
    ''', (status, notes, business_id))
    conn.commit()
    conn.close()

# Step 1: Initialize the database
init_db()

# Title of the App
st.title('Business Call Tracker')

# Step 2: Upload Excel file
uploaded_file = st.file_uploader("Upload an Excel file to populate the database", type=['xlsx'])
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    
    # Debugging: Display the column names to inspect them
    st.write("Column names in the uploaded file:", df.columns)
    
    # Standardize column names (lowercase and strip whitespaces)
    df.columns = df.columns.str.strip().str.lower()
    
    # Debugging: Show the first few rows of the DataFrame
    st.write("Data in the uploaded file:", df.head())
    
    # Insert the data into the database
    insert_data(df)
    st.success('Data uploaded and saved to database!')

# Step 3: Filter/Search Functionality
st.subheader("Search and Filter Businesses")

search_term = st.text_input("Search by Business Name")
filter_status = st.selectbox("Filter by Call Status", ["All", "To Call", "Called"])

df = get_data()

if search_term:
    df = df[df['business_name'].str.contains(search_term, case=False)]

if filter_status != "All":
    df = df[df['call_status'] == filter_status]

# Display data in a scrollable format
st.dataframe(df[['business_name', 'phone_number', 'call_status', 'notes']], height=400)

# Step 4: Analytics Section
st.subheader("Analytics")
total_businesses = len(df)
called = len(df[df['call_status'] == 'Called'])
to_call = len(df[df['call_status'] == 'To Call'])

st.write(f"**Total Businesses:** {total_businesses}")
st.write(f"**Called:** {called}")
st.write(f"**To Call:** {to_call}")

# Step 5: Track Call Status and Notes
st.subheader('Update Call Status and Notes')

for i, row in df.iterrows():
    st.write(f"**Business: {row['business_name']}**, Phone: {row['phone_number']}")

    # Call Status selection
    status = st.selectbox(f"Call Status for {row['business_name']}", 
                          ['To Call', 'Called'], 
                          index=0 if row['call_status'] == 'To Call' else 1, 
                          key=f"status_{i}")
    
    # Notes input
    note = st.text_area(f"Notes for {row['business_name']}", row['notes'], key=f"note_{i}")

    # Save button for each business
    if st.button(f'Save for {row["business_name"]}', key=f"save_{i}"):
        update_call_status(row['id'], status, note)
        st.success(f'Status and notes updated for {row["business_name"]}')

# Step 6: Option to Download the Updated Data as Excel
st.subheader('Download the Updated Data')

if st.button("Download Updated Excel"):
    df = get_data()  # Fetch updated data
    df.to_excel('updated_progress.xlsx', index=False)
    with open('updated_progress.xlsx', 'rb') as file:
        st.download_button(
            label="Download Updated Excel",
            data=file,
            file_name='progress_updated.xlsx',
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
