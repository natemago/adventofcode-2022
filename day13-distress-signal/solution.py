from functools import cmp_to_key

def read_input(inpf):
    with open(inpf) as f:
        pairs = []
        pair = []
        for line in f:
            line = line.strip()
            if not line:
                pairs.append(pair)
                pair = []
                continue
            packet = eval(line)
            pair.append(packet)
        
        if pair:
            pairs.append(pair)
        
        return pairs


def compare(p1, p2):
    print(' > compare:', p1, p2)
    if not p1 and p2:
        return True
    for i in range(min([len(p1), len(p2)])):
        el1 = p1[i]
        el2 = p2[i]

        if isinstance(el1, int) and isinstance(el2, int):
            print(' .. ', el1, '<>', el2)
            if el1 > el2:
                print('  > e1 > e2 - wrong')
                return False
            elif el1 < el2:
                print('  > e1 > e2 - correct')
                return True
        elif isinstance(el1, int) and isinstance(el2, list):
            if not compare([el1], el2):
                return False
        elif isinstance(el1, list) and isinstance(el2, int):
            if not compare(el1, [el2]):
                return False
        elif isinstance(el1, list) and isinstance(el2, list):
            if not compare(el1, el2):
                return False

    return True

def compare(a1, a2):
    for i in range(min((len(a1), len(a2)))):
        e1 = a1[i]
        e2 = a2[i]

        if isinstance(e1, list) and isinstance(e2, list):
            r = compare(e1, e2)
            if r != 0:
                return r
            continue
        elif isinstance(e1, list) and isinstance(e2, int):
            r = compare(e1, [e2])
            if r != 0:
                return r
            continue
        elif isinstance(e1, int) and isinstance(e2, list):
            r = compare([e1], e2)
            if r != 0:
                return r
            continue
        else:
            if e1 == e2:
                continue
            return 1 if e1 < e2 else -1
    
    if len(a1) > len(a2):
        return -1
    elif len(a1) < len(a2):
        return 1
    return 0


def part1(pairs):
    total = 0
    for i, pair in enumerate(pairs):
        if compare(*pair) == 1:
            total += i + 1
    return total

def part2(pairs):
    packets = []
    for pair in pairs:
        packets.append(pair[0])
        packets.append(pair[1])
    
    # Include the divider packets
    packets.append([[6]])
    packets.append([[2]])

    packets = list(sorted(packets, key=cmp_to_key(compare), reverse=True))

    res = 1
    for i, p in enumerate(packets):
        if p == [[6]] or p == [[2]]:
            res *= (i+1)
    return res


print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))

