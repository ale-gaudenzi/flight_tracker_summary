import smtplib
import tweepy
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(settings, subject, body):
    if not settings.get('enabled', True):
        return

    msg = MIMEMultipart()
    msg['From'] = settings['sender_email']
    msg['To'] = settings['receiver_email']
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

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