def read_input(inpf):
    with open(inpf) as f:
        program = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) == 1:
                program.append((parts[0], None))
            else:
                op = parts[0]
                value = int(parts[1])
                program.append((op, value))
        return program


class CrtCpu:

    def __init__(self, program):
        self.registers = {'X': 1}
        self.cycle = 0
        self.program = program
        self.PC = 0
        self.update_handlers = []
    
    def add_handler(self, hnd):
        self.update_handlers.append(hnd)
    
    def exec_instr(self, instr):
        op, value = instr
        if op == 'addx':
            curr = self.registers['X']
            self.registers['X'] = curr + value
            #self.on_update(curr, self.cycle, self.cycle+2)
            self.on_cycle(self.cycle + 1, curr)
            self.on_cycle(self.cycle + 2, curr)
            self.cycle += 2
            self.PC += 1
        elif op == 'noop':
            #self.on_update(self.registers['X'], self.cycle, self.cycle+1)
            self.on_cycle(self.cycle + 1, self.registers['X'])
            self.cycle += 1
            self.PC += 1
        else:
            self.on_cycle(self.cycle + 1, self.registers['X'])  
            raise Exception('Unknown instruction: {}'.format(instr))
    
    def exec(self):
        while True:
            if self.PC < 0 or self.PC >= len(self.program):
                print('PC out of bound - HLT')
                return
            instr = self.program[self.PC]
            self.exec_instr(instr)
    
    # def on_update(self, curr, pcycle, ncycle):
    #     for hnd in self.update_handlers:
    #         hnd(self, curr, pcycle, ncycle)
    def on_cycle(self, cycle, value):
        for hnd in self.update_handlers:
            hnd(self, cycle, value)


def part1(program):
    cpu = CrtCpu(program)

    values = {}

    # def measure(cpu, p_value, pcycle, ncycle):
    #     for cycle in [20, 60, 100, 140, 180, 220]:
    #         if cycle > pcycle and cycle <= ncycle:
    #             # use the final value
    #             values[cycle] = p_value
    #         elif cycle == ncycle+1:
    #             # in the middle, use the previous value
    #             values[cycle] = cpu.registers['X']

    def measure(cpu, cycle, value):
        if cycle in [20, 60, 100, 140, 180, 220]:
            values[cycle] = value
    
    cpu.add_handler(measure)
    cpu.exec()
    print(values)
    return sum([k*v for k,v in values.items()])


def part2(program):
    cpu = CrtCpu(program)

    display = [['.' for _ in range(40)] for i in range(6)]

    
    def on_cycle(cpu, cycle, value):
        row = cycle//40
        pos = cycle % 40

        sp = value
        if pos >= sp and pos <= (sp+2):
            display[row][pos] = '#'

    cpu.add_handler(on_cycle)

    cpu.exec()

    print('\n'.join(''.join(r) for r in display))


print('Part 1:', part1(read_input('input')))
part2(read_input('input'))