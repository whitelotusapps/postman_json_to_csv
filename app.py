import streamlit as st
import json
import csv
import time

# Function to load data from a JSON file
@st.cache_data
def load_data_from_file(uploadfile):
    data = json.load(uploadfile)
    return data

# Function to load data from pasted JSON text
@st.cache_data
def load_data_from_text(json_text):
    data = json.loads(json_text)
    return data

# Function to export the selected data to a CSV file
def export_to_csv(data, keys, output_file):
    with open(output_file, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

# Main function containing the Streamlit application
def main():
    st.title("JSON to CSV Converter")

    # User selects input type (file or text)
    input_option = st.radio("Select input type", ("File", "Text"))

    data = None

    # If input type is file, user uploads a JSON file
    if input_option == "File":
        uploaded_file = st.file_uploader("Choose a JSON file", type='json')
        if uploaded_file is not None:
            data = load_data_from_file(uploaded_file)

    # If input type is text, user pastes JSON data into a text area
    elif input_option == "Text":
        json_text = st.text_area("Paste JSON data")
        if json_text:
            data = load_data_from_text(json_text)

    # If data is successfully loaded, process it
    if data:
        # Extract keys from the JSON data
        keys = set(next(iter(data[0].values())).keys())
        # Sort the keys alphabetically
        keys_sorted = sorted(keys)

        # User arranges the keys in the desired order
        keys_ordered = (
            st.text_area(
                "Arrange the keys (one key per line)", "\n".join(keys_sorted), height=len(keys)*25
            )
            .strip()
            .split("\n")
        )

        # Extract the ordered keys
        selected_keys_ordered = [
            key.strip() for key in keys_ordered if key.strip() in keys
        ]

        # Warn if some keys are missing from the ordered list
        if len(selected_keys_ordered) != len(keys):
            st.warning("Some keys were not found in the ordered list")

        # Create the output filename with a timestamp
        timestampStr = time.strftime("%Y-%m-%d_%H-%M-%S")
        output_file = f"JSONtoCSV_{timestampStr}.csv"

        # If user clicks the "Export to CSV" button, export the data
        if st.button("Export to CSV"):
            selected_data = []
            for item in data:
                selected_item = {
                    k: v
                    for k, v in next(iter(item.values())).items()
                    if k in selected_keys_ordered
                }
                selected_data.append(selected_item)
            if selected_data:
                export_to_csv(selected_data, selected_keys_ordered, output_file)
                st.success(f"CSV file exported successfully to {output_file}")
            else:
                st.warning("No data selected for export")

if __name__ == "__main__":
    main()
