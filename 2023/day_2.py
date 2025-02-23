
with open('input_2.txt', 'r') as f:
    games = []
    for line in f:
        line = line.rstrip().split(':')[1].split(';')
        game = []
        for game_round in line:
            game_round = game_round.strip().split(',')
            game_round = [(color,int(number)) for number,color in [selection.split() for selection in game_round]]
            game.append(game_round)
        games.append(game)



#============PART 1 ==============
color_amounts = {
    'red':12,
    'green':13,
    'blue':14
}
fair_games_sum = 0

for idx, game in enumerate(games):
    game_is_fair = True
    for game_round in game:
            
        if game_is_fair:
            for selection in game_round:
                color,number = selection
                if number > color_amounts[color]:
                    game_is_fair = False
                    break
        else:
            break
    
    if game_is_fair:
        fair_games_sum += idx+1
print(fair_games_sum)

#===========PART 2 ==============

total_power = 0
for game in games:
    minimum_colors = {'red':0,'green':0,'blue':0}
    for game_round in game:
        for selection in game_round:
            color,number = selection
            minimum_colors[color] = max(minimum_colors[color], number)
    
    cube_power = 1
    for color in minimum_colors:
        cube_power *= minimum_colors[color]
    total_power += cube_power

print(total_power)



