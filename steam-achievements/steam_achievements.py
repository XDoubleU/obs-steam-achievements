from os import remove
import time, grequests, requests, logging, math

def _get_achieved_achievements(achievements):
    result = 0

    for achievement in achievements:
        result += achievement["achieved"]

    return result

def _get_total_achievements(achievements):
    return len(achievements)

def _get_game_completion(game):
    return (game[0]/game[1])*100

def get_steam_achievements(api_key, steam_id):
    start_time = time.time()

    owned_games = requests.get("https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key="+api_key+"&steamid="+steam_id+"&include_played_free_games=true").json()["response"]["games"]

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
            achieved_achievements = _get_achieved_achievements(game_stats["achievements"])
            total_achievements = _get_total_achievements(game_stats["achievements"])
            game_achievements[game_stats["gameName"]] = _get_game_completion([achieved_achievements, total_achievements])
    
    logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.INFO)
    logging.info("Gathered achievement info for "+str(len(owned_games))+" games in "+str(time.time() - start_time)+" seconds")
    return dict(sorted(game_achievements.items(), key=lambda item: item[0].lower()))

def get_steam_completion(game_achievements):
    # https://steamcommunity.com/sharedfiles/filedetails/?id=650166273
    
    total_percentage = sum(game_completion for game_completion in game_achievements.values() if round(game_completion) is not 0)
    started_games = sum(1 for game_completion in game_achievements.values() if round(game_completion) is not 0)

    return math.floor((total_percentage/started_games))

def get_real_completion(game_achievements):
    total_percentage = sum(game_completion for game_completion in game_achievements.values())
    total_games = len(game_achievements)

    return round((total_percentage/total_games), 2)