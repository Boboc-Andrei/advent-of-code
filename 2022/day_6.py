with open('input_6.txt','r') as f:
    message = f.readline().rstrip()



marker_length = 14

marker = {}
for i in range(marker_length-1):
    if message[i] not in marker:
        marker[message[i]] = 1
    else:
        marker[message[i]] += 1

for i in range(marker_length-1,len(message)):
    letter = message[i]
    oldest_letter = message[i-(marker_length-1)]

    if letter not in marker:
        marker[letter] = 1
    else:
        marker[letter] += 1
    
    if len(marker) == marker_length:
        print(i+1)
        break

    if marker[oldest_letter] == 1:
        del marker[oldest_letter]
    else:
        marker[oldest_letter] -= 1
