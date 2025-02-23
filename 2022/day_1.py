elves = []
current_elf = []
max_calories = 0
with open('input_1.txt','r') as f:
    for line in f:
        line = line[:-1]
        if line == '':
            elves.append(current_elf)
            current_elf = []
        else:
            current_elf.append(int(line))
            

elf_total_calories = []

for i, elf in enumerate(elves):
    elf_calories = sum(elf)
    elf_total_calories.append((i,elf_calories))

    if elf_calories > max_calories:
        max_calories = elf_calories

print(f'elf with max calories: {max_calories}')

sorted_elf_calories = sorted(elf_total_calories, key = lambda elf: elf[1], reverse=True)

print(sum(map(lambda elf: elf[1],sorted_elf_calories[:3])))