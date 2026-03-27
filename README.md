# QueueNotify (program)
## Description
Program that sends you a text when your Solo Shuffle pops in World of Warcraft. Developed for Windows 11 (but 10 should work).

**Please note that this program is in Alpha, and so you can expect errors to occur and things to be more difficult to set up for now. I've decided to release it despite the somewhat primitive state, as I think it will be useful for a lot of people who are able to follow the instructions below.**

Report any problems in the [Issues](https://github.com/dev-fatal/queue-notify/issues) tab, but please try searching things yourself first.

You can view the addon source code here: https://github.com/dev-fatal/queue-notify-addon

## Installation
1. Install the QueueNotify addon via [CurseForge](https://www.curseforge.com/wow/addons/queuenotify) or [Wago](https://addons.wago.io/addons/queuenotify) and then `/reload`
2. Install [Python 3 for Windows](https://www.python.org/downloads/) and ensure it's in your PATH. Note that this program has been tested on Python version 3.10
3. Download this repo (`git clone https://github.com/dev-fatal/queue-notify`, or [download the ZIP](https://github.com/dev-fatal/queue-notify/archive/refs/heads/main.zip) and then extract it somewhere)
4. Open Command Prompt and `cd` into where you saved it, e.g., `cd C:\Users\test\Documents\queue-notify`
5. Run `pip install -r requirements.txt` and wait until complete.

## Setup
### Telegram
1. Install the [Telegram app](https://telegram.org/apps) on your phone and sign up
2. Open a new message to the user `@BotFather` and type `/newbot`. You will then be prompted to fill in some values
3. Enter a name such as `QueueNotify`
4. Enter some unique username like `queuenotify_123456_bot`
5. Write down the HTTP API token you get, and enter it under `token` in the `config.toml` file
6. Ensure the `path` to your WoW folder in `config.toml` is correct. You must use double backslashes, e.g., `"C:\\Program Files (x86)\\World of Warcraft"`
7. Run the program (from inside the directory, as before) with `python main.py`. You will need to run this whenever you want to begin monitoring after a restart
8. When running for the first time, it will prompt you to send a message to your bot. Do this by clicking the `t.me/{username}` link given to you by the BotFather. Note you need to type something as well as the default `/start`.
9. Stop monitoring by closing the Command Prompt window.

### Home Assistant
Home Assistant integration supports three notification methods: persistent notifications, mobile app notifications, or custom notifiers.

#### Prerequisites
1. Have a Home Assistant instance running and accessible from your computer
2. Know your Home Assistant URL (e.g., `http://homeassistant.local:8123` or `http://192.168.1.100:8123`)

#### Creating a Long-Lived Access Token
1. In Home Assistant, go to **Settings** > **Devices & Services** > **Long-Lived Access Tokens** (at the bottom)
2. Click **Create Token** and name it `QueueNotify` (or something similar)
3. Copy the token and save it somewhere safe
4. Update `ha_token` in `config.toml` with this token

#### Option 1: Persistent Notifications
Sends notifications that appear in Home Assistant's notification panel and persist until dismissed.

1. Set `ha_service = "persistent_notification"` in `config.toml`
2. Add these to your Home Assistant configuration (optional, for customization):
   ```yaml
   # In configuration.yaml
   homeassistant:
     customize:
       notify.persistent_notification:
         friendly_name: "Queue Notify"
   ```
3. Test: Run `python main.py` and trigger a queue notification

#### Option 2: Mobile App Notifications
Sends push notifications to your phone via the Home Assistant app.

1. Install the [Home Assistant mobile app](https://www.home-assistant.io/app/) on your phone
2. Log in and complete the setup
3. Find your device name by going to **Settings** > **Devices & Services** > **Devices** and looking for your phone
4. Alternatively, check the notification service by going to **Developer Tools** > **Services** and finding the `notify.mobile_app_*` service
5. Set `ha_service = "mobile_app_<device_name>"` in `config.toml` (e.g., `mobile_app_john_iphone` or `mobile_app_jane_samsung`)
6. Test: Run `python main.py` and trigger a queue notification - you should receive a push notification

#### Option 3: Custom Notifier
Use a custom notification service you've configured in Home Assistant (MQTT, email, webhook, etc.).

1. In Home Assistant, ensure your custom notification service is set up and working
2. Get the service name by going to **Developer Tools** > **Services** and looking for your service under the `notify` domain
3. The service name format is typically `notify.service_name`
4. Set `ha_service = "service_name"` in `config.toml` (without the `notify.` prefix)
5. Test: Run `python main.py` and trigger a queue notification

#### Example config.toml for Home Assistant
```toml
token = ""  # Leave empty to use Home Assistant instead of Telegram
path = "C:\\World of Warcraft"
chat_id = ""

# Home Assistant Settings
ha_url = "http://192.168.1.100:8123"  # Your Home Assistant URL
ha_token = "aGFBNOIiy50.kb2saHFGN33q40krgk13n56bBDG"  # Your long-lived access token
ha_service = "persistent_notification"  # Options: persistent_notification, mobile_app_<device>, or custom service name
```

## Linux
If using Linux, you should make the following changes:
- Change `self.path = config["path"] + "\\_retail_\\Screenshots"` to `self.path = config["path"] + "/_retail_/Screenshots"` in `monitor.py`
- Use a path in the config such as `path = "/home/<username>/.local/share/Steam/steamapps/compatdata/<id>/pfx/drive_c/Program Files (x86)/World of Warcraft"`


## Updates
It is likely that this program will change significantly, and so you should check back here for updates. Please also keep the addon updated.


## Changing account
If you wish to change your linked Telegram account, simply change the `chat_id` value in `config.toml` to `""` and re-run the program.
