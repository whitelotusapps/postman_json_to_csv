import streamlit as st
import csv
import json
import time


def export_to_csv(data, keys):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    with open(f"{timestr} - output.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)


def main():
    st.title("JSON to CSV Converter")
    json_input = st.text_area("Paste the JSON here", height=400)
    try:
        data = json.loads(json_input)
    except ValueError:
        st.error("Invalid JSON")
        return

    keys = set()
    for item in data:
        keys.update(item[list(item.keys())[0]].keys())

    selected_keys = st.multiselect(
        "Select the keys to export", list(keys), default=list(keys)
    )

    if not selected_keys:
        st.warning("No keys selected")
        return

    keys_ordered = (
        st.text_area(
            "Arrange the selected keys (one key per line)", "\n".join(selected_keys)
        )
        .strip()
        .split("\n")
    )

    selected_keys_ordered = [
        key.strip() for key in keys_ordered if key.strip() in selected_keys
    ]

    if len(selected_keys_ordered) != len(selected_keys):
        st.warning("Some selected keys were not found in the ordered list")

    if st.button("Export to CSV"):
        selected_data = []
        for item in data:
            selected_item = {
                k: v
                for k, v in item[list(item.keys())[0]].items()
                if k in selected_keys_ordered
            }
            selected_data.append(selected_item)
        if selected_data:
            export_to_csv(selected_data, selected_keys_ordered)
            st.success("CSV file exported successfully")
        else:
            st.warning("No data selected for export")


if __name__ == "__main__":
    main()
