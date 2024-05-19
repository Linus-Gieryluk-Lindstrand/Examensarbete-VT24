# Imported Modules
import requests

# Documentation at: https://pushover.net/api.

class PushoverNotification:
    """
    Class handles Pushover notifications.
    """

    # Constant values.
    api_url = "https://api.pushover.net/1/messages.json"

    def __init__(self, user_key: str, api_token: str) -> None:
        self.user = user_key
        self.token = api_token

    def send_msg(self, message: str) -> None:
        data = {
            "token": self.token,
            "user": self.user,
            "message": message, 
            "sound": "vibrate" # optional, a list of sound is in the documentation.
        }

        # POST an HTTPS request to Pushover API with the data.
        requests.post(self.api_url, data=data)
        print("Message sent.")

"""
Example 
"""
if __name__ == "__main__":
    # Required information; gathered from Pushover site.
    user_key = "USER_KEY"
    api_token = "API_TOKEN"

    notifier = PushoverNotification(user_key, api_token)
    message = "MESSAGE"

    notifier.send_msg(message)
