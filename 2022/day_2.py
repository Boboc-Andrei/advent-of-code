#   opp player
#   A = X =     Rock
#   B = Y =     Papper
#   C = Z =     Scissors

matches = []
default_scores = {'X':1,'Y':2,'Z':3}
always_win_dict = {
    'A': {'X':3, 'Y':6, 'Z':0},
    'B': {'X':0, 'Y':3, 'Z':6},
    'C': {'X':6, 'Y':0, 'Z':3}
}

#       L      D      W       (lose,draw,win)
choose_outcome_dict = {
    'A' : {'X':3, 'Y':1, 'Z':2},   # choose_outcome_dict[game_outcome_for_player][opponent input] = score of needed move
    'B' : {'X':1, 'Y':2, 'Z':3},
    'C' : {'X':2, 'Y':3, 'Z':1}
}
choose_outcome_defaults = {'X':0,'Y':3,'Z':6}



with open('input_2.txt','r') as f:
    matches = [line.rstrip().split() for line in f]

total_winning_score = 0
total_choosing_score = 0

for match in matches:
    opponent, player = match

    winning_score = default_scores[player] + always_win_dict[opponent][player]
    choosing_score = choose_outcome_defaults[player] + choose_outcome_dict[opponent][player]
    total_winning_score += winning_score
    total_choosing_score += choosing_score

print(f'score when winning every round: {total_winning_score}')
print(f'score when choosing wether to win every round: {total_choosing_score}')




