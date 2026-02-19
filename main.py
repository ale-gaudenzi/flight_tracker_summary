import time
import json
import schedule
from datetime import datetime
from notifications import daily_report


def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
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


def trigger_report():
    daily_report(config['email'], config['twitter'], daily_log)
    daily_log.clear()


if __name__ == "__main__":
    config = load_config()
    daily_log = {}

    interval = config['system'].get('check_interval', 10)
    report_time = config['system'].get('report_time', "23:59")
    
    schedule.every(interval).seconds.do(update_tracker)
    schedule.every().day.at(report_time).do(trigger_report)
    
    print(f"Tracker started. Checking every {interval}s. Report scheduled for {report_time}.")

    while True:
        schedule.run_pending()
        time.sleep(1)