<img src = "1w.png">
# 🐍 Snake_AP

# 🐍 Snake_AP

> **Created by: JACSTROY**

**Snake_AP** is a Python-based tool designed for WiFi access point emulation, deauthentication attacks, captive portal creation, and more. It provides a variety of options to control wireless interfaces, spoof networks, collect credentials, and spoof DNS responses.

---

## 🔌 Wi-Fi Adapter Used: Alfa AWUS036NHA (Atheros AR9271)

### 📦 Device Overview

The [**Alfa AWUS036NHA**](https://www.alfa.com.tw/products_show.php?pc=34&ps=201) is a high-performance USB Wi-Fi adapter powered by the **Atheros AR9271** chipset. It is widely used in wireless security research due to its excellent compatibility with Linux and powerful wireless performance.

| Feature              | Description                            |
| -------------------- | -------------------------------------- |
| **Chipset**          | Atheros AR9271                         |
| **Wi-Fi Standard**   | IEEE 802.11b/g/n (2.4 GHz only)        |
| **Max Speed**        | Up to 150 Mbps                         |
| **Antenna**          | 5 dBi RP-SMA detachable (upgradeable)  |
| **Interface**        | USB 2.0 (Mini-B)                       |
| **OS Compatibility** | Linux, Windows (via 3rd party drivers) |
| **Modes Supported**  | Monitor Mode, Packet Injection         |

### ✅ Why This Adapter Is Used

- Monitor mode and packet injection support out-of-the-box.
- Fully supported by the `ath9k_htc` driver in most Linux distros, including Kali Linux.
- Ideal for use with tools like `aircrack-ng`, `snek_ap`, `hostapd`, and other Wi-Fi audit frameworks.

### ⚠️ Limitations

- **Single-interface limitation**: This device cannot reliably split into two simultaneous virtual interfaces (e.g., AP + client) due to hardware constraints.
- **Only 2.4 GHz**: No support for 5 GHz bands.
- Creating additional interfaces using commands like:
  ```bash
  sudo iw dev wlan1 interface add wlansnake type station
  ```
  may work temporarily, but dual-mode operation is **not stable or recommended**.

### 🛠️ Setup Example (Kali Linux)

```bash
# Install firmware if not already available
sudo apt update && sudo apt install firmware-atheros

# Enable monitor mode
sudo ip link set wlan1 down
sudo iw dev wlan1 set type monitor
sudo ip link set wlan1 up
```

### 🧪 Used With: `snek_ap`

This adapter is tested and fully compatible with `snek_ap`, allowing:

- Rogue AP attacks
- Beacon/Probe flooding
- Packet injection-based attacks

---

## 📖 Usage

```bash
python3 snake_ap.py <Options>
```

---

## ⚙️ Options

| Short    | Long                                        | Description                                                                                                          |
| -------- | ------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| `-S`     | `--Show`                                    | Display all nearby access points with details such as BSSID, SSID, channel, and signal strength.                     |
| `-I`     | `--Interface`                               | Specify the network interface to act as an access point (must support AP mode).                                      |
| `-AP`    | `--APName`                                  | Set the name of the access point (default is `'Free-wifi'` if not specified).                                        |
| `-D`     | `--Deauth`                                  | Send deauthentication packets to a target WiFi network using `aireplay-ng`.                                          |
| `-CP`    | `--Portal`                                  | Enable a captive portal for WiFi login pages.                                                                        |
| `-L`     | `--List`                                    | Check the availability of access points.                                                                             |
| `-T`     | `--Target`                                  | Specify the MAC address of the target device to send deauthentication packets.                                       |
| `-P`     | `--Packet`                                  | Set the number of deauthentication packets to send.                                                                  |
| *(none)* | `--dns`                                     | Enable DNS spoofing for selected websites.                                                                           |
| *(none)* | `--cert`                                    | Renew SSL certificates spoofing for specified websites. **(conflicts with `-cert`)**                                 |
| *(none)* | `--reset`                                   | Reset all Apache2 configurations, clear cache, and remove all Snake_AP setups.                                       |
| `-W`     | `--webdata`                                 | Print credentials captured from websites.                                                                            |

> ⚠️ **Note:** The options `-cert` and `--cert` conflict. You should rename one of them to avoid runtime issues.

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
