# 📡 Wi-Fi Dead Zone & Spatial RF Signal Strength Mapper

## 📌 Project Overview

The **Wi-Fi Dead Zone & Spatial RF Signal Strength Mapper** is a Python-based web application developed using Streamlit. It helps users analyze Wi-Fi signal strength at different locations and identify areas with weak Wi-Fi connectivity.

The application records signal measurements, visualizes Wi-Fi coverage through a spatial heatmap, and generates downloadable measurement reports.

## 🎯 Problem Statement

Poor Wi-Fi connectivity and dead zones can affect internet performance in homes, offices, and other environments. This project helps identify weak signal areas by collecting signal strength measurements at different locations and visualizing them using a heatmap.

## ✨ Key Features

- **Wi-Fi Network Scanner:** Scan nearby Wi-Fi networks where the scanning utility is supported.
- **Signal Measurement:** Record Wi-Fi signal strength at different locations.
- **Measurement Storage:** Save and view recorded measurements.
- **Spatial Wi-Fi Heatmap:** Visualize signal strength using a graphical heatmap.
- **Weak Signal Detection:** Identify locations with weak Wi-Fi signals.
- **CSV Report:** Download recorded measurement data for further analysis.
- **Interactive Dashboard:** Easy-to-use Streamlit interface.

## 🛠️ Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib
- Regular Expressions
- Subprocess
- GitHub

## 📂 Project Structure

```text
Wi-Fi-Dead-Zone-Mapper/
│
├── app.py
├── wifi_scanner.py
├── signal_analyzer.py
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

**Step 1: Clone the Repository**

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

**Step 2: Open the Project Folder**

```bash
cd wifi-dead-zone-mapper
```

**Step 3: Install Required Libraries**

```bash
pip install -r requirements.txt
```

**Step 4: Run the Application**

```bash
streamlit run app.py
```

**Step 5: Open in Browser**

The application will open at:

```text
http://localhost:8501
```

## 📊 How It Works

1. Open the Wi-Fi Dead Zone Mapper application.
2. Scan available Wi-Fi networks where supported.
3. Enter location details and coordinates.
4. Record Wi-Fi signal strength in dBm.
5. Save the measurements.
6. View the spatial Wi-Fi heatmap.
7. Identify weak signal locations.
8. Download the measurement report in CSV format.

## 📈 Expected Output

- Wi-Fi network information.
- Recorded signal measurements.
- Spatial Wi-Fi signal strength heatmap.
- Weak signal location analysis.
- Downloadable CSV report.

## 🌍 Real-World Applications

- Home Wi-Fi optimization.
- Office network planning.
- Wi-Fi coverage analysis.
- Network troubleshooting.
- Identification of Wi-Fi dead zones.

## 🚀 Future Enhancements

- Real-time Wi-Fi signal monitoring.
- GPS-based location tracking.
- Advanced machine learning-based signal prediction.
- Interactive floor plan visualization.
- Automatic Wi-Fi coverage optimization.

## 👨‍💻 Developer

**Vikram**

AI & Machine Learning Student

## 📜 License

This project is developed for educational and academic purposes.

---

⭐ If you find this project interesting, consider giving this repository a star!
