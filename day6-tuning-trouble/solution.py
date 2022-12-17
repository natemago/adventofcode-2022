def read_input(inpf):
    with open(inpf) as f:
        return f.read().strip()

def solve(inp, n=4):
    for i in range(0, len(inp) - n):
        buff = inp[i:i+n]
        if len({s for s in buff}) == n:
            return i + n
    raise Exception('none found?')


print('Part 1:', solve(read_input('input')))
print('Part 2:', solve(read_input('input'), 14))