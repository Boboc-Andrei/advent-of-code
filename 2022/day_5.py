with open('input_5.txt','r') as f:
    stacks = []
    operations = []
    for line in f:
        if line[0] == '[':
            stacks.append(line[:-1])
        else:
            operations.append(line.rstrip())

crate_stacks = [[] for _ in range((len(stacks[0])+1)//4)]
for line in stacks[::-1]:
    for idx, c in enumerate(line):
        if c == '[':
            crate_stacks[idx//4].append(line[idx+1])

print('INITIAL STACKS :')
for idx, stack in enumerate(crate_stacks):
    print(f'crate {idx+1} : {[f"[{item}]" for item in stack]}')
operations = operations[2:]

for idx, operation in enumerate(operations):
    operation = operation.split()
    number_to_move = int(operation[1])
    initial_stack = int(operation[3])-1
    destination_stack = int(operation[5])-1
    
    # part 1
    '''
    for _ in range(number_to_move):
        crate_stacks[destination_stack].append(crate_stacks[initial_stack].pop())
    '''
    # part 2
    boxes_moved = []
    for _ in range(number_to_move):
        boxes_moved.append(crate_stacks[initial_stack].pop())
    crate_stacks[destination_stack].extend(boxes_moved[::-1])



top_boxes = ''
print('FINAL STACKS :')
for idx, stack in enumerate(crate_stacks):
    print(f'crate {idx+1} : {[f"[{item}]" for item in stack]}')
    top_boxes += stack[-1]
print(top_boxes)