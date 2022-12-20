def read_input(inpf):
    with open(inpf) as f:
        return [int(line) for line in f if line]

class Node:

    def __init__(self, value):
        self.value = value
        self.prev = self
        self.next = self

    def move_n_fwd(self, n):
        nn = self.next
        self.remove()
        for _ in range(n-1):
            nn = nn.next
        
        self.put_after(nn)

        return self
    
    def move_n_bwd(self, n):
        p = self.prev
        self.remove()
        for _ in range(n-1):
            p = p.prev
        
        self.put_before(p)
        
        return self
    
    def skip_n(self, n):
        node = self
        for _ in range(n):
            node = node.next
        
        return node
    
    def remove(self):
        n = self.next
        p = self.prev

        # stich p <-> n
        p.next = n
        n.prev = p

        self.prev = self
        self.next = self

        return self
    
    def put_after(self, t):
        n = t.next

        # configure t <-> self <-> n
        t.next = self
        self.prev = t

        self.next = n
        n.prev = self

        return self
    
    def put_before(self, t):
        p = t.prev

        # configure p <-> self <-> t
        p.next = self
        self.prev = p
        
        self.next = t
        t.prev = self

        return self

    def as_list(self):
        ll = []
        n = self
        ll.append(n.value)
        n = n.next
        while n != self:
            ll.append(n.value)
            n = n.next

        return ll
    
    def find(self, value):
        if self.value == value:
            return self
        n = self.next
        while n != self:
            if n.value == value:
                return n
            n = n.next
        raise Exception('Not found %s' % value)


def to_list(seq):
    head = Node((0, seq[0]))
    tail = head

    for i,n in enumerate(seq[1:]):
        n = Node((i+1, n))
        n.prev = tail
        tail.next = n
        tail = n
    
    head.prev = tail
    tail.next = head

    return head


def part1(seq):
    node = to_list(seq)
    zero = None
    
    for i,n in enumerate(seq):
        node = node.find((i,n))
        if n == 0:
            zero = (i, 0)
        elif n > 0:
            node.move_n_fwd(n % (len(seq) - 1))
        else:
            node.move_n_bwd(abs(n) % (len(seq) - 1))
    
    zero = node.find(zero)

    r = [
        zero.skip_n(n*1000).value[1] for n in range(1,4)
    ]
    print(r)
    return sum(r)


def part2(seq):
    seq = [n*811589153 for n in seq]

    node = to_list(seq)
    zero = None
    
    for k in range(10):
        print('Decryption round:', k)
        for i,n in enumerate(seq):
            node = node.find((i,n))
            if n == 0:
                zero = (i, 0)
            elif n > 0:
                node.move_n_fwd(n % (len(seq) - 1))
            else:
                node.move_n_bwd(abs(n) % (len(seq) - 1))
    
    zero = node.find(zero)

    r = [
        zero.skip_n(n*1000).value[1] for n in range(1,4)
    ]
    print(r)
    return sum(r)

print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))
        