def read_input(inpf):
    with open(inpf) as f:
        return [[int(line) for line in group.split('\n') if line.strip()] for group in f.read().split('\n\n')]


def part1(elves):
    return max([sum(elf) for elf in elves]) 


def part2(elves):
    return sum((sorted([sum(elf) for elf in elves], reverse=True))[0:3])


print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))