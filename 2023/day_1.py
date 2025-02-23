
with open('input_1.txt', 'r') as f:
    codes = []
    for line in f:
        codes.append(line.rstrip())


digits = '0123456789'
str2num = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9
}

class number_tree:
    '''
        Tree for indexing number spelling letter by letter
    '''
    def __init__(self):
        self.children = {}
        self.value = None

    def add_number(self,number,value):
        if len(number) == 0:
            self.value = value
            return
        if number[0] in self.children:
            self.children[number[0]].add_number(number[1:],value)
        else:
            new_child = number_tree()
            new_child.add_number(number[1:],value)
            self.children[number[0]] = new_child

    def print_tree(self, depth = 0):
        if self.value is not None:
            print(' '*depth + str(self.value))
        else:
            for child in self.children:
                print(' '*depth + child)
                self.children[child].print_tree(depth+1)
    
    def find_number(self,value):
        if not self.children:
            return self.value

        if not value:
            return False

        if value[0] in self.children:
            return self.children[value[0]].find_number(value[1:])
        return False


    

root = number_tree()

for string in str2num:
    root.add_number(string,str2num[string])




#======PART 1=====

code_sum = 0
for code in codes:
    first = None
    last = None
    for c in code:
        if c in digits:
            if first is None:
                first = int(c)*10
            last = int(c)
    code_sum += first+last

print(code_sum)


#======PART 2=====
code_sum = 0

for code in codes:
    first = None
    for i,c in enumerate(code):
        if c in digits:
            last = int(c)
            if first is None:
                first = last * 10
        else:
            number_found = root.find_number(code[i:])
            if number_found:
                last = number_found
                if first is None:
                    first = last * 10

    code_sum += first+last



print(code_sum)