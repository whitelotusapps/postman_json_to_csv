# Import the necessary libraries
import streamlit as st
import json
import csv
import time

# Use the Streamlit cache to speed up repeated loading of the same file
@st.cache_data
def load_data_from_file(uploadfile):
    # Load the JSON data from the file
    data = json.load(uploadfile)
    return data

# Use the Streamlit cache to speed up repeated parsing of the same text
@st.cache_data
def load_data_from_text(json_text):
    # Load the JSON data from the text
    data = json.loads(json_text)
    return data

# Function to export the selected data to a CSV file
def export_to_csv(data, keys, output_file):
    with open(output_file, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

def main():
    st.title("JSON to CSV Converter")

    # Let the user choose whether to input a file or text
    input_option = st.radio("Select input type", ("File", "Text"))

    data = None

    # Handle the file input option
    if input_option == "File":
        uploaded_file = st.file_uploader("Choose a JSON file", type='json')
        if uploaded_file is not None:
            data = load_data_from_file(uploaded_file)

    # Handle the text input option
    elif input_option == "Text":
        json_text = st.text_area("Paste JSON data")
        if json_text:
            data = load_data_from_text(json_text)

    if data:
        # Get the keys from the first item in the data
        keys = set(next(iter(data[0].values())).keys())

        # Let the user arrange the keys
        keys_ordered = (
            st.text_area(
                "Arrange the keys (one key per line)", "\n".join(keys), height=len(keys)*25
            )
            .strip()
            .split("\n")
        )

        # Only keep the keys that the user entered
        selected_keys_ordered = [
            key.strip() for key in keys_ordered if key.strip() in keys
        ]

        if len(selected_keys_ordered) != len(keys):
            st.warning("Some keys were not found in the ordered list")

        # Create a timestamp for the filename
        timestampStr = time.strftime("%Y-%m-%d_%H-%M-%S")
        output_file = f"JSONtoCSV_{timestampStr}.csv"

        # Handle the export to CSV button
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
