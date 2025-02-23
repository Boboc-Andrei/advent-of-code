import ast
import json

input = []
right_order_counter = 0

with open("input_13.txt", 'r') as f:
    for line in f:
        line = line.strip()
        if(len(line) != 0):
            input.append(json.loads(line))

def compare_packets(left: list|int, right: list|int) -> int:
    stack = [(left, right)]
    
    while stack:
        left, right = stack.pop()
        
        print(f"COMPARING PAIR {idx//2+1}: {left} AND {right}")
        
        if(isinstance(left, int) and isinstance(right, int)):
            if(left < right):
                print(f"END: {left} < {right} ORDERED CORRECTLY\n")
                return 1
            if(left > right):
                print(f"END: {left} > {right} ORDERED INCORRECTLY\n")
                return -1
        else:
            if(isinstance(left, int)): 
                print(f"LEFT IS INT {left} -> [{left}]")
                left = [left]
            elif(isinstance(right, int)):
                print(f"RIGHT IS INT {right} -> [{right}]")
                right = [right]
            
            stack.append((len(left), len(right)))
            
            i = 0
            to_compare = []
            while(i < len(left) and i < len(right)):
                to_compare.append((left[i], right[i]))
                i += 1
            to_compare.reverse()
            stack.extend(to_compare)
    return 0

for idx in range(0, len(input), 2):
    if(compare_packets(input[idx], input[idx+1]) == 1):
        right_order_counter += idx//2 + 1
        
print(f"sum of indexes of correct pairs: {right_order_counter}")

#====================PART 2==============================

separator1 = [[2]]
separator2 = [[6]]
separator1_rank = 1
separator2_rank = 1

if(compare_packets(separator1, separator2) == 1):
    separator2_rank += 1
else:
    separator1_rank += 1

for packet in input:
    if(compare_packets(packet, separator1) == 1):
        separator1_rank += 1
    if(compare_packets(packet, separator2) == 1):
        separator2_rank += 1

print(f"Separator ranks: {separator1_rank} * {separator2_rank} = {separator1_rank * separator2_rank}")