def read_input(inpf):
    result = []
    elf_entries = []
    with open(inpf) as f:
        for line in f:
            line = line.strip()
            if not line:
                if elf_entries:
                    result.append(elf_entries)
                    elf_entries = []
            else:
                elf_entries.append(int(line))
    return result


def part1(elves):
    return max([sum(elf) for elf in elves]) 


def part2(elves):
    elves = list(sorted([sum(elf) for elf in elves], reverse=True))
    return sum(elves[0:3])


print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))