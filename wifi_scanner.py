import subprocess
import re


def scan_wifi():
    try:
        result = subprocess.run(
            ["netsh", "wlan", "show", "networks", "mode=bssid"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=20
        )

        if result.returncode != 0:
            return [], "Unable to scan Wi-Fi networks."

        networks = []
        current_ssid = None
        current_signal = None
        current_security = None

        for line in result.stdout.splitlines():
            line = line.strip()

            if line.startswith("SSID ") and ":" in line:
                if current_ssid and current_signal is not None:
                    networks.append({
                        "SSID": current_ssid,
                        "Signal (%)": current_signal,
                        "Security": current_security or "Unknown"
                    })

                current_ssid = line.split(":", 1)[1].strip()
                current_signal = None
                current_security = None

            elif line.startswith("Signal") and ":" in line:
                match = re.search(r"(\d+)%", line)

                if match:
                    current_signal = int(match.group(1))

            elif line.startswith("Authentication") and ":" in line:
                current_security = line.split(":", 1)[1].strip()

        if current_ssid and current_signal is not None:
            networks.append({
                "SSID": current_ssid,
                "Signal (%)": current_signal,
                "Security": current_security or "Unknown"
            })

        if not networks:
            return [], "No networks found. Check that Wi-Fi is enabled."

        return networks, None

    except FileNotFoundError:
        return [], "Windows netsh was not found."

    except subprocess.TimeoutExpired:
        return [], "Wi-Fi scanning timed out."

    except Exception as error:
        return [], str(error)