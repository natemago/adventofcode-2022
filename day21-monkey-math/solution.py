import re

def read_input(inpf):
    with open(inpf) as f:
        expressions = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            var_name, expr = line.split(':')
            expressions.append((
                var_name.strip(),
                [tok.strip() for tok in expr.split() if tok.strip()],
            ))

        return expressions

OPERATIONS = {
    '+': lambda a,b: a+b,
    '-': lambda a,b: a-b,
    '*': lambda a,b: a*b,
    '/': lambda a,b: a//b,
}

def tokenize(expr):
    tokens = []
    for tok in expr:
        if tok in OPERATIONS:
            tokens.append(('op', OPERATIONS[tok], tok)),
        elif re.match(r'^-?\d+$', tok):
            tokens.append(('const', int(tok), tok))
        elif tok.isalpha():
            tokens.append(('var', tok, tok))
    return tokens

class Node:

    def __init__(self, _type, value, rawval):
        self.type = _type
        self.value = value
        self.raw = rawval

        self.left = None
        self.Right = None
    

def as_graph(expressions):
    graph= {}
    for var, expr in expressions:
        if var in graph:
            raise Exception('Redefined? {}'.format((var, expr)))
        graph[var] = tokenize(expr)

    return graph

def evaluate(node, graph, values, humn=None):
    #print('node=',node)
    if node == 'humn' and humn is not None:
        #print(':::: hooman pls hlp')
        return humn
    if node in values:
        return values[node]
    tokens = graph.get(node)
    if len(tokens) == 1:
        # assignment
        tp, value, raw = tokens[0]
        if tp == 'const':
            values[node] = value
            return value
        if tp == 'var':
            values[node] = evaluate(value, graph, values, humn)
            return values[node]
        raise Exception('Assign from {}'.format(tokens))
    if len(tokens) == 3:
        a, op, b = tokens
        a = evaluate(a[1], graph, values, humn)
        b = evaluate(b[1], graph, values, humn)
        value = op[1](a,b)
        values[node] = value
        return value
    
    raise Exception('Dont know what to do with: {} (node: {})'.format(tokens, node))



def part1(expressions):
    graph = as_graph(expressions)
    return evaluate('root', graph, {})

def part2(expressions):
    graph = as_graph(expressions)
    a, _, b = graph.get('root')

    print('humn=', graph.get('humn'))

    def f(n):
        vala = evaluate(a[1], graph, {}, n)
        valb = evaluate(b[1], graph, {}, n)
        return vala - valb
    
    def derivative_at(n, d):
        return (f(n+d) - f(n))/d

    # Newton's method
    x0 = -100
    epsilon = 0.5
    while True:
        x1 = x0 - (f(x0)/derivative_at(x0, 10))
        if abs(x1 - x0) <= epsilon:
            # we got as solution
            break
        x0 = x1
    x0 = int(x0)
    # Try out a couple of values
    for i in range(x0-5, x0+5):
        if f(i) == 0:
            # this is the exact solution
            return i
        


print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))