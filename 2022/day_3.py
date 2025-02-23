

with open('input_3.txt','r') as f:
    backpacks = [line.rstrip() for line in f]

priority_scores = [(letter,ord(letter)-96) for letter in 'abcdefghijklmnopqrstuvwxyz']
priority_scores.extend([(letter,ord(letter)-38) for letter in 'abcdefghijklmnopqrstuvwxyz'.upper()])
priority_scores = dict(priority_scores)

total_priority_score = 0
for backpack in backpacks:
    left = list(backpack[:len(backpack)//2])
    right = list(backpack[len(backpack)//2:])
    temp_list = [None] * len(left)
    left_dict = dict(list(zip(left,temp_list)))

    for letter in right:
        if letter in left_dict:
            total_priority_score += priority_scores[letter]
            break

print(f'total priority score for items sorted wrong: {total_priority_score}')


# ============== PART 2 ====================

total_priority_for_groups = 0
for i in range(0,len(backpacks),3):
    elf_group = backpacks[i:i+3]
    
    encountered_items = {}
    
    found = False
    for i,elf in enumerate(elf_group):
        for item in list(elf):
            if item not in encountered_items:
                if i==0:
                    encountered_items[item] = i
            else:   #item is in encountered items
                if i - encountered_items[item] > 1:
                    encountered_items.pop(item)
                else:
                    encountered_items[item] = i
                    if i == 2:
                        badge = item
                        found = True
                        break



        if found == True:
            break
    total_priority_for_groups += priority_scores[badge]
    
    print(f'for the group \n{elf_group[0]}\n{elf_group[1]}\n{elf_group[2]}\n common item is {badge} with score {priority_scores[badge]}\n')

print(f'total priority score for common items in groups of 3: {total_priority_for_groups}')
