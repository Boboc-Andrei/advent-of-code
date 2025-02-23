
with open('input_3.txt','r') as f:
    schematic = [[c for c in line.rstrip()] for line in f]


rows = len(schematic)
cols = len(schematic[0])
numbers = '0123456789'
relevant_fields = [[False for _ in range(cols)] for _ in range(rows)]

for row in range(rows):
    for col in range(cols):
        if schematic[row][col] not in numbers and schematic[row][col] != '.':
            for r in range(row-1,row+2):
                for c in range(col-1,col+2):
                    try:
                        relevant_fields[r][c] = True
                    except:
                        pass
        

total_nums = 0
for row in range(rows):
    current_number = 0
    current_digit = 0
    is_relevant = False
    for col in range(cols-1,-1,-1):
        if schematic[row][col] in numbers:
            current_number += int(schematic[row][col]) * 10**current_digit
            current_digit+=1
            is_relevant = is_relevant or relevant_fields[row][col]
        else:
            if is_relevant:
                total_nums += current_number
            current_digit = 0
            current_number = 0
            is_relevant = False
    if is_relevant:
        total_nums += current_number


print(total_nums)

#========PART 2 ===========

