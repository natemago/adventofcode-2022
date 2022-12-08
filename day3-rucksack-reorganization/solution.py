def read_input(inpf):
    with open(inpf) as f:
        return [l.strip() for l in f.readlines()]


def prio(itm):
    if itm.islower():
        return ord(itm) - ord('a') + 1
    return ord(itm) - ord('A') + 27

def part1(rucksacks):
    total = 0
    for items in rucksacks:
        comp1 = items[0:len(items)//2]
        comp2 = items[len(items)//2:]
        c1 = {c for c in comp1}
        c2 = {c for c in comp2}
        total += prio(tuple(c1.intersection(c2))[0])
    return total

def part2(rucksacks):
    total = 0
    group = set()
    for i, items in enumerate(rucksacks):
        if (i+1) %3 == 1:
            group = {c for c in items}
        else:
            group = group.intersection({c for c in items})
        if (i+1) % 3 == 0:
            total += prio(tuple(group)[0])
    return total


print('Part 1: ', part1(read_input('input')))
print('Part 2: ', part2(read_input('input')))