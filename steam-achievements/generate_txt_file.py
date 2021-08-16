import steam_achievements, math

def _generate_values(achievements, game, amount_of_games):
    current_game = game

    if game != None:
        current_game_completion = achievements[game]
    else:
        current_game_completion = None

    steam_completion = steam_achievements.get_steam_completion(achievements)
    real_completion = steam_achievements.get_real_completion(achievements)

    completed_games = 0
    for key, value in dict(achievements).items():
        if value == 100:
            completed_games += 1
            achievements.pop(key)
        else:
            break
    
    return [current_game, current_game_completion, steam_completion, real_completion, completed_games, dict(list(achievements.items())[:amount_of_games])]

def _generate_strings(values, width_of_games):
    if values[0] == None:
        current_game = ""
        current_game_completion = ""
    else:
        current_game = values[0]
        current_game_completion = _progress_bar(values[1]) + " - " + str('{:.2f}'.format(values[1]) + "%")
    
    steam_completion = _progress_bar(values[2]) + " - " + str('{:.2f}'.format(values[2]) + "%")
    real_completion = _progress_bar(values[3]) + " - " + str('{:.2f}'.format(values[3]) + "%")
    completed_games = str(values[4])
    
    highest_ranked_games = ""
    games = values[5]
    for index in range(0, len(games)):
        if len(list(games.keys())[index]) > width_of_games:
            name = list(games.keys())[index][:width_of_games - 5] + "...  "
        elif len(list(games.keys())[index]) < width_of_games:
            name = list(games.keys())[index] + " "*(width_of_games-len(list(games.keys())[index]))
        else:
            name = list(games.keys())[index]

        game_completion = list(games.values())[index]
        highest_ranked_games += name + ": " + _progress_bar(game_completion) + " - " + str('{:.2f}'.format(game_completion)) + "%\n"

    return [current_game, current_game_completion, steam_completion, real_completion, completed_games, highest_ranked_games]

def _progress_bar(value):
    # 10 blocks => 1 per 10%
    return "#"*math.floor(value/10) + " "*(10 - math.floor(value/10))

def _replace_output_template(output_template, string_array):
    # string_array = [current_game, current_game_completion, steam_completion, real_completion, completed_games, highest_ranked_games]

    output_template = output_template.replace("#current_game#", string_array[0])
    output_template = output_template.replace("#current_game_completion#", string_array[1])
    output_template = output_template.replace("#steam_completion#", string_array[2])
    output_template = output_template.replace("#real_completion#", string_array[3])
    output_template = output_template.replace("#completed_games#", string_array[4])
    output_template = output_template.replace("#highest_ranked_games#", string_array[5])

    return output_template

def generate_txt_file(achievements, current_game, output_template, amount_of_games, width_of_games):
    sorted_achievements = dict(sorted(achievements.items(), key=lambda item: item[1], reverse=True))

    values = _generate_values(sorted_achievements, current_game, amount_of_games)
    strings = _generate_strings(values, width_of_games)
    
    file = open("achievements.txt","wb")
    file.write(_replace_output_template(output_template, strings).encode('utf8'))
    file.close()

