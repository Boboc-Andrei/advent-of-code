
with open('input_10.txt', 'r') as f:
    inputs = []
    for line in f:
        line = line.strip().split()
        if len(line) > 1:
            line[1] = int(line[1])
        inputs.append(line)


X = 1
cycles = 0
total_signal_strength = 0
cycle_target = 40
image = []
row = ''

def get_character_to_draw(X,cycle):
    return '#' if X in range(cycle-1,cycle+2) else ' '

total_characters = 0

for idx, line in enumerate(inputs):
    if line[0] == 'noop':
        total_characters+=1
        if cycles == cycle_target:
            total_signal_strength += X*cycle_target
            image.append(row)
            row = ''
            cycles = 0
        row += get_character_to_draw(X, cycles)
        cycles += 1
    else:
        total_characters+=2
        '''if cycles+2 >= cycle_target:
            total_signal_strength += X*cycle_target
            cycle_target += 40
        '''
        for _ in range(2):
            if cycles == cycle_target:
                total_signal_strength += X*cycle_target
                image.append(row)
                row = ''
                cycles = 0
            row += get_character_to_draw(X, cycles)
            cycles+=1
        X += line[1]

print(total_characters/4)

image.append(row)
for line in image:
    print(line, len(line))

#   REHPRLUB