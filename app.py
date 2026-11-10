import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime

from wifi_scanner import scan_wifi
from signal_analyzer import analyze_networks
from heatmap import create_heatmap


BASE_DIR = Path(__file__).parent
DATASET_PATH = BASE_DIR / "dataset.csv"

st.set_page_config(
    page_title="Wi-Fi Dead Zone Mapper",
    page_icon="📡",
    layout="wide"
)

st.title("📡 Wi-Fi Dead Zone & Spatial RF Signal Strength Mapper")

st.write(
    "Scan nearby Wi-Fi networks, compare signal strength, "
    "and map measurements collected at different locations."
)

st.info(
    "Windows Wi-Fi scanning reports signal percentage. "
    "For the spatial heatmap, record actual signal measurements in dBm."
)

# Initialize dataset.
if not DATASET_PATH.exists():
    pd.DataFrame(
        columns=[
            "Location",
            "X",
            "Y",
            "SSID",
            "Signal (dBm)",
            "Timestamp"
        ]
    ).to_csv(DATASET_PATH, index=False)


# Wi-Fi scanning section.
st.header("1. Scan Nearby Wi-Fi Networks")

if st.button("🔍 Scan Wi-Fi"):
    with st.spinner("Scanning available networks..."):
        networks, error = scan_wifi()

    if error:
        st.warning(error)

    else:
        analyzed = analyze_networks(networks)
        st.session_state["networks"] = analyzed


if "networks" in st.session_state:
    networks_df = pd.DataFrame(st.session_state["networks"])

    st.dataframe(
        networks_df,
        use_container_width=True,
        hide_index=True
    )

    best_network = networks_df.loc[
        networks_df["Signal (%)"].idxmax()
    ]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Networks Found",
        len(networks_df)
    )

    col2.metric(
        "Strongest Network",
        best_network["SSID"]
    )

    col3.metric(
        "Best Signal",
        f'{best_network["Signal (%)"]}%'
    )


# Spatial measurement section.
st.header("2. Record a Spatial Signal Measurement")

st.write(
    "Visit a location, measure its actual Wi-Fi signal in dBm "
    "using a suitable measurement tool, and enter the result below."
)

with st.form("measurement_form"):
    location = st.text_input(
        "Location name",
        placeholder="Example: Bedroom"
    )

    col1, col2 = st.columns(2)

    with col1:
        x_coordinate = st.number_input(
            "X coordinate",
            min_value=0,
            max_value=100,
            value=0
        )

    with col2:
        y_coordinate = st.number_input(
            "Y coordinate",
            min_value=0,
            max_value=100,
            value=0
        )

    ssid = st.text_input(
        "Wi-Fi network name (SSID)"
    )

    signal_dbm = st.number_input(
        "Measured signal strength (dBm)",
        min_value=-120,
        max_value=0,
        value=-60
    )

    submitted = st.form_submit_button(
        "Save Measurement"
    )

    if submitted:
        if not location.strip():
            st.error("Please enter a location name.")

        elif not ssid.strip():
            st.error("Please enter the Wi-Fi network name.")

        else:
            new_record = pd.DataFrame([{
                "Location": location.strip(),
                "X": x_coordinate,
                "Y": y_coordinate,
                "SSID": ssid.strip(),
                "Signal (dBm)": signal_dbm,
                "Timestamp": datetime.now().isoformat(
                    timespec="seconds"
                )
            }])

            existing = pd.read_csv(DATASET_PATH)

            updated = pd.concat(
                [existing, new_record],
                ignore_index=True
            )

            updated.to_csv(
                DATASET_PATH,
                index=False
            )

            st.success("Measurement saved successfully!")


# Display measurements.
st.header("3. View Recorded Measurements")

data = pd.read_csv(DATASET_PATH)
try:
    existing = pd.read_csv(DATASET_PATH)
except pd.errors.EmptyDataError:
    existing = pd.DataFrame()

if data.empty:
    st.info(
        "No measurements have been recorded yet. "
        "Add measurements above to generate your heatmap."
    )

else:
    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )

    weak_count = (
        data["Signal (dBm)"] < -70
    ).sum()

    col1, col2 = st.columns(2)

    col1.metric(
        "Measurements Recorded",
        len(data)
    )

    col2.metric(
        "Weak Measurements",
        int(weak_count)
    )

    st.caption(
        "Measurements below -70 dBm are flagged as weak "
        "for this project's configurable default threshold."
    )

    # Heatmap section.
    st.header("4. Spatial Wi-Fi Heatmap")

    selected_ssid = st.selectbox(
        "Select Wi-Fi network",
        sorted(data["SSID"].dropna().unique())
    )

    filtered_data = data[
        data["SSID"] == selected_ssid
    ]

    fig = create_heatmap(filtered_data)

    if fig is not None:
        st.pyplot(fig)
        import matplotlib.pyplot as plt
        plt.close(fig)

    # Weak location report.
    st.header("5. Weak Signal Locations")

    weak_data = filtered_data[
        filtered_data["Signal (dBm)"] < -70
    ]

    if weak_data.empty:
        st.success(
            "No recorded measurements for this network "
            "are below -70 dBm."
        )

    else:
        st.warning(
            f"{len(weak_data)} recorded measurements "
            "are below -70 dBm."
        )

        st.dataframe(
            weak_data[
                [
                    "Location",
                    "X",
                    "Y",
                    "Signal (dBm)"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    # Download report.
    st.header("6. Download Measurement Report")

    csv_data = filtered_data.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📥 Download CSV Report",
        data=csv_data,
        file_name="wifi_signal_report.csv",
        mime="text/csv"
    )