import re


def read_input(inpf):
    stacks = {}
    procedure = []

    with open(inpf) as f:
        for line in f:
            if not line.strip():
                continue
            if not line:
                continue
            if line.strip().startswith('['):
                sp = 1
                cs = line[0:3] # first stack
                if cs.strip():
                    stacks[sp] = stacks.get(sp, [])
                    stacks[sp].append(cs.strip()[1:-1])
                for i in range(0, len(line)-3//4):
                    cs = line[i*4+3: i*4+7]
                    sp += 1
                    if cs.strip():
                        stacks[sp] = stacks.get(sp, [])
                        stacks[sp].append(cs.strip()[1:-1])
            elif line.strip().startswith('move'):
                m = re.match(r'move\s+(?P<crate>\d+)\s+from\s+(?P<from_stack>\d+)\s+to\s+(?P<to_stack>\d+)', line.strip())
                if not m:
                    raise Exception('did not match: %s' % line)
                crate = int(m.group('crate'))
                from_stack = int(m.group('from_stack'))
                to_stack = int(m.group('to_stack'))
                procedure.append((crate, from_stack, to_stack))
            else:
                pass

    return {k: list(reversed(s)) for k,s in stacks.items()}, procedure

def part1(stacks, procedure):
    for crates, fr, to in procedure:
        from_stack = stacks[fr]
        to_stack = stacks[to]
        for i in range(crates):
            to_stack.append(from_stack.pop())
    
    return ''.join([s[-1] for _,s in sorted(list(stacks.items()))])


def part2(stacks, procedure):
    for crates, fr, to in procedure:
        from_stack = stacks[fr]
        to_stack = stacks[to]
        cs = from_stack[-crates:]
        stacks[fr] = from_stack[0:-crates]
        stacks[to] += cs

    return ''.join([s[-1] for _,s in sorted(list(stacks.items()))])

print('Part 1:', part1(*read_input('input')))
print('Part 2:', part2(*read_input('input')))
