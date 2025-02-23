
with open('input_4.txt', 'r') as f:
    cards = []
    for card in f:
        card = card.rstrip().split(':')[1].split('|')
        card[0] = card[0].split()
        card[1] = card[1].split()
        cards.append(card)


cumulative_winnings = [{'copies':1,'winnings':0} for _ in range(len(cards))]

total_winnings = 0
for i, card in enumerate(cards):
    winning_count = 0
    winning,actual = card
    for number in actual:
        if number in winning:
            winning_count+=1
    
    current_winnings = 2**(winning_count-1)
    cumulative_winnings[i]['winnings'] = winning_count
    if winning_count:
        total_winnings += current_winnings

print(total_winnings)

#=========PART 2==============

total_cumulative_tickets = 0
for i, card in enumerate(cumulative_winnings):
    copies, winnings = card['copies'], card['winnings']
    for j in range(i+1,i+1+winnings):
        cumulative_winnings[j]['copies']+=copies

    total_cumulative_tickets += copies

print(total_cumulative_tickets)