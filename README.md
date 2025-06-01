➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️

# 📢 Twitch Chat Bot by TheAsarya  
_with assistance from ChatGPT and Claude AI_


➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️

## 🎯 Main Functionality Summary

- Automatically shouts out users who are on a list when they post their first message of the stream.
- Users can have custom shoutouts; if they don’t, they’ll receive the default.
- Users can be added to the list via command.
- Custom shoutouts can be added or edited via command.
- Users can be removed from the list via command.

➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️

## 🪛 Installation Instructions (Windows)

1. Install Python from [python.org](https://www.python.org).  
   Tested with versions 3.13.3 and 3.12.10.

2. Add Python to your PATH/environment variables (if not done automatically).  
   You can check if python's already in your path by running this in a terminal (run `cmd` from windows search):
   ```shell
   python --version
   ```

3. Install required Python packages:
   ```shell
   pip install twitchio python-dotenv
   ```

4. Download the SOBot project files  
   Place them in a convenient folder (e.g. your Documents folder).

5. Edit the following in the project files:
   - Choose the Twitch account the bot will use (an account that is not the one you're streaming from is preferable).  
     Get a bot access token from [twitchtokengenerator.com](https://twitchtokengenerator.com).  
     Open `.env.example`, replace the placeholder text with your bot token. Save and rename the file to `.env`.  

     ⚠️ **N.B. Never share your access token**.

   - In `SOBot.py`, find the line:
     ```python
     self.channelname = "theasarya"
     ```
     Replace `"theasarya"` with your Twitch channel name in lowercase.
   - Customize the default shoutout as described in the [Customization](#customisation) section below.

6. Run the bot:
   - Open a terminal (`cmd`)
   - Navigate to your SOBot folder:
     ```shell
     cd path\to\SOBot
     ```
   - Run
     ```shell
     python SOBot.py
     ```

7. Make the bot a mod in your Twitch channel.

8. Try a command like `!hellosb` in chat to see if it's responding correctly.

9. Edit the `bat` file:
   - Put it somewhere easy to access (e.g. Desktop)
   - Update it to point to your current `SOBot.py` path

10. Double-click the `.bat` file to launch the bot quickly in the future.

11. Once you're confident the bot is functioning correctly, you can set:
    ```python
    self.debug = False
    ```
    in `SOBot.py` to reduce terminal spam.

➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️

## 🛠️ Commands

| Command | Description |
|--------|-------------|
| `!addsbso [username] [custom_shoutout - optional]` | Add a user to the list; optionally add a custom shoutout |
| `!editsbso [username] [custom_shoutout]` | adds a custom shoutout to a user if they're already in the shoutout list. 
      Use with caution. this will overwrite any existing custom shoutout |
| `!hellosb` | Say hello to the bot so you can check if it's running |
| `!sbso [username]` | manual shoutout to a user if they're in the shoutout list. 
      will use custom shoutout if available. otherwise will use default message |
| `!removesbso [username]` | intended mainly for if a user is added with a typo in their name etc.
      use with caution |
| `!resetsbshouted` | resets the already shouted list which tracks who on the list 
      has already had an automated shoutout this stream (since the 
      bot was restarted or this command was last used) |
| `!sbcommands` | Lists available SOBot commands in chat |
| `!startsbsw [optional_offset_minutes]` | starts a stopwatch. optional offest lets you start the timer from 
      e.g. two minutes ago by doing "!startsbtimer 2" |
| `!sbsw` | report the current duration of the stopwatch in chat, if the stopwatch
      is active |
| `!stopsbsw` | stops the stopwatch, if there's one active, and reports the total
      duration in chat |

➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️

## 🎨 Customisation

- Change the default shoutout by editing:
  ```python
  self.defaultSO = "..."
  ```
  You can use `{user}` and `{game}` as dynamic placeholders.

- You can also edit `{username}_sODatabase.json` directly to add users and custom shoutouts:
  - Use UTF-8 encoding
  - Maintain the JSON formatting
  - Useful for batch editing

- Probably a good idea to backup your `{Username}_sODatabase.json` occasionally.

- Add your own commands between the following comment lines in `SOBot.py`. They may fail to register if further down:
  ```python
  # add additional commands after this line


  # add additional commands before this line
  ```

➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️➡️⬅️

## 📜 Changelog

- v0.6 - general tidying up. github initial public release
- v0.5 – Fixed bug with remote `.bat` file path resolution
- v0.4 – Test release
