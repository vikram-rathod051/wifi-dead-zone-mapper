def classify_signal(signal):
    if signal >= 80:
        return "Excellent"

    elif signal >= 60:
        return "Good"

    elif signal >= 40:
        return "Fair"

    else:
        return "Weak"


def analyze_networks(networks):
    analyzed = []

    for network in networks:
        signal = network["Signal (%)"]

        analyzed.append({
            "SSID": network["SSID"],
            "Signal (%)": signal,
            "Signal Quality": classify_signal(signal),
            "Security": network["Security"]
        })

    return analyzed