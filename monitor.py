from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
import time
from message import send_message, send_ha_notification
import os


class ScanFolder:
    def __init__(self, config):
        # Monitor the screenshots folder for any file ending in .tga
        self.path = config["path"] + "\\_retail_\\Screenshots"
        self.token = config["token"]
        self.chat_id = config["chat_id"]
        self.ha_url = config.get("ha_url", "")
        self.ha_token = config.get("ha_token", "")
        self.ha_service = config.get("ha_service", "persistent_notification")
        self.event_handler = PatternMatchingEventHandler(patterns=["*.tga"], ignore_patterns=None,
                                                         ignore_directories=False, case_sensitive=True)
        self.event_handler.on_created = self.on_created
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.path, recursive=False)
        self.observer.start()

    def on_created(self, event):
        print("Queue detected! Sending alerts...")
        send_message(self.token, self.chat_id)
        send_ha_notification(self.ha_url, self.ha_token, self.ha_service)
        if os.path.exists(event.src_path):
            os.remove(event.src_path)  # Delete the screenshot we created

    def stop(self):
        self.observer.stop()
        self.observer.join()


def monitor(config):
    observer = ScanFolder(config)
    print("Monitoring...")
    try:
        while True:
            time.sleep(1)  # Blocking sleep so we only check every second
    except:
        observer.stop()
