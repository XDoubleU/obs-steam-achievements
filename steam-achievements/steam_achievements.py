import time, grequests, requests, logging, math, os.path

def _get_games_without_achievements():
    result = []

    if os.path.isfile("games_without_achievements.txt"):
        f = open("games_without_achievements.txt", "r")
        lines = f.readlines()

        for line in lines:
            result.append(line.replace("\n", ""))
            
        f.close()

    return result

def _save_game_without_achievements(game_name):
    if game_name not in _get_games_without_achievements():
        f = open("games_without_achievements.txt", "a")
        f.write(game_name + "\n")
        f.close()

def _filter_games_without_achievements(games):
    result = []
    games_without_achievements = _get_games_without_achievements()

    for game in games:
        # check if game has stats
        if "has_community_visible_stats" not in game:
            _save_game_without_achievements(game["name"])

        if game["name"] not in games_without_achievements:
            result.append(game)
    
    return result

def _get_completed_games():
    result = []

    if os.path.isfile("completed_games.txt"):
        f = open("completed_games.txt", "r")
        lines = f.readlines()

        for line in lines:
            result.append(line.strip())
            
        f.close()

    return result

def _save_completed_game(game_name):
    if game_name not in _get_completed_games():
        f = open("completed_games.txt", "a")
        f.write(game_name + "\n")
        f.close()

def _filter_completed_games(games):
    result = {}
    completed_games = _get_completed_games()

    ready_for_removal = []
    for i in range(0, len(games)):
        if games[i]["name"] in completed_games:
            ready_for_removal.append(i)
            result[games[i]["name"]] = 100
    
    for index in ready_for_removal:
        games.pop(index)

    return result

def _get_achieved_achievements(achievements):
    result = 0

    for achievement in achievements:
        result += achievement["achieved"]

    return result

def _get_total_achievements(achievements):
    return len(achievements)

def _get_game_completion(game):
    return (game[0]/game[1])*100

def get_current_game(api_key, steam_id):
    player_summary = requests.get("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key="+api_key+"&steamids="+steam_id).json()["response"]["players"][0]
    
    if "gameid" in player_summary:
        return player_summary["gameextrainfo"]
    else:
        return None

def get_steam_achievements(api_key, steam_id):
    game_achievements = {}

    start_time = time.time()

    owned_games = requests.get("https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key="+api_key+"&steamid="+steam_id+"&include_played_free_games=true&include_appinfo=true").json()["response"]["games"]
    
    # remove games without achievements
    owned_games = _filter_games_without_achievements(owned_games)

    # remove completed games and add these to game_achievements
    game_achievements = _filter_completed_games(owned_games)

    # create request urls
    urls = []
    for game in owned_games:
        urls.append("https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v1/?key="+api_key+"&steamid="+steam_id+"&appid="+str(game["appid"]))

    # request stuff
    rs = (grequests.get(u) for u in urls)
    responses = grequests.map(rs)

    for response in responses:
        game_stats = response.json()["playerstats"]

        if "achievements" in game_stats:
            achieved_achievements = _get_achieved_achievements(game_stats["achievements"])
            total_achievements = _get_total_achievements(game_stats["achievements"])
            game_completion = _get_game_completion([achieved_achievements, total_achievements])

            if game_completion == 100:
                _save_completed_game(game_stats["gameName"])

            game_achievements[game_stats["gameName"]] = game_completion

        elif "gameName" in game_stats:
            _save_game_without_achievements(game_stats["gameName"])
    
    logging.basicConfig(filename='app.log', filemode='a', format='%(asctime)s - %(message)s', level=logging.INFO)
    logging.info("Gathered achievement info for "+str(len(owned_games))+" games in "+str(time.time() - start_time)+" seconds")
    return dict(sorted(game_achievements.items(), key=lambda item: item[0].lower()))

def get_steam_completion(game_achievements):
    # https://steamcommunity.com/sharedfiles/filedetails/?id=650166273
    
    total_percentage = sum(game_completion for game_completion in game_achievements.values() if round(game_completion) != 0)
    started_games = sum(1 for game_completion in game_achievements.values() if round(game_completion) != 0)

    return math.floor((total_percentage/started_games))

def get_real_completion(game_achievements):
    total_percentage = sum(game_completion for game_completion in game_achievements.values())
    total_games = len(game_achievements)

    return round((total_percentage/total_games), 2)