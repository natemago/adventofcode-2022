def read_input(inpf):
    with open(inpf) as f:
        mid = None
        items = []
        operation = None
        cond = None
        out_true = None
        out_false = None
        divisor = None

        monkeys = []

        for line in f:
            line = line.strip()
            if not line:
                monkeys.append(Monkey(
                    mid,
                    items,
                    operation,
                    cond,
                    {'true': out_true, 'false': out_false},
                    divisor,
                ))
                mid = None
                continue
            if line.startswith('Monkey'):
                mid = int(line.split()[1].strip()[:-1])
            elif line.startswith('Starting items:'):
                items = [int(i) for i in line[len('Starting items:'):].strip().split(',')]
            elif line.startswith('Operation:'):
                operation = parse_operation(line)
            elif line.startswith('Test:'):
                cond, divisor = parse_condition(line)
            elif line.startswith('If true:'):
                out_true = int(line[len('If true: throw to monkey'):].strip())
            elif line.startswith('If false:'):
                out_false = int(line[len('If false: throw to monkey'):].strip())
            else:
                raise Exception('Failed to parse line: %s' % line)

        if mid:
            monkeys.append(Monkey(
                mid,
                items,
                operation,
                cond,
                {'true': out_true, 'false': out_false},
                divisor,
            ))
        
        return monkeys

def parse_operation(line):
    var1,operand,var2 = line[len('Operation:'):].split('=')[1].strip().split()
    operation = OPERATIONS['{}-{}'.format(
        'const' if var1.isnumeric() else var1,
        'const' if var2.isnumeric() else var2,
    )](OPS[operand], int(var1) if var1.isnumeric() else int(var2) if var2.isnumeric() else None)
    return operation


def parse_condition(line):
    line = line[len('Test:'):].strip().split()
    divisible_by = int(line[2])
    cond = lambda value: value % divisible_by == 0
    return cond, divisible_by

OPS = {
    '+': lambda a,b: a+b,
    '*': lambda a,b: a*b
}

OPERATIONS = {
    'old-old': lambda op,_: lambda var: op(var, var),
    'old-const': lambda op,const: lambda var: op(var, const),
    'const-old': lambda op,const: lambda var: op(const, var),
}


class Monkey:

    def __init__(self, id, items, operation, condition, outcomes, divisor):
        self.items = items
        self.operation = operation
        self.condition = condition
        self.outcomes = outcomes
        self.id = id
        self.inspected = 0
        self.manage_stress_levels = 3
        self.divisor = divisor
    
    def catch_item(self, value):
        self.items.append(value)

    def examine_and_throw_all(self, monkeys):
        if self.manage_stress_levels == 1:
            for value in self.items:
                value = self.operation(value % self.divisor) % self.divisor
                if self.condition(value):
                    monkeys[self.outcomes['true']].catch_item(value)
                else:
                    monkeys[self.outcomes['false']].catch_item(value)
        else:
            for value in self.items:
                value = self.operation(value) // 3
                if self.condition(value):
                    monkeys[self.outcomes['true']].catch_item(value)
                else:
                    monkeys[self.outcomes['false']].catch_item(value)

        # thrown all items
        self.inspected += len(self.items)
        self.items = []

    def __str__(self):
        return '\n'.join([
            'Monkey {}:'.format(self.id),
            '   Starting items: {}'.format(self.items),
            '   Operation: {}'.format(self.operation),
            '   Test: {}'.format(self.condition),
            '       It true: throw to monkey {}'.format(self.outcomes['true']),
            '       It false: throw to monkey {}'.format(self.outcomes['false']),
        ])
    
    def __repr__(self):
        return self.__str__()


def part1(monkeys):

    for _ in range(20): # 20 rounds
        for monkey in monkeys:
            monkey.examine_and_throw_all(monkeys)
    
    monkeys = list(sorted(monkeys, key=lambda m: m.inspected, reverse=True))
    return monkeys[0].inspected * monkeys[1].inspected

def part2(monkeys):
    # monkeys[0].operation = lambda value: value * 19
    # monkeys[0].condition = lambda value: value % 23 == 0
    # monkeys[0].divisor = 23

    # monkeys[1].operation = lambda value: value + 6
    # monkeys[1].condition = lambda value: value % 19 == 0
    # monkeys[1].divisor = 19

    # monkeys[2].operation = lambda value: value * value
    # monkeys[2].condition = lambda value: value % 13 == 0
    # monkeys[2].divisor = 13

    # monkeys[3].operation = lambda value: value + 3
    # monkeys[3].condition = lambda value: value % 17 == 0
    # monkeys[3].divisor = 17

    divisor = 1

    for m in monkeys:
        m.manage_stress_levels = 1
        divisor *= m.divisor
    for m in monkeys:
        m.divisor = divisor

    for i in range(10_000): # 10000 rounds
        for monkey in monkeys:
            monkey.examine_and_throw_all(monkeys)
        if (i+1) in [1, 19, 20, 21, 1000, 2000, 10_000]:
            print('== After round {} =='.format(i+1))
            for m in monkeys:
                print('Monkey {} has examined {} times.'.format(m.id, m.inspected))
    
    monkeys = list(sorted(monkeys, key=lambda m: m.inspected, reverse=True))
    return monkeys[0].inspected * monkeys[1].inspected

print('Part 1: ', part1(read_input('input')))
print('Part 2: ', part2(read_input('input')))