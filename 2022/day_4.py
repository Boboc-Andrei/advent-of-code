
with open('input_4.txt','r') as f:
    pairs = [[[int(sector) for sector in elf.split('-')] for elf in line.rstrip().split(',')] for line in f]

print(pairs[-5:])

total_overlaps = 0
overlaps = 0
for idx, pair in enumerate(pairs):
    elf1, elf2 = pair
    lower1, upper1 = elf1
    lower2, upper2 = elf2

    if (lower1 >= lower2 and upper1<=upper2) or (lower2 >= lower1 and upper2 <= upper1):
        total_overlaps+=1
    if not (upper1 < lower2 or upper2 < lower1):
        overlaps+=1

        #print(f'OVERLAP {lower1}-{upper1} : {lower2}-{upper2} at index {idx}')
    #else:
        #print(f'NO OVERLAP {lower1}-{upper1} : {lower2}-{upper2} at index {idx}')



print(f'there are {total_overlaps} complete overlaps')
print(f'there are {overlaps} at least partial overlaps')