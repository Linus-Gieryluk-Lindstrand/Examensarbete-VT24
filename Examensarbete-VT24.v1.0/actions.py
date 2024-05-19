# Imported Modules
import time
from pushover import pushover_app
from gmail import gmail_app

def start_timer() -> float:
    start_time = time.time()
    return start_time

def end_timer(start_time: float) -> float:
    end_time = time.time()
    elapsed_time = end_time - start_time
    elapsed_time_in_minutes = elapsed_time/60
    return elapsed_time_in_minutes

def coffee_pushover_notifier() -> None:
    user_key = "USER_KEY"
    api_token = "API_TOKEN"
    pushover_notification = pushover_app.PushoverNotification(user_key, api_token)
    notification_content = "CONTENT"
    pushover_notification.send_msg(notification_content)

def coffee_mail_notifier(msg: str) -> None:
    notifier = gmail_app.EmailNotification("SENDER_GMAIL", "APPLICATION_PASSWORD")
    notifier.send_email(to="RECEIVER_GMAIL",subject="SUBJECT",body=msg)