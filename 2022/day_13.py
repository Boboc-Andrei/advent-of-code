import ast
import json

input = []
right_order_counter = 0

with open("input_13.txt", 'r') as f:
    for line in f:
        line = line.strip()
        if(len(line) != 0):
            input.append(json.loads(line))

for idx in range(0, len(input), 2):
    stack = [(input[idx], input[idx+1])]
    
    while stack:
        left, right = stack.pop()
        
        print(f"COMPARING PAIR {idx//2+1}: {left} AND {right}")
        
        if(isinstance(left, int) and isinstance(right, int)):
            if(left < right):
                print(f"END: {left} < {right} ORDERED CORRECTLY\n")
                right_order_counter += idx//2 + 1
                break
            if(left > right):
                print(f"END: {left} > {right} ORDERED INCORRECTLY\n")
                break
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
            


print(f"sum of indexes of correct pairs: {right_order_counter}")