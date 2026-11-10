import subprocess
import platform
import re


def scan_wifi():
    try:
        system = platform.system()

        if system == "Windows":
            command = [
                "netsh", "wlan", "show",
                "networks", "mode=bssid"
            ]

        elif system == "Linux":
            command = ["nmcli", "-t", "-f", "SSID,SIGNAL,SECURITY", "dev", "wifi", "list"]

        else:
            return [], "Unsupported operating system."

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=20
        )

        if result.returncode != 0:
            return [], result.stderr or "Wi-Fi scan failed."

        networks = []

        if system == "Windows":
            current_ssid = None

            for line in result.stdout.splitlines():
                line = line.strip()

                if line.startswith("SSID ") and ":" in line:
                    current_ssid = line.split(":", 1)[1].strip()

                elif line.startswith("Signal") and ":" in line:
                    match = re.search(r"(\d+)%", line)

                    if match and current_ssid:
                        networks.append({
                            "SSID": current_ssid,
                            "Signal (%)": int(match.group(1)),
                            "Security": "Unknown"
                        })
                        current_ssid = None

        else:
            for line in result.stdout.splitlines():
                parts = line.split(":")

                if len(parts) >= 3 and parts[0]:
                    networks.append({
                        "SSID": parts[0],
                        "Signal (%)": int(parts[1]),
                        "Security": parts[2] or "Unknown"
                    })

        if not networks:
            return [], "No Wi-Fi networks found."

        return networks, None

    except FileNotFoundError:
        return [], "Wi-Fi scanning utility is unavailable on this server."

    except Exception as error:
        return [], str(error)
