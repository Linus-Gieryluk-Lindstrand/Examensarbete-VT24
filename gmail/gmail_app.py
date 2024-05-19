# Simple program that sends an email.

# Imported Classes
from email.message import EmailMessage
from smtplib import SMTP

# email.message documentation: https://docs.python.org/3/library/email.message.html
# smtplib documentation: https://docs.python.org/3/library/smtplib.html

class EmailNotification:
    """
    Class handles Gmail notifications.
    """
    
    # Constant values
    HOST = "smtp.gmail.com"
    PORT = 587

    def __init__(self, sender: str, password: str) -> None:
        self.sender = sender
        self.password = password

    def send_email(self: str, to: str, subject: str, body: str) -> None:
        # Create instances.
        msg = EmailMessage()
        server = SMTP(host=self.HOST, port=self.PORT)

        # Message details.
        msg["to"] = to
        msg["subject"] = subject
        msg["from"] = self.sender
        msg.set_content(body)

        # Sending message.
        server.starttls()
        server.login(self.sender, self.password)
        server.send_message(msg)
        server.quit()