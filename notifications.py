import smtplib
import tweepy
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(settings, subject, body):
    if not settings.get('enabled', True):
        return
    msg = MIMEMultipart()
    msg['From'] = settings['sender_email']
    msg['To'] = settings['receiver_email']
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    try:
        server = smtplib.SMTP(settings['smtp_server'], settings['smtp_port'])
        server.starttls()
        server.login(settings['sender_email'], settings['sender_password'])
        text = msg.as_string()
        server.sendmail(settings['sender_email'], settings['receiver_email'], text)
        server.quit()
        print("✅ Email sent successfully")
    except Exception as e:
        print(f"❌ Error sending email: {e}")


def send_tweet(settings, body):
    if not settings.get('enabled', False):
        return
    try:
        client = tweepy.Client(
            consumer_key=settings['api_key'],
            consumer_secret=settings['api_secret'],
            access_token=settings['access_token'],
            access_token_secret=settings['access_token_secret']
        )
        response = client.create_tweet(text=body)
        print(f"✅ Tweet sent successfully! ID: {response.data['id']}")
    except Exception as e:
        print(f"❌ Error sending tweet: {e}")


def daily_report(config_email, config_twitter, daily_log):
    valid_entries = [v for v in daily_log.values() if isinstance(v, dict)]
    if not valid_entries:
        return

    total_count = len(valid_entries)
    lowest = min(valid_entries, key=lambda x: x['min_alt'])
    fastest = max(valid_entries, key=lambda x: x['max_speed'])
    
    low_meters = int(lowest['min_alt'] * 0.3048)
    fast_kmh = int(fastest['max_speed'] * 1.852)

    subject = f"✈️ Daily Flight Report - {datetime.now().strftime('%Y-%m-%d')}"
    
    email_body = f"""
    <html>
    <body style="font-family: Arial, sans-serif;">
        <h2 style="color: #2c3e50;">📅 Daily ADS-B Summary</h2>
        <p><b>📊 Overview</b><br>
        Total Unique Aircraft Seen: {total_count} 📡</p>
        
        <p><b>📉 Lowest Flight of the Day</b><br>
        Flight Code: {lowest['flight']}<br>
        Minimum Altitude: {lowest['min_alt']} ft ({low_meters} m)<br>
        Time First Seen: {lowest['first_seen']}</p>
    
        <p><b>🚀 Fastest Flight of the Day</b><br>
        Flight Code: {fastest['flight']}<br>
        Max Speed: {fastest['max_speed']} kts ({fast_kmh} km/h)</p>
        Time First Seen: {fastest['first_seen']}</p>

    </body>
    </html>
    """

    twitter_body = (
        f"📅 Daily ADS-B Summary\n"
        f"Total Aircraft: {total_count} 📡\n\n"
        f"📉 Lowest: {lowest['flight']} at {lowest['min_alt']}ft\n"
        f"🚀 Fastest: {fastest['flight']} at {fastest['max_speed']}kts"
    )

    send_email(config_email, subject, email_body)
    #send_tweet(config_twitter, twitter_body)