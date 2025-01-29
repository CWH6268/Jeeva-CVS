import pandas as pd
from bs4 import BeautifulSoup
import streamlit as st
from io import StringIO

# Streamlit Title
st.title("Jeeva Table Extractor")
st.write("Paste the Jeeva HTML content below, and this app will extract the prospect table and save it as a CSV.")

# Text area for pasting HTML content
html_content = st.text_area("Paste the HTML content here:")

if html_content:
    try:
        # Parse the HTML content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Locate the table
        table = soup.find('table')

        if table:
            # Extract headers
            headers = [th.get_text(strip=True) if th.get_text(strip=True) else f"Column_{i}" 
                       for i, th in enumerate(table.find_all('th'))]

            # Ensure unique column names in case of duplicates
            seen = {}
            for i, col in enumerate(headers):
                if col in seen:
                    seen[col] += 1
                    headers[i] = f"{col}_{seen[col]}"  # Rename duplicate columns
                else:
                    seen[col] = 0

            # Extract rows
            rows = []
            for tr in table.find_all('tr'):
                cells = [td.get_text(strip=True) for td in tr.find_all('td')]
                if cells:  # Avoid empty rows
                    rows.append(cells)

            # Create DataFrame
            df = pd.DataFrame(rows, columns=headers)

            # Display the extracted table
            st.write("### Extracted Table")
            st.dataframe(df)

            # Allow user to download the CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="jeeva_table.csv",
                mime="text/csv"
            )

        else:
            st.error("No table found in the provided HTML content. Please make sure you've copied the correct section.")

    except Exception as e:
        st.error(f"An error occurred while processing the HTML content: {e}")
