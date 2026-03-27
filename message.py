import requests


def get_chat_id(token):
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    data = requests.get(url).json()  # Try find chat that user sent to our bot
    try:
        chat_id = data["result"][0]["message"]["chat"]["id"]  # Retrieve chat id so we can reply
    except IndexError:
        return None
    return str(chat_id)


def send_message(token, chat_id):
    message = "Your Solo Shuffle is ready."
    url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url)  # Send the message to the user


def send_ha_notification(ha_url, ha_token, ha_service, message="Your Solo Shuffle is ready.", title="Queue Alert"):
    """Send notification to Home Assistant via REST API."""
    if not ha_url or not ha_token:
        print("Home Assistant notification skipped: ha_url or ha_token not configured.")
        return
    
    headers = {
        "Authorization": f"Bearer {ha_token}",
        "Content-Type": "application/json"
    }
    
    # Payload structure depends on the service type
    if ha_service.startswith("mobile_app_"):
        payload = {
            "message": message,
            "title": title,
            "data": {"tag": "queue_alert"}
        }
    else:  # persistent_notification or custom notifier
        payload = {
            "message": message,
            "title": title
        }
    
    try:
        url = f"{ha_url}/api/services/notify/{ha_service}"
        response = requests.post(url, json=payload, headers=headers, timeout=5)
        if response.status_code == 200:
            print(f"Home Assistant notification sent successfully.")
        else:
            print(f"Home Assistant notification failed: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending Home Assistant notification: {e}")
