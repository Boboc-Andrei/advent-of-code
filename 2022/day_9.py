with open('input_9.txt','r') as f:
    movements = []
    for line in f:
        direction, distance = line.rstrip().split()
        distance = int(distance)
        movements.append([direction, distance])
    
n_knots = 9
knots = [(0,0) for _ in range(n_knots)]
head_poz = (0,0)

tail_visited = {(0,0):True}

#   maps direction letters to vectors
directions = {
    'U': (-1,0),
    'D': (1,0),
    'L': (0,-1),
    'R': (0,1),
}

def move(a,b):
    '''
    adds movement vector y to position vector x
    '''
    xa,ya = a
    xb,yb = b
    return (xa+xb, ya+yb)

def get_distance(a,b):
    xa,ya = a
    xb,yb = b
    return (abs(xa-xb), abs(ya-yb))

def get_dir(a,b):
    xa,ya = a
    xb,yb = b
    dx = 0 if xa-xb == 0 else abs(xa-xb)/(xa-xb)
    dy = 0 if ya-yb == 0 else abs(ya-yb)/(ya-yb)
    return (dx,dy)

for movement in movements:
    direction,distance = movement
    direction = directions[direction]

    for _ in range(distance):
        head_poz = move(head_poz,direction)
        destination = head_poz
        for i, knot in enumerate(knots):

            tail_distance = get_distance(destination,knot)
            tail_dir = get_dir(destination,knot)

            if 2 in tail_distance:
                knot = move(knot,tail_dir)
                knots[i] = knot
            
            destination = knot
            tail_visited[knots[-1]] = True



print(len(tail_visited))