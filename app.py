import streamlit as st
import pandas as pd
from io import BytesIO
import plotly.express as px

# Function to read the Excel file and handle different column names
@st.cache_data
def load_data(file):
    try:
        df = pd.read_excel(file)

        # Check for different possible column names for Phone Number
        phone_col = next((col for col in df.columns if col.lower() in ['phone number', 'phone', 'mobile number', 'contact']), None)

        if phone_col is None:
            st.error("Error: No valid 'Phone Number' column found in the file.")
            return None
        
        # Rename the found column to 'Phone Number' for uniformity
        df.rename(columns={phone_col: 'Phone Number'}, inplace=True)
        
        # Initialize 'Called' and 'Notes' columns if not present
        if 'Called' not in df.columns:
            df['Called'] = False
        if 'Notes' not in df.columns:
            df['Notes'] = ""

        return df

    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

# Function to display the data with checkboxes, notes, and real-time updates
def display_data_with_actions(df):
    st.write("### Manage Call Data")

    # Display the data with interactive checkboxes and notes for each row
    for index, row in df.iterrows():
        st.write(f"**Row {index + 1} - Phone Number: {row['Phone Number']}**")
        # Display call status with colored indicators
        status_color = 'green' if row['Called'] else 'red'
        st.markdown(f"<span style='color:{status_color}; font-weight:bold'>**Status: {status_color.capitalize()}**</span>", unsafe_allow_html=True)

        # Checkbox for call status
        called = st.checkbox("Called", key=f"called_{index}", value=row['Called'])
        
        # Text area for notes
        notes = st.text_area(f"Notes for {row['Phone Number']}", value=row['Notes'], key=f"notes_{index}")

        # Update the DataFrame in session state
        if called != row['Called'] or notes != row['Notes']:
            st.session_state.df.at[index, 'Called'] = called
            st.session_state.df.at[index, 'Notes'] = notes

    return st.session_state.df

# Function to filter the data
def filter_data(df, filter_option):
    if filter_option == "Show All":
        return df
    elif filter_option == "Called":
        return df[df['Called'] == True]
    else:
        return df

# Function to download the updated Excel file
def download_updated_data(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

# Function to show summary statistics
def show_summary_stats(df):
    if df.empty:
        st.write("### No data available for summary.")
        st.write("Please upload a valid Excel file with call data.")
        return

    total_calls = df['Called'].sum()
    total_records = len(df)
    to_be_called = total_records - total_calls
    
    st.write("### Summary")
    st.write(f"Total Records: {total_records}")
    st.write(f"Total Calls Made: {total_calls}")
    st.write(f"Pending Calls: {to_be_called}")

    # Prepare chart data
    chart_data = pd.DataFrame({
        'Status': ['Called', 'To be Called'],
        'Count': [total_calls, to_be_called]
    })

    # Handle the case where no data is available for pie chart
    if chart_data['Count'].sum() == 0:
        st.write("### No data to plot.")
        st.write("The dataset is empty or does not contain enough data for a meaningful chart.")
        return

    fig = px.pie(chart_data, names='Status', values='Count', title="Call Status Breakdown")
    st.plotly_chart(fig, use_container_width=True)

# Streamlit app
def main():
    st.title("Super Professional Call Management Platform")

    # Upload Excel file
    uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

    if uploaded_file is not None:
        # Display loading spinner while reading the file
        with st.spinner('Loading data...'):
            df = load_data(uploaded_file)

        if df is not None:
            # Initialize session state if not already
            if 'df' not in st.session_state:
                st.session_state.df = df

            # Sidebar navigation
            st.sidebar.title("Navigation")
            options = ["Show All", "Called"]
            choice = st.sidebar.selectbox("Select a section", options)

            # Filter data based on the selected section
            filtered_df = filter_data(st.session_state.df, choice)

            # Show filtered data with interactive checkboxes and notes
            updated_df = display_data_with_actions(filtered_df)

            # Display summary statistics and chart
            show_summary_stats(st.session_state.df)

            # Button to download the updated data
            st.write("### Download Updated Data")
            st.download_button(
                label="Download Updated Excel File",
                data=download_updated_data(st.session_state.df),
                file_name="updated_call_data.xlsx",
                mime="application/vnd.ms-excel"
            )

if __name__ == "__main__":
    main()
