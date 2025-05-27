<img src = "1.png">
# 🐍 Snake_AP

> **Created by: JACSTROY**

**Snake_AP** is a Python-based tool designed for WiFi access point emulation, deauthentication attacks, captive portal creation, and more. It provides a variety of options to control wireless interfaces, spoof networks, collect credentials, and spoof DNS responses.

---

## 📖 Usage

```bash
python3 snake_ap.py <Options>
```

---

## ⚙️ Options

| Short | Long        | Description |
|-------|-------------|-------------|
| `-S`  | `--Show`     | Display all nearby access points with details such as BSSID, SSID, channel, and signal strength. |
| `-I`  | `--Interface`| Specify the network interface to act as an access point (must support AP mode). |
| `-AP` | `--APName`   | Set the name of the access point (default is `'Free-wifi'` if not specified). |
| `-D`  | `--Deauth`   | Send deauthentication packets to a target WiFi network using `aireplay-ng`. |
| `-CP` | `--Portal`   | Enable a captive portal for WiFi login pages. |
| `-L`  | `--List`     | Check the availability of access points. |
| `-T`  | `--Target`   | Specify the MAC address of the target device to send deauthentication packets. |
| `-P`  | `--Packet`   | Set the number of deauthentication packets to send. |
| `-cert` | *(no long form)* | Renew SSL certificates. |
| *(none)* | `--dns`   | Enable DNS spoofing for selected websites. |
| *(none)* | `--cert`  | Renew SSL certificates spoofing for specified websites. |
| *(none)* | `--reset` | Reset all Apache2 configurations, clear cache, and remove all Snake_AP setups. |
| `-W` | `--webdata`   | Print credentials captured from websites. |

> ⚠️ **Note:** The options `-cert` and `--cert` conflict. You should rename one of them to avoid runtime issues.

---

## 🧪 Example Commands

```bash
# Show all nearby access points
python3 snake_ap.py --Show

# Create an AP named 'MyNetwork' on wlan0
python3 snake_ap.py --Interface wlan0 --APName MyNetwork --Portal

# Send deauth packets
python3 snake_ap.py --Deauth wlan0 --Target AA:BB:CC:DD:EE:FF --Packet 100

# Enable DNS spoofing
python3 snake_ap.py --dns
```

---

## 🧰 Requirements

- Python 3.x
- `argparse` (standard library)
- `aireplay-ng`, `airmon-ng`
- `hostapd`, `dnsmasq`, `iptables`
- Apache2 (for captive portal)

---

## ⚠️ Disclaimer

This tool is intended for **educational and ethical hacking purposes only**. Use it **only** on networks you own or have explicit permission to test.

---

## 📄 License

MIT License
