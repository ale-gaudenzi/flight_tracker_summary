# ✈️ ADS-B Daily Tracker

A lightweight Python tool for Raspberry Pi that tracks aircraft via `dump1090`, records daily statistics (lowest altitude, highest speed), and sends a summary report via Email and Twitter at the end of the day.

## 📋 Features

* **Real-time Monitoring**: Reads `aircraft.json` every 10 seconds (configurable).
* **Daily Stats**: Tracks the lowest flying and fastest aircraft of the day.
* **Automated Reporting**: Sends a summary at 23:59 via Email and Twitter.
* **Zero Database**: Uses in-memory storage for the day, resets after reporting.

## ⚙️ Requirements

* Python 3.x
* Running instance of `dump1090-mutability` or `dump1090-fa`
* Internet connection for SMTP and Twitter API

## 📦 Installation

1.  **Clone the repository**:
    ```bash
    git clone [https://github.com/yourusername/adsb-daily-tracker.git](https://github.com/yourusername/adsb-daily-tracker.git)
    cd adsb-daily-tracker
    ```

2.  **Install dependencies**:
    ```bash
    pip install schedule tweepy
    ```

3.  **Configuration**:
    Edit `config.json` with your settings:

    ```json
    {
        "system": {
            "json_path": "/run/dump1090-mutability/aircraft.json", 
            "check_interval": 10,
            "report_time": "23:59"
        },
        "email": {
            "enabled": true,
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "sender_email": "your-email@gmail.com",
            "sender_password": "your-app-password",
            "receiver_email": "receiver@gmail.com"
        },
        "twitter": {
            "enabled": true,
            "api_key": "YOUR_TWITTER_API_KEY",
            "api_secret": "YOUR_TWITTER_API_SECRET",
            "access_token": "YOUR_ACCESS_TOKEN",
            "access_token_secret": "YOUR_TOKEN_SECRET"
        }
    }
    ```

    *Note: For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833), not your login password.*

4.  **Run**:
    ```bash
    python main.py
    ```

## 🚀 Running in Background

To keep it running after you close the terminal, use `nohup` or create a systemd service.

```bash
nohup python3 main.py &