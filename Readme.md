![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

## Link to the Project :- [Link]()

# Conversations-Tracker :  Super Professional Call Management Platform

## Overview

The Super Professional Call Management Platform is a web application designed to help manage and track phone call data efficiently. Built using Streamlit, Pandas, and Plotly, this application allows users to upload an Excel file with phone call data, manage call statuses, add notes, and visualize call statistics through interactive charts.

## Features

- **Upload and Manage Data**: Upload an Excel file containing phone call data. The application automatically detects and renames columns for consistency.
- **Interactive Data Management**: View and update call statuses and notes for each entry with real-time updates.
- **Filter Data**: Easily switch between viewing all records or filtering to show only the calls marked as 'Called'.
- **Summary Statistics**: View summary statistics including total records, calls made, and pending calls.
- **Visual Analytics**: Interactive pie chart to visualize the breakdown of call statuses.
- **Download Updated Data**: Save and download the updated data in Excel format.

## Technologies

- **Streamlit**: For building the web application and providing an interactive user interface.
- **Pandas**: For data manipulation and handling Excel file operations.
- **Plotly**: For creating interactive charts and visualizations.
- **XlsxWriter**: For writing Excel files.

## Installation

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    ```

2. **Create and Activate a Virtual Environment (Optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Application:**

    ```bash
    streamlit run app.py
    ```

2. **Upload Excel File:**
   - Navigate to the web application in your browser.
   - Use the file uploader to upload an Excel file with phone call data.

3. **Manage Data:**
   - Use checkboxes to mark calls as 'Called'.
   - Add or update notes for each phone number.
   - Use the filter options to view specific records.

4. **View Statistics and Download Updated Data:**
   - View summary statistics and an interactive pie chart.
   - Download the updated data by clicking the download button.

## File Structure

- `app.py`: Main application script containing the Streamlit code.
- `requirements.txt`: List of Python dependencies for the project.

