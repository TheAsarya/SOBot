=><==><==><==><==><==><==><==><==><==><==><==><==><==><==><==><=
    
    Twitch chat bot by TheAsarya with assistance from ChatGPT and Claude AI
    
    Main functionality summary
    - automatically shouts out users who are on a list when they post their
        first message of the stream
    - users can have custom shoutouts or if they don't they'll get the default
    - users can be added to the list via command
    - users' custom shoutouts can be added or edited via command
    - users can be removed from the list via command
    
    
=><==><==><==><==><==><==><==><==><==><==><==><==><==><==><==><=

    Installation instructions Windows
    
    1. Install python from python.org i've used v3.13.3 and v3.12.2
    2. add python to path and env in your Windows environment if doesn't do it
        automatically. you can check by entering "python --version" in a 
        terminal window (run cmd when from windows search) 
    3. Install necessary python packages via "pip install your_package_here" in
        a terminal window
        a) twitchio
        b) python-dotenv
    4. get SOBot project files and put them in a folder on your PC
    5. edit the following in the project files 
        a) choose the twitch account SOBot will use (an account that is 
            not the one you're streaming from is preferable) and get a bot 
            access token for it from https://twitchtokengenerator.com/ if you 
            don't have one. Then in the file .env.example replace the 
            placeholder with your bot's access token. Then rename the file to 
            .env
            
            N.B. Don't share your access tokens with anyone
            
        b) In SOBot.py, find the line 
            "self.channelname = "theasarya" and replace whatever is between the
            inner quotation marks with your twitch channel username in lower 
            case 
        c) This would be a good time to edit the default shoutout as described
            in the customisation section below
    5. open a terminal window (go to the windows search box and type cmd)
    6. Navigate to your SOBot folder in your terminal window then enter 
        "python sobot.py" to run the bot
    7. Make the bot a mod in your channel
    8. try a command like !hellosb in chat to check if it's responding properly
        Click into the terminal window and hit ctrl+c to stop the bot
    9. Once you're confident it's working you can edit the bat file. 
         Put the bat file somewhere convenient like your desktop. Open the bat
         file for editing and replace the path to SOBot.py with the path
         to whichever version of sobot you're using
    10. double click the bat file to run the bot
    11. Once you're confident that the bot is running correctly you can set
         the line self.debug = False in SOBot.py to have less information 
         printing to the terminal window when the bot's running
    
        
=><==><==><==><==><==><==><==><==><==><==><==><==><==><==><==><=

    Commands
    -------------------------
    !addsbso [username] [custom_shoutout - optional]
    
        adds a user to the shoutout list. optionally adds a custom shoutout
    
    -------------------------
    !editsbso [username] [custom_shoutout]
    
        adds a custom shoutout to a user if they're already in the shoutout list'
        use with caution. this will overwrite any existing custom shoutout
    
    -------------------------
    !hellosb
    
        say hello to the bot so you can check if it's running
    
    -------------------------
    !sbso [username]
    
        manual shoutout to a user if they're in the shoutout list. 
        will use custom shoutout if available. otherwise will use default message
    
    -------------------------
    !removesbso [username]
    
        remove user from shoutout list
        intended mainly for if a user is added with a typo in their name etc.
        use with caution
    
    -------------------------
    !resetsbshouted
    
        resets the already shouted list which tracks who on the list 
        has already had an automated shoutout this stream (since the 
        bot was restarted or this command was last used)
    
    -------------------------
    !sbcommands
    
        lists available SOBot commands in chat
        
    -------------------------
    !startsbsw [optional = offset in minutes]
    
        starts a stopwatch. optional offest lets you start the timer from 
        e.g. two minutes ago by doing "!startsbtimer 2"
        
    -------------------------
    !sbsw
    
        report the current duration of the stopwatch in chat, if the stopwatch
        is active
        
    -------------------------
    !stopsbsw
    
        stops the stopwatch, if there's one active, and reports the total
        duration in chat
    
        
        
        
=><==><==><==><==><==><==><==><==><==><==><==><==><==><==><==><=

    Customisation
    
    - customise your default shoutout message in the line "self.defaultSO =" 
        Remember to use {user} and {game} variables in it if you want these to
        be generated dynamically
    - in addition to using the commands, sODatabase.json can be edited directly to 
        add users and custom shoutouts etc. to the list as long as you 
        maintain the text formatting and ensure that you save it in utf-8 
        format. Otherwise unicode emojis will probably stop working
    - it might be a good idea to backup your sODatabase.json file 
        occasionally
    - there's a section marked in comments in SOBotx_y.py for you to add
        your own commands. They may fail to register if defined further 
        down in the code. It looks like this
        
            #add additional commands after this line
                
                
                
            #add additional commands before this line
            
=><==><==><==><==><==><==><==><==><==><==><==><==><==><==><==><=

    Changelog
    
    v0_5 fixed bug when running from remote batch. new version always looks in 
        sobotx_y.py folder for appropriate .json file
    v0_4 test release            
