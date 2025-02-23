from enum import Enum


class OperationType(Enum):
    ADDITION = 0
    MULTIPLICATION = 1
    SQUARE = 2


class Monkey:
    
    
    def __init__(self, items: list[int], operation_type: OperationType, test_divisibility: int, success_monkey_index: int, failure_monkey_index: int, operation_value: int = None) -> None:
        self.items = items
        self.operation_type = operation_type
        self.test_divisibility = test_divisibility
        self.operation_value = operation_value
        self.success_monkey_index = success_monkey_index
        self.failure_monkey_index = failure_monkey_index
        self.total_inspections = 0
        self.success_monkey: Monkey
        self.failure_monkey: Monkey
    
    def perform_operation(self, item_value: int) -> int:
        if self.operation_type == OperationType.ADDITION:
            new_item_value = item_value + self.operation_value
        if self.operation_type == OperationType.MULTIPLICATION:
            new_item_value = item_value * self.operation_value
        if self.operation_type == OperationType.SQUARE:
            new_item_value = item_value * item_value

        return new_item_value
    
    
    def inspect_and_pass(self, item_value):
        self.total_inspections += 1
        item_value = self.perform_operation(item_value)
        item_value = reduce_factors(item_value)
        self.throw_item_to_monkey(item_value, self.decide_pass_target(item_value))
    
    def inspect_and_pass_all_items(self):
        for item in self.items:
            self.inspect_and_pass(item)
        self.items = []

    def test_item_divisibility(self, item_value) -> bool:
        return item_value % self.test_divisibility == 0
    
    def decide_pass_target(self, item_value):
        if self.test_item_divisibility(item_value):
            target_monkey = self.success_monkey
        else:
            target_monkey = self.failure_monkey

        return target_monkey
    
    def throw_item_to_monkey(self, item_value, target_monkey) -> None:
        target_monkey.recieve_item(item_value)

    def recieve_item(self, item_value) -> None:
        self.items.append(item_value)

    def build_monkey(monkey_dict):
        starting_items = [int(item) for item in monkey_dict['Starting items'].split(',')]
        
        operation_string, operation_value  = monkey_dict['Operation'].split(' ')[-2:]
        if operation_value == 'old':
            operation_type = OperationType.SQUARE
            operation_value = 0
        elif operation_string == '+':
            operation_type = OperationType.ADDITION
            operation_value = int(operation_value)
        elif operation_string == '*':
            operation_type = OperationType.MULTIPLICATION
            operation_value = int(operation_value)
        
        test_divisibility = int(monkey_dict['Test'].split()[-1])
        true_monkey = int(monkey_dict['If true'].split()[-1])
        false_monkey = int(monkey_dict['If false'].split()[-1])

        return Monkey(starting_items, operation_type, test_divisibility, true_monkey, false_monkey, operation_value)
        
    def convert_operation_to_str(self):
        if self.operation_type == OperationType.SQUARE:
            return f"* old"
        if self.operation_type == OperationType.ADDITION:
            return f"+ {self.operation_value}"
        if self.operation_type == OperationType.MULTIPLICATION:
            return f"* {self.operation_value}"    
    
    def __repr__(self) -> str:
        return f"\nItems: {self.items}\nOperation: new = old {self.convert_operation_to_str()}\nTest: divisible by {self.test_divisibility}\n True: {self.success_monkey_index}\n False: {self.failure_monkey_index}\nTotal inspections: {self.total_inspections}"
        

PRIME_FACTOR = 2*3*5*7*11*13*17*19*23
def reduce_factors(num: int) -> int:
    return num % PRIME_FACTOR

monkey_list: list[Monkey] = []

with open('input_11.txt', 'r') as f:
    monkey_dict = {}
    for line in f:
        line = line.strip()
        
        if not line:
            new_monkey = Monkey.build_monkey(monkey_dict)
            monkey_list.append(new_monkey)
            monkey_dict.clear()
            continue
        
        key, value = line.split(':')
        if not value:
            continue
        monkey_dict[key] = value


for idx, monkey in enumerate(monkey_list):
    monkey.success_monkey = monkey_list[monkey.success_monkey_index]
    monkey.failure_monkey = monkey_list[monkey.failure_monkey_index]


for monkey_round in range(10000):
    print(f'Round {monkey_round}')
    for idx, monkey in enumerate(monkey_list):
        monkey.inspect_and_pass_all_items()


passes = []
for monkey in monkey_list:
    passes.append(monkey.total_inspections)
    
print(passes)
sorted_passes = sorted(passes)
print(sorted_passes[-1] * sorted_passes[-2])
