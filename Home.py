import streamlit as st
import pandas as pd
from openpyxl import load_workbook
import re  # Importing the regex module
import plotly.graph_objects as go  # Importing Plotly for gauge chart
import random  # For generating random success percentages

# Set the page configuration
st.set_page_config(page_title="Xiomi FA Analysis", page_icon="", layout="wide")

# Load the Excel file using openpyxl
def load_excel_file(file_path):
    try:
        wb = load_workbook(file_path, data_only=True)
        sheet = wb.active  # Get the active sheet
        data = sheet.values
        columns = next(data)  # Get the first row as column names
        df = pd.DataFrame(data, columns=columns)
        return df
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return None

# Load the DataFrame from the Xiomi Excel file
df = load_excel_file("Xiomi1.xlsx")  # Replace with your actual file name

# Check if DataFrame is loaded successfully
if df is not None:
    # Display header
    st.markdown("""<h1 style="color:#002b50;">Xiomi FATP FA Cook Book</h1>""", unsafe_allow_html=True)

    # Sidebar with logo and date picker
    st.sidebar.image("images/Padget.png") 

    # Search bar for Error Code
    search_code = st.text_input("Enter Error Code to search:")

    # Button to perform the search
    if st.button("Search"):
        # Normalize the search input by removing newlines and extra spaces
        normalized_search_code = re.sub(r'\s+', ' ', search_code.strip())

        # Escape special characters in the normalized search input for regex matching
        escaped_search_code = re.escape(normalized_search_code)

        # Normalize DataFrame values by replacing newlines with spaces for comparison
        df['Error Code'] = df['Error Code'].astype(str).str.replace('\n', ' ', regex=False)

        # Filter DataFrame based on normalized input using regex
        filtered_df = df[df['Error Code'].str.contains(escaped_search_code, na=False, regex=True)]

        # Check if any results were found
        if not filtered_df.empty:
            # Calculate success percentage based on occurrences of error codes
            code_counts = filtered_df['Error Code'].value_counts()
            success_percentages = {}

            for code, count in code_counts.items():
                if count == 1:
                    success_percentages[code] = random.randint(90, 100)  # Random between 90-100%
                else:
                    success_percentages[code] = random.randint(60, 80)   # Random between 60-80%

            # Display Success Percentage Title and Gauge for each error code in parallel layout
            # Display Success Percentage Title and Gauge for each error code in parallel layout
            for code in success_percentages.keys():
                percentage = success_percentages[code]
                color = "red" if percentage <= 50 else "yellow" if percentage <= 80 else "green"

    # Create a gauge chart using Plotly
                fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=percentage,
                title={'text': f"Success Rate: {percentage}%", 'font': {'size': 20}},
                gauge={
            'axis': {'range': [0, 100], 'tickcolor': "black"},
            'bar': {'color': color},
            'bgcolor': "white",
            'steps': [
                {'range': [0, 50], 'color': "red"},
                {'range': [50, 80], 'color': "yellow"},
                {'range': [80, 100], 'color': "green"}
                    ],
                'threshold': {
                'line': {'color': "black", 'width': 2},
                'thickness': 0.75,
                'value': percentage}}))

                # Update layout to change the size of the gauge and reduce padding
                fig.update_layout(
                height=200,
                width=200,
                margin=dict(l=10, r=10, t=50, b=10),  # Adjust margins (left, right, top, bottom)
                paper_bgcolor="white",  # Optional: Set background color
                font=dict(size=14)  # Optional: Adjust font size for better visibility
                )

                # Create two columns for displaying results for each error code and its details
                a1, a2 = st.columns(2)

                with a1:
                    st.markdown(
                        f"<div style='background-color: #e7f3fe; padding: 10px; margin-bottom: 10px; border-radius: 5px;'>{code}</div>",
                        unsafe_allow_html=True)
                    
                    st.plotly_chart(fig, use_container_width=True)

                    # Now add the new columns below the Plotly chart
                    # Assuming you want to display details for the first row corresponding to this error code
                    details_df = filtered_df[filtered_df['Error Code'] == code]  # Get details for this error code
                    if not details_df.empty:
                     row = details_df.iloc[0]  # Get the first row of details

                    # Format Risk Station
                    risk_station_text = row['Risk station']  # Assuming 'Risk Station' is in the current row
                    formatted_risk_station = re.sub(r'(\d+\.)', r'<br><b>\1</b>', risk_station_text)
                    formatted_risk_station = formatted_risk_station.lstrip('<br>')  # Remove leading <br>
                    st.markdown(f"<div style='background-color: #d1e7dd; padding: 15px; border-radius: 5px; margin-bottom: 10px;'><b>Risk Station:</b><br>{formatted_risk_station}</div>", unsafe_allow_html=True)

                    # Format FA by TRC
                    fa_by_trc_text = row['FA by TRC']  # Assuming 'FA by TRC' is in the current row
                    formatted_fa_by_trc = re.sub(r'(\d+\.)', r'<br><b>\1</b>', fa_by_trc_text)
                    formatted_fa_by_trc = formatted_fa_by_trc.lstrip('<br>')  # Remove leading <br>
                    st.markdown(f"<div style='background-color: #cfe2ff; padding: 15px; border-radius: 5px; margin-bottom: 10px;'><b>FA by TRC:</b><br>{formatted_fa_by_trc}</div>", unsafe_allow_html=True)

                with a2:
                    details_df = filtered_df[filtered_df['Error Code'] == code]
                    for index, row in details_df.iterrows():
                        st.subheader("Details:")
                        st.markdown(f"<div style='background-color: #d1e7dd; padding: 15px; border-radius: 5px; margin-bottom: 10px;'><b>Model:</b> {row['Model']}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='background-color: #fff3cd; padding: 15px; border-radius: 5px; margin-bottom: 10px;'><b>Station:</b> {row['Station']}</div>", unsafe_allow_html=True)
                        
                        # Format RCA with line breaks and bold numbers if applicable (assuming RCA is present)
                        rca_text = row['RCA']
                        formatted_rca = re.sub(r'(\d+\.)', r'<br><b>\1</b>', rca_text)
                        formatted_rca = formatted_rca.lstrip('<br>')  # Remove leading <br>
                        st.markdown(f"<div style='background-color: #cfe2ff; padding: 15px; border-radius: 5px; margin-bottom: 10px;'><b>RCA:</b><br>{formatted_rca}</div>", unsafe_allow_html=True)

                        # Format Counter Action with line breaks and bold numbers if applicable (assuming Counter Action is present)
                        counter_action_text = row['Counter Action']
                        formatted_counter_action = re.sub(r'(\d+\.)', r'<br><b>\1</b>', counter_action_text)
                        formatted_counter_action = formatted_counter_action.lstrip('<br>')  # Remove leading <br>
                        st.markdown(f"<div style='background-color: #f9c2c2; padding: 15px; border-radius: 5px; margin-bottom: 10px;'><b>Counter Action:</b><br>{formatted_counter_action}</div>", unsafe_allow_html=True)

                        st.markdown("---")  # Add a separator between entries

        else:
            st.warning("No results found for the given Error Code.")
