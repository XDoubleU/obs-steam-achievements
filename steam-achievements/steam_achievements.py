from os import remove
import time, grequests, requests, logging, math

def calculate_percentage(achievements):
    total = len(achievements)
    achieved = 0

    for achievement in achievements:
        achieved += achievement["achieved"]
    
    return round((achieved/total)*100, 2)

def get_steam_achievements(api_key, steam_id):
    start_time = time.time()

    #include_free_games didn't look necessary when building this
    #owned_games = requests.get("https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key="+api_key+"&steamid="+steam_id+"&include_played_free_games=true").json()["response"]["games"]
    owned_games = requests.get("https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key="+api_key+"&steamid="+steam_id).json()["response"]["games"]

    # create request urls
    urls = []
    for game in owned_games:
        urls.append("https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/?key="+api_key+"&steamid="+steam_id+"&appid="+str(game["appid"]))

    # request stuff
    rs = (grequests.get(u) for u in urls)
    responses = grequests.map(rs)

    game_achievements = {}

    for response in responses:
        game_stats = response.json()["playerstats"]

        if "achievements" in game_stats:
            game_percentage = calculate_percentage(game_stats["achievements"])
            game_achievements[game_stats["gameName"]] = game_percentage
    
    logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.INFO)
    logging.info("Gathered achievement info for "+str(len(owned_games))+" games in "+str(time.time() - start_time)+" seconds")
    return game_achievements

def get_real_completion(game_achievements):
    total_percentage = sum(game_achievements.values())
    return round((total_percentage/len(game_achievements)), 2)

def get_steam_completion(game_achievements):
    # https://steamcommunity.com/sharedfiles/filedetails/?id=650166273
    total_percentage = sum(game_achievements.values())
    started_games = 0
    for i in range(0, len(game_achievements)):
        if list(game_achievements.values())[i] != 0:
            started_games+=1

    return math.floor(total_percentage/started_games)