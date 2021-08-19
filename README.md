# Steam Achievements script for OBS Studio
This script generates a customizable text-file containing:
- Your current game and completion percentage
- Your steam average achievement completion percentage
- Your real average achievement completion percentage
- Your top 10 games in achievement completion percentages

All of these come with a progress bar and percentage

![Example image](https://github.com/XDoubleU/obs-steam-achievements/blob/main/example.PNG)
![Example image](https://github.com/XDoubleU/obs-steam-achievements/blob/main/example-config.PNG)

## How to install and configure?
1. Download the latest release.
2. Unzip this and move the "steam-achievements" folder into your OBS Studio plugins folder.
3. Open OBS Studio and in the top menu go to "Tools">"Scripts", make sure your Python path is entered in settings (https://www.youtube.com/watch?v=t7RhpvlVte0) and add "main_script.py" to your scripts.
4. Enter Steam Web API-Key (request here: https://steamcommunity.com/dev/apikey; you can enter any domain).
5. Enter Steam Id (use steamid64 from this url: www.steamidfinder.com; enter your profile-url).
   Side note: I know that some profile-urls already contain the steam id but I'm writing a work-for-all method here :)
6. Add a Text Source and select "Read from file".
7. Browse for the text file and pick "achievements.txt" in your OBS Studio bin folder.
8. A monospace font is required/recommended (otherwise the lay-out will be messy), but that's up to you.
