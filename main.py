import time
import json
import schedule
from datetime import datetime
import notifications

config = {}
daily_log = {}


def load_config():
    global config
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        exit(1)


def fetch_data():
    try:
        with open(config['system']['json_path'], 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Read error: {e}")
    return None


def update_tracker():
    data = fetch_data()
    if not data or 'aircraft' not in data:
        return
    
    now_str = datetime.now().strftime("%H:%M")

    for plane in data['aircraft']:
        if 'hex' not in plane:
            continue
        hex_code = plane['hex']

        flight = plane.get('flight', 'Unknown').strip()

        alt = plane.get('altitude') or plane.get('alt_baro')
        if alt is None or not isinstance(alt, (int, float)) or alt <= 0:
            continue

        speed = plane.get('speed') or plane.get('gs')
        if speed is None or not isinstance(speed, (int, float)):
            speed = 0

        if hex_code not in daily_log:
            daily_log[hex_code] = {
                'flight': flight,
                'min_alt': alt,      
                'max_speed': speed,  
                'first_seen': now_str
            }
        else:
            if alt < daily_log[hex_code]['min_alt']:
                daily_log[hex_code]['min_alt'] = alt
            if speed > daily_log[hex_code]['max_speed']:
                daily_log[hex_code]['max_speed'] = speed
            if daily_log[hex_code]['flight'] == 'Unknown' and flight != 'Unknown':
                daily_log[hex_code]['flight'] = flight


def process_daily_report():
    if not daily_log:
        return

    total_count = len(daily_log)
    lowest = min(daily_log.values(), key=lambda x: x['min_alt'])
    fastest = max(daily_log.values(), key=lambda x: x['max_speed'])
    low_meters = int(lowest['min_alt'] * 0.3048)
    fast_kmh = int(fastest['max_speed'] * 1.852)

    subject = f"Daily Flight Report - {datetime.now().strftime('%Y-%m-%d')}"
    body = f"""
    📅 Daily ADS-B Summary

    📊 **Overview**
    Total Unique Aircraft Seen: {total_count} 📡
        
    📉 **Lowest Flight of the Day**
    Flight: {lowest['flight']}
    Minimum Altitude: {lowest['min_alt']} ft ({low_meters} m)
    Time First Seen: {lowest['first_seen']}
        
    🚀 **Fastest Flight of the Day**
    Flight: {fastest['flight']}
    Max Speed: {fastest['max_speed']} kts ({fast_kmh} km/h)
    """

    notifications.send_email(config['email'], subject, body)
    #notifications.send_tweet(config['twitter'], body)

    daily_log.clear()


if __name__ == "__main__":
    load_config()
    
    interval = config['system'].get('check_interval', 10)
    report_time = config['system'].get('report_time', "23:59")
    
    schedule.every(interval).seconds.do(update_tracker)
    schedule.every().day.at(report_time).do(process_daily_report)
    
    print(f"Tracker started. Checking every {interval}s. Report scheduled for {report_time}.")

    while True:
        schedule.run_pending()
        time.sleep(1)