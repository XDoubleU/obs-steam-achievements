import steam_achievements, math

def progress_bar(value):
    # 10 blocks => 1 per 10%
    return "#"*math.floor(value/10) + " "*(10 - math.floor(value/10))

def generate_txt_file(achievements):
    sorted_achievements = dict(sorted(achievements.items(), key=lambda item: item[1], reverse=True))

    steam_completion = steam_achievements.get_steam_completion(sorted_achievements)
    real_completion = steam_achievements.get_real_completion(sorted_achievements)
    completed_games = 0

    for key, value in dict(sorted_achievements).items():
        if value == 100:
            completed_games += 1
            sorted_achievements.pop(key)
        else:
            break

    file = open("achievements.txt","wb")

    file.write(("Steam Completion: " + progress_bar(steam_completion) + " - " + str('{:.2f}'.format(steam_completion)) + "%\n").encode('utf8'))
    file.write(("Real  Completion: " + progress_bar(real_completion) + " - " + str('{:.2f}'.format(real_completion)) + "%\n").encode('utf8'))
    file.write(("Completed Games : " + str(completed_games) + "\n\n").encode('utf8'))
    file.write(("Highest Ranked  : \n").encode('utf8'))

    for index in range(0, 10):
        if len(list(sorted_achievements.keys())[index]) > 16:
            name = list(sorted_achievements.keys())[index][:12] + "... "
        elif len(list(sorted_achievements.keys())[index]) < 16:
            name = list(sorted_achievements.keys())[index] + " "*(16-len(list(sorted_achievements.keys())[index]))
        else:
            name = list(sorted_achievements.keys())[index]

        game_completion = list(sorted_achievements.values())[index]
        file.write((name + ": " + progress_bar(game_completion) + " - " + str('{:.2f}'.format(game_completion)) + "%\n").encode('utf8'))

    file.close()

achievements = steam_achievements.get_steam_achievements("2388D55D6F0B0FD21D7EC8A15F1D3C05", "76561198127953838")
generate_txt_file(achievements)

