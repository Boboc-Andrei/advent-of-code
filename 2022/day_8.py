
with open('input_8.txt','r') as f:
    forest = []
    for line in f:
        forest.append([int(tree) for tree in line.rstrip()])


rows = len(forest)
cols = len(forest[0])

visibility = [[False for _ in range(cols)] for _ in range(rows)]

left_visible = [-1 for _ in range(rows)]
right_visible = left_visible.copy()

top_visible = [-1 for _ in range(cols)]
bot_visible = top_visible.copy()


for i in range(rows):
    for j in range(cols):

        # check if trees in row are visible from the top
        if forest[i][j] > top_visible[j]:
            top_visible[j] = forest[i][j]
            visibility[i][j] = True
        
        # check if trees in row are visible from the bottom
        if forest[-i-1][j] > bot_visible[j]:
            bot_visible[j] = forest[-i-1][j]
            visibility[-i-1][j] = True

        # check if trees in row are visible from the left
        if forest[i][j] > left_visible[i]:
            left_visible[i] = forest[i][j]
            visibility[i][j] = True
           
        # check if trees in row are visible from the right
        if forest[i][-j-1] > right_visible[i]:
            right_visible[i] = forest[i][-j-1]
            visibility[i][-j-1] = True

print(sum(sum(row) for row in visibility))


row = [3,0,3,7,3]
right_visibility = [0,0,0,0,0]
stack = []

for i in range(len(row)):
    while stack and row[i] >= stack[-1][1]:
        idx,x = stack.pop()
        right_visibility[idx] = i-idx 
    stack.append((i,row[i]))
    
while stack:
    idx, x = stack.pop()
    right_visibility[idx] = len(row)-idx-1

#print(right_visibility)


left_visibility = [[0 for _ in range(rows)] for _ in range(cols)]
right_visibility = [[0 for _ in range(rows)] for _ in range(cols)]
top_visibility = [[0 for _ in range(rows)] for _ in range(cols)]
bot_visibility = [[0 for _ in range(rows)] for _ in range(cols)]
overall_visibility = [[0 for _ in range(rows)] for _ in range(cols)]
left_stack, right_stack, top_stack, bot_stack = [],[],[],[]

for i in range(rows):
    for j in range(cols):

        # compute how many trees are visible to the RIGHT of each tree
        while right_stack and forest[i][j] >= right_stack[-1][1]:
            col,tree = right_stack.pop()
            right_visibility[i][col] = j-col
        right_stack.append((j,forest[i][j]))

        # compute how many trees are visible to the LEFT of each tree
        while left_stack and forest[i][-j-1] >= left_stack[-1][1]:
            col, tree = left_stack.pop()
            left_visibility[i][-col-1] = j-col
        left_stack.append((j,forest[i][-j-1]))

    # default values for leftover trees on the RIGHT
    while right_stack:
        col,tree = right_stack.pop()
        right_visibility[i][col] = cols-col-1
    # default values for leftover trees on the LEFT
    while left_stack:
        col,tree = left_stack.pop()
        left_visibility[i][-col-1] = cols-col-1

for j in range(cols):
    for i in range(rows):

        # compute how many trees are visible BELOW each tree
        while bot_stack and forest[i][j] >= bot_stack[-1][1]:
            row,tree = bot_stack.pop()
            bot_visibility[row][j] = i-row
        bot_stack.append((i,forest[i][j]))

        # compute how many trees are visible ABOVE each tree
        while top_stack and forest[-i-1][j] >= top_stack[-1][1]:
            row,tree = top_stack.pop()
            top_visibility[-row-1][j] = i-row
        top_stack.append((i,forest[-i-1][j]))
    
    while bot_stack:
        row,tree = bot_stack.pop()
        bot_visibility[row][j] = rows-row-1

    while top_stack:
        row,tree = top_stack.pop()
        top_visibility[-row-1][j] = rows-row-1

        

for i in range(rows):
    for j in range(cols):
        overall_visibility[i][j] = left_visibility[i][j] * right_visibility[i][j] * top_visibility[i][j] * bot_visibility[i][j]

print('LEFT visibility:')
[print(row) for row in left_visibility]
print('\nRIGHT visibility:')
[print(row) for row in right_visibility]
print('\nABOVE visibility:')
[print(row) for row in top_visibility]
print('\nBELOW visibility:')
[print(row) for row in bot_visibility]
print('\nOVERALL visibility:')
[print(row) for row in overall_visibility]




print()

best_bisibility = print(max([max(row) for row in overall_visibility]))

best_visibility, row,col = max([(tree,i,j) for j, (tree,i) in enumerate([(max(row),i) for i, row in enumerate(overall_visibility)])])

print(f'tree with best visibility of {best_visibility} at position ({row},{col})')
