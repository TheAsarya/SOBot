"""
    Twitch chat bot by TheAsarya with assistance from ChatGPT and Claude AI
    
    Main functionality summary
    - automatically shouts out users who are on a list when they post their
        first message of the stream
    - users can have custom shoutouts or if they don't they'll get the default
    - users can be added to the list via command
    - users' custom shoutouts can be added or edited via command
    - users can be removed from the list via command
    
    look at the readme.txt for description of available commands and
    customisation info
    
    
"""

from twitchio.ext import commands
import datetime
from dotenv import load_dotenv
import os
import json
import time

#class to track the state of the bot
class SOBotState:
    def __init__(self):
        #track who's already been shouted out this stream
        self.channelname = "theasarya" #Enter your twitch channel username between the quotation marks in lowercase
        self.defaultSO = "Please welcome @{username} to the channel and give them a follow at http://www.twitch.tv/{username} for some excellent {game} gaming."
        self.defaultGame = ""
        self.already_shouted = set()
        self.stream_start_time = datetime.datetime.now()
        self.message_count = 0
        self.connected = False
        self.debug = True #set to true to enable debug prints. False to disable
        self.activeStopwatch = False
        self.stopwatchStart = time.time()
        self.validAccessLevels = {"anyone": {"accessText": "anyone"}, 
                                  "vipPlus": {"accessText": "vips, mods and the streamer"}, 
                                  "modPlus": {"accessText": "mods and the streamer"}, 
                                  "streamer": {"accessText": "the streamer"}}

        

class SOBot(commands.Bot):
    def __init__(self):
        
        # Load environment variables from the file .env in the SOBot folder
        load_dotenv()
        
        #initialise a bot state instance
        self.state = SOBotState()
        
        # Get the token from the environment file. create a file called ".env" in the same folder as this file with the contents TWITCH_TOKEN=oauth:your_twitch_access_token
        token = os.getenv('TWITCH_TOKEN')
        if token is None:
            raise ValueError("TWITCH_TOKEN environment variable not found")
            
        self.state.sOList = self.load_shoutouts()
        self.debug_print(f"shoutout list: {self.state.sOList}")


        # call the parent constructor for commands.Bot
        super().__init__(
            token=token,
            prefix='!',
            initial_channels=[self.state.channelname] 
        )
        
    """Command to check if the bot is running"""
    @commands.command(name='hellosb')    
    async def hellosb(self, ctx):        
        
        #access level check. use this in all commands and edit access_level as appropriate
        access_level = "anyone" #set access level to "anyone", "vipPlus", "modPlus", "streamer"
        if not self.has_access(ctx, access_level):
            text = self.state.validAccessLevels[access_level]["accessText"]
            await ctx.send(f"@{ctx.author.name} Only {text} can use this command")
            print(f"{ctx.author.name} not authorised for command")
            return
        
        print(f"helloSOBot command triggered by {ctx.author.name}")
        
        user = ctx.author.name
        await ctx.send(f"Yeah, yeah @{user} I'm awake 🤔")  
     
    # command to manually shout out a user who is in the shoutout list. 
    # uses default shoutout or custom if available    
    @commands.command(name='sbso')
    async def manual_shoutout(self, ctx, username: str):
        
        #access level check. use this in all commands and edit access_level as appropriate
        access_level = "modPlus" #set access level to "anyone", "vipPlus", "modPlus", "streamer"
        if not self.has_access(ctx, access_level):
            text = self.state.validAccessLevels[access_level]["accessText"]
            await ctx.send(f"@{ctx.author.name} Only {text} can use this command")
            print(f"{ctx.author.name} not authorised for command")
            return
        
        username = username.lstrip('@').lower()
        
        self.debug_print(f"\n Manual shoutout requested for: {username} \n")
        
        #check if user is in shout out list
        if username in self.state.sOList:
            user_entry = self.state.sOList.get(username)
            
            if user_entry != None:
                game = user_entry.get("customGame") or ""
                
            msg = user_entry.get("customSO") or self.state.defaultSO
            
            try:
                formatted_message = msg.format(username=username, game=game)
            except KeyError as e:
                formatted_message = f"Shoutout error {e}."
                await ctx.send(f"{formatted_message}")
                self.debug_print(f"Bad format string in shoutout for {username}: {msg}")
                return
            except ValueError as v:
                formatted_message = f"Shoutout error {v}."
                await ctx.send(f"{formatted_message}")
                self.debug_print(f"Bad format string in shoutout for {username}: {msg}")
                return
            
            await ctx.channel.send(f"{formatted_message}") 
            
            
        else:
            self.debug_print(f"{username} not in shoutout list")  
            await ctx.send(f"{username} not in shoutout list")
    
    #command to add user to the shoutout list if they're not in it already
    @commands.command(name='addsbso')
    async def add_shoutout(self, ctx, username: str, *, custom_message: str = ""):
        
        #access level check. use this in all commands and edit access_level as appropriate
        access_level = "modPlus" #set access level to "anyone", "vipPlus", "modPlus", "streamer"
        if not self.has_access(ctx, access_level):
            text = self.state.validAccessLevels[access_level]["accessText"]
            await ctx.send(f"@{ctx.author.name} Only {text} can use this command")
            print(f"{ctx.author.name} not authorised for command")
            return
        
        display_name = username.lstrip('@')
        username = username.lstrip('@').lower()
        
        try:
            formatted_message = custom_message.format(username=username, game=self.state.defaultGame)
        except KeyError as e:
            formatted_message = f"Shoutout error: {e}"
            await ctx.send(f"{formatted_message}")
            self.debug_print(f"Bad format string in shoutout for {username}: {custom_message}")
            return
        except ValueError as v:
            formatted_message = f"Shoutout error: {v}"
            await ctx.send(f"{formatted_message}")
            self.debug_print(f"Bad format string in shoutout for {username}: {custom_message}")
            return
        
        #check if user is already in shoutout list
        if not username in self.state.sOList:
            # Add to shoutout list in bot state
            self.state.sOList[username]= {
                "customSO": custom_message
            }
    
            # Save to JSON
            self.save_shoutouts()
    
            await ctx.send(f"Added shoutout for @{display_name} with message: \"{custom_message}\"")
        else:
            await ctx.send(f"{display_name} is already in the shoutout list")

    #command to remove user from shoutout list
    @commands.command(name='removesbso')
    async def remove_shoutout(self, ctx, username: str):
        
        #access level check. use this in all commands and edit access_level as appropriate
        access_level = "modPlus" #set access level to "anyone", "vipPlus", "modPlus", "streamer"
        if not self.has_access(ctx, access_level):
            text = self.state.validAccessLevels[access_level]["accessText"]
            await ctx.send(f"@{ctx.author.name} Only {text} can use this command")
            print(f"{ctx.author.name} not authorised for command")
            return
        
        display_name = username.lstrip('@')
        username = username.lstrip('@').lower()
        
        #check if user is already in shoutout list
        if username in self.state.sOList:
            # Add to shoutout list in bot state
            del self.state.sOList[username]
    
            # Save to JSON
            self.save_shoutouts()
    
            await ctx.send(f"Removed shoutout for @{display_name}")
        else:
            await ctx.send(f"{display_name} not in the shoutout list")
            
    #command to add or repalce a user's custom shoutout if they are on the list
    @commands.command(name='editsbso')
    async def edit_shoutout(self, ctx, username: str, *, custom_message: str = ""):
        
        #access level check. use this in all commands and edit access_level as appropriate
        access_level = "modPlus" #set access level to "anyone", "vipPlus", "modPlus", "streamer"
        if not self.has_access(ctx, access_level):
            text = self.state.validAccessLevels[access_level]["accessText"]
            await ctx.send(f"@{ctx.author.name} Only {text} can use this command")
            print(f"{ctx.author.name} not authorised for command")
            return
        
        display_name = username.lstrip('@')
        username = username.lstrip('@').lower()
        
        try:
            formatted_message = custom_message.format(username=username, game=self.state.defaultGame)
        except KeyError as e:
            formatted_message = f"Shoutout error: {e}"
            await ctx.send(f"{formatted_message}")
            self.debug_print(f"Bad format string in shoutout for {username}: {custom_message}")
            return
        except ValueError as v:
            formatted_message = f"Shoutout error: {v}"
            await ctx.send(f"{formatted_message}")
            self.debug_print(f"Bad format string in shoutout for {username}: {custom_message}")
            return
        
        #check if user is already in shoutout list
        if username in self.state.sOList:
            # add or replace custom shoutout

            self.state.sOList[username]["customSO"] = custom_message
    
            # Save to JSON
            self.save_shoutouts()
    
            await ctx.send(f"Edited custom shoutout for @{display_name} with message: \"{custom_message}\"")
        else:
            await ctx.send(f"{display_name} not in the shoutout list")
                        
    #command to reset the already shouted list
    @commands.command(name='resetsbshouted')
    async def reset_already_shoutout(self, ctx):
        
        #access level check. use this in all commands and edit access_level as appropriate
        access_level = "modPlus" #set access level to "anyone", "vipPlus", "modPlus", "streamer"
        if not self.has_access(ctx, access_level):
            text = self.state.validAccessLevels[access_level]["accessText"]
            await ctx.send(f"@{ctx.author.name} Only {text} can use this command")
            print(f"{ctx.author.name} not authorised for command")
            return
        
        self.state.already_shouted = set()

        await ctx.send("Already shouted list reset")
        
    #command to list available commands in chat
    @commands.command(name='sbcommands')
    async def sOBot_commands(self, ctx):
        
        #access level check. use this in all commands and edit access_level as appropriate
        access_level = "anyone" #set access level to "anyone", "vipPlus", "modPlus", "streamer"
        if not self.has_access(ctx, access_level):
            text = self.state.validAccessLevels[access_level]["accessText"]
            await ctx.send(f"@{ctx.author.name} Only {text} can use this command")
            print(f"{ctx.author.name} not authorised for command")
            return
        
        commands = format(list(self.commands.keys()))
        await ctx.send(f"Availalble SOBot commands are {commands}")
        
    #command to start timer
    @commands.command(name='startsbsw')
    async def start_stopwatch(self, ctx, offset: str = "0"):
        
        #access level check. use this in all commands and edit access_level as appropriate
        access_level = "vipPlus" #set access level to "anyone", "vipPlus", "modPlus", "streamer"
        if not self.has_access(ctx, access_level):
            text = self.state.validAccessLevels[access_level]["accessText"]
            await ctx.send(f"@{ctx.author.name} Only {text} can use this command")
            print(f"{ctx.author.name} not authorised for command")
            return
        
        if self.state.activeStopwatch:
            await ctx.send(f"@{ctx.author.name} Stopwatch already active")
            return
        
        try:
            offsetSeconds = float(offset)*60
        except KeyError as e:
             formatted_message = f"stopwatch offset error: {e}"
             await ctx.send(f"{formatted_message}")
             self.debug_print(f"stopwatch offset error using {offset}")
             return
        except ValueError as v:
             formatted_message = f"stopwatch offset error: {v}"
             await ctx.send(f"{formatted_message}")
             self.debug_print(f"stopwatch offset error using {offset}")
             return
        
        self.state.stopwatchStart = time.time() - offsetSeconds
        self.state.activeStopwatch = True
        
        await ctx.send(f"Stopwatch started at {datetime.timedelta(seconds=offsetSeconds)}")
        print(f"{ctx.author.name} started a stopwatch")
        
    #command to report current timer duration in chat
    @commands.command(name='sbsw')
    async def stopwatch_duration(self, ctx):
        
        #access level check. use this in all commands and edit access_level as appropriate
        access_level = "anyone" #set access level to "anyone", "vipPlus", "modPlus", "streamer"
        if not self.has_access(ctx, access_level):
            text = self.state.validAccessLevels[access_level]["accessText"]
            await ctx.send(f"@{ctx.author.name} Only {text} can use this command")
            print(f"{ctx.author.name} not authorised for command")
            return
        
        if self.state.activeStopwatch:
            timer = time.time() - self.state.stopwatchStart 
            await ctx.send(f"@{ctx.author.name} The stopwatch has been running for {datetime.timedelta(seconds=timer)}")
            print(f"{ctx.author.name} requested stopwatch elapsed time")
            return
        else:
            await ctx.send(f"@{ctx.author.name} Stopwatch not active")
            print(f"{ctx.author.name} requested inactive stopwatch duration")
            return
        
    @commands.command(name='stopsbsw')
    async def stop_stopwatch(self, ctx):
        
        #access level check. use this in all commands and edit access_level as appropriate
        access_level = "vipPlus" #set access level to "anyone", "vipPlus", "modPlus", "streamer"
        if not self.has_access(ctx, access_level):
            text = self.state.validAccessLevels[access_level]["accessText"]
            await ctx.send(f"@{ctx.author.name} Only {text} can use this command")
            print(f"{ctx.author.name} not authorised for command")
            return
        
        if self.state.activeStopwatch:
            timer = time.time() - self.state.stopwatchStart 
            self.state.activeStopwatch = False
            await ctx.send(f"@{ctx.author.name} Stopwatch stopped. Total time was {datetime.timedelta(seconds=timer)}")
            print(f"{ctx.author.name} requested stopwatch elapsed time")
            return
        else:
            await ctx.send(f"@{ctx.author.name} Stopwatch not active")
            print(f"{ctx.author.name} tried to end an inactive stopwatch")
            return        


            
    #add additional commands after this line
        
        
        
    #add additional commands before this line
        
    async def event_ready(self):
        """Called once when the bot goes online."""
        print(f'Logged in as | {self.nick}')
        # Get the actual connected channels from the bot's client
        connected_channels = [channel.name for channel in self.connected_channels]
        print(f'Connected to channels: {", ".join(connected_channels)}')
        
        # Check if commands are properly registered
        print("Commands available:", list(self.commands.keys()))
        self.state.connected = True
        
        for ch in self.connected_channels:
            await ch.send("SOBot is watching 👺")
        
    async def event_message(self, message):
        """Called when a message is received."""

        # Update message counter for debugging
        self.state.message_count += 1
        self.debug_print(f"\n--- MESSAGE #{self.state.message_count} ---")
        
        # Check if message has author
        if message.author is None:
            self.debug_print("WARNING: Received message with no author")
            self.debug_print(f"Message content: {message.content}")
            self.debug_print("-" * 30)
            return

        
        # Process commands if the message starts with the prefix
        await self.handle_commands(message)
        
        # Get display name and lowercase name    
        display_name = message.author.name.lstrip('@')  # Keep original capitalization for display
        username = display_name.lower()     # Lowercase for comparisons

        # Skip messages from the bot itself to avoid potential loops
        # Check if we have a valid nick attribute and compare it
        if hasattr(self, 'nick') and username == self.nick.lower():
            self.debug_print("Skipping bot's own message")
            return

        channel = message.channel
        game = "some game" #placeholder for recent game functionality or default if no recent game found
        
        
        # Debug info about the message
        self.debug_print(f"Time: {datetime.datetime.now()}")
        self.debug_print(f"From: {display_name} (lowercase: {username})")
        self.debug_print(f"Content: {message.content}")
        self.debug_print(f"Channel: {message.channel.name if message.channel else 'Unknown'}")        
        
        #check if user has already been shouted out this stream
        if username in self.state.already_shouted:
            print(f"{username} has already been shouted out this stream")
            return
        
        #check if user is in shout out list
        if username in self.state.sOList:
            user_entry = self.state.sOList.get(username)
            
            if user_entry != None:
                game = user_entry.get("customGame") or ""
                
            msg = user_entry.get("customSO") or self.state.defaultSO
            
            try:
                formatted_message = msg.format(username=display_name, game=game)
            except KeyError as e:
                formatted_message = f"Shoutout error: missing placeholder {e}. Using default format."
                fallback_msg = f"Check out @{display_name} streaming {game} at http://www.twitch.tv/{display_name}"
                await channel.send(f"{formatted_message}\n{fallback_msg}")
                self.debug_print(f"Bad format string in shoutout for {display_name}: {msg}")
                return
            
            await channel.send(f"{formatted_message}") 
            self.state.already_shouted.add(username)
            
        else:
            self.debug_print(f"{username} not in shoutout list")    
        
        
    def load_shoutouts(self):
        #Load the shoutout list from the JSON file.
        
        filename = f"{self.state.channelname}_sODatabase.json"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(script_dir, filename)
        print(f"{full_path}")
        
        try:
            with open(full_path, 'r', encoding="utf-8") as file:
                shoutouts = json.load(file)
            return shoutouts
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            print("Error decoding the sODatabase.json file!")
            return {}        
        
    def save_shoutouts(self):
        """Save the shoutout list to the JSON file."""
        
        filename = f"{self.state.channelname}_sODatabase.json"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(script_dir, filename)
        print(f"{full_path}")
        
        with open(full_path, 'w', encoding="utf-8") as file:
            json.dump(self.state.sOList, file, indent=4)   
    
    #class for enabling and disabling debug prints
    def debug_print(self, *args, **kwargs):
        if self.state.debug:
            print(*args, **kwargs)
    
    #check if user is allowed to use something
    def has_access(self, ctx, accessLevel):
        if not accessLevel in self.state.validAccessLevels:
            print(f"{ctx.author.name} invalid access level defined")
            return
        
        if accessLevel == "anyone":
            return True
        elif accessLevel == "modPlus":
            return (
                ctx.author.is_mod or
                ctx.author.name.lower() == ctx.channel.name.lower()
            )
        elif accessLevel == "vipPlus":
            badges = ctx.author.badges or {}
            return (
                ctx.author.is_mod or
                ctx.author.name.lower() == ctx.channel.name.lower() or
                'vip' in badges
            )
        elif accessLevel == "streamer":
            return (
                ctx.author.name.lower() == ctx.channel.name.lower()
            )
        else:
            print("access level error")
            return False           
            
            
if __name__ == "__main__":
    bot = SOBot()
    bot.run()