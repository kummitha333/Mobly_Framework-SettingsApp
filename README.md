# Mobly_Framework-SettingsApp

A Podman-based automated testing framework for Android Settings App using Mobly. Designed for cross-platform scalability, this framework runs inside a Podman container with GoTTY-based shell access and integrates with the Sirius platform to enable real-time mobile automation workflows.

---

## 🚀 Overview

This system supports:
- Automated test execution using Mobly
- Snippet-based control of Android services
- Real-time test logging and reporting
- Parallel test execution across multiple Android devices

It operates in a **Podman container environment** and is optimized for **Windows/Linux** hosts.

---

## 🧭 System Context

- **Containerization**: Podman-managed Docker image
- **Access**: Web-based GoTTY shell
- **Platform Integration**: Sirius automation platform
- **Device Support**: USB and wireless ADB-connected Android devices

---

## 🔑 Key Features

- ✅ YAML-based test configuration
- ✅ Parallel test execution on 10+ Android devices
- ✅ Snippet-based interactions with Android system services
- ✅ Real-time logging and structured test reports
- ✅ Media/data upload & download over HTTP
- ✅ Self-recovering and fault-tolerant test execution

---

## 📦 Technical Architecture
##.yml file

---

## ✅ Functional Requirements

1. Run Mobly tests on Android devices connected via ADB.
2. Generate structured test reports (JSON, HTML).
3. Upload/download test data (e.g., logs, media) over HTTP.
4. Automatically detect and recover from test failures.

---

## 🔧 Non-Functional Requirements

- ⏱ Cross-platform: Windows and Linux support
- 📈 Scalability: Tested with up to 10 Android devices
- 💡 Fault-tolerant: Automatically retries failed tests

---

## 🛠️ Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/kummitha333/Mobly_Framework-SettingsApp.git
   cd Mobly_Framework-SettingsApp
2.Build Podman Image
bash
podman build -t mobly-settings .
3.Run the Container
bash
podman run --rm -it --privileged -v /dev/bus/usb:/dev/bus/usb mobly-settings
4.Access GoTTY Shell
Open your browser and navigate to:
http://<host-ip>:8080
5.Start a Test
bash
python3 test_script.py --config test_settings.yml

---

📄 Example YAML Config

TestBeds:
  - Name: SettingsAppTest
    Controllers:
      AndroidDevice:
        - serial: <device_serial>
    TestParams:
      network: WiFi
      toggle_options: [Bluetooth, AirplaneMode, DarkTheme]

---    

Contributing:
Feel free to fork the repo and submit pull requests. Issues and feature requests are welcome.
