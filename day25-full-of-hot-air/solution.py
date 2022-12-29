def read_input(inpf):
    with open(inpf) as f:
        return [line.strip() for line in f if line.strip()]

addition = {
    ('0', '0'): ('0', ''),
    ('0', '1'): ('1', ''),
    ('0', '2'): ('2', ''),
    ('0', '-'): ('-', ''),
    ('0', '='): ('=', ''),

    ('1', '0'): ('1', ''),
    ('1', '1'): ('2', ''),
    ('1', '2'): ('=', '1'),
    ('1', '-'): ('0', ''),
    ('1', '='): ('-', ''),
    
    ('2', '0'): ('2', ''),
    ('2', '1'): ('=', '1'),
    ('2', '2'): ('-', '1'),
    ('2', '-'): ('1', ''),
    ('2', '='): ('0', ''),

    ('-', '0'): ('-', ''),
    ('-', '1'): ('0', ''),
    ('-', '2'): ('1', ''),
    ('-', '-'): ('=', ''),
    ('-', '='): ('2', '-'),

    ('=', '0'): ('=', ''),
    ('=', '1'): ('-', ''),
    ('=', '2'): ('0', ''),
    ('=', '-'): ('2', '-'),
    ('=', '='): ('1', '-'),
}

def add_with_carry(a, b, c):
    if not c:
        return addition[(a,b)]
    ab, c1 = addition[(a, b)]
    abc, c2 = addition[(ab, c)]
    if not c1 and not c2:
        return (abc, '')
    if c1 and c2:
        c, _ = addition[(c1, c2)]
    else:
        c = c1 if c1 else c2
    return (abc, c)

def full_add(a, b):
    c = ''
    res = ''
    for i in range(max([len(a), len(b)])):
        aa = a[len(a) - i - 1] if i < len(a) else '0'
        bb = b[len(b) - i - 1] if i < len(b) else '0'
        s, c = add_with_carry(aa, bb, c)
        res = s + res
    if c:
        res = c + res
    return res

def part1(snafu_numbers):
    result = snafu_numbers[0]
    for b in snafu_numbers[1:]:
        result = full_add(result, b)
    return result



print('Part 1:', part1(read_input('input')))


