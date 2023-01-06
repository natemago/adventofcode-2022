import re
from collections import deque
from multiprocessing import Pool

def read_input(inpf):
    with open(inpf) as f:
        return [parse_blueprint(line.strip()) for line in f if line.strip()]


def parse_blueprint(line):
    blueprint, specs = line.split(':')
    blueprint = int(re.match(r'Blueprint (\d+)', blueprint).group(1))
    robots = {}
    for spec in specs.split('.'):
        spec = spec.strip()
        if not spec:
            continue
        m = re.match(r'Each (?P<robot>\w+) robot costs (?P<cost1>\d+) (?P<dep1>\w+) and (?P<cost2>\d+) (?P<dep2>\w+)', spec)
        if m:
            robots[m.group('robot')] = {
                m.group('dep1'): int(m.group('cost1')),
                m.group('dep2'): int(m.group('cost2')),
            }
        else:
            m = re.match(r'Each (?P<robot>\w+) robot costs (?P<cost1>\d+) (?P<dep1>\w+)', spec)
            if not m:
                raise Exception('Failed to parse: %s' % spec)
            robots[m.group('robot')] = {
                m.group('dep1'): int(m.group('cost1')),
            }
    
    return blueprint, robots


def can_build(blueprint, robot, state):
    for dep, cost in blueprint[robot].items():
        if state.get(dep, 0) < cost:
            return False
    return True

def what_robots_can_be_build(blueprint, state):
    robots = []
    for robot in blueprint.keys():
        if can_build(blueprint, robot, state):
            robots.append(robot)
    return robots

def get_max_robots(blueprint):
    robots = {}

    for _, deps in blueprint.items():
        for robot, cost in deps.items():
            robots[robot] = max(cost, robots.get(robot, 0))

    return robots

def clone(dct):
    cln = {}
    cln.update(dct)
    return cln

def reached_max(robots, max_robots):
    for robot, count in max_robots.items():
        if robots.get(robot,  0) < count:
            return False
    return True

def has_enough_for_geode(blueprint, robots):
    deps = blueprint['geode']
    for dep, cost in deps.items():
        if robots.get(dep, 0) < cost:
            return False
    return True

def to_state(state):
    return (
        state.get('ore', 0),
        state.get('clay', 0),
        state.get('obsidian', 0),
        state.get('geode', 0),
    )

def check_blueprint(blueprint, minutes=24):
    print(' we have', minutes, 'minutes')
    state = {}
    robots = {'ore': 1}
    geode_max = 0
    max_robots = get_max_robots(blueprint)

    seen = set()

    # state, robots, time
    q = deque()
    q.append((state, robots, 0))


    it = 0

    while q:
        state, robots, time = q.pop()
        it += 1

        node = (
            to_state(state),
            to_state(robots),
            time,
        )

        if node in seen:
            continue
        seen.add(node)

        if time >= minutes:
            if state.get('geode', 0) > geode_max:
                geode_max = state['geode']
            continue
        
        if geode_max:
            # calculate potentially max number of geodes that can be produced here
            curr_geodes = state.get('geode', 0)
            curr_geode_robots = robots.get('geode', 0)
            time_left = (minutes - time)
            total_potential = time_left * curr_geode_robots + curr_geodes + (time_left*(time_left+1))//2
            if total_potential <= geode_max:
                continue

        

        # let's update the state
        state_clone = clone(state)
        robots_clone = clone(robots)
        
        
        can_be_build = what_robots_can_be_build(blueprint, state_clone)

        for robot in can_be_build:
            if robot != 'geode' and robots.get(robot) and robots.get(robot) >= max_robots.get(robot):
                continue
            upd_state = clone(state)
            upd_robots = clone(robots)
            upd_robots[robot] = upd_robots.get(robot, 0) + 1

            for dep, cost in blueprint[robot].items():
                upd_state[dep] -= cost
            
            for robot, count in robots_clone.items():
                upd_state[robot] = upd_state.get(robot, 0) + count

            q.append((upd_state, upd_robots, time+1))

        if has_enough_for_geode(blueprint, robots):
            # don't branch into not building geode
            continue
        for robot, count in robots_clone.items():
            state_clone[robot] = state_clone.get(robot, 0) + count
        q.append((state_clone, robots_clone, time+1))


    print('    Total iterations:', it)

    return geode_max

def part1(blueprints):
    total = 0
    for blueprint_id, blueprint in blueprints:
        print('Checking blueprint:', blueprint_id, blueprint)
        res = check_blueprint(blueprint)
        qual_level = res * blueprint_id
        print('Blueprint {} has max geodes {} and quality level {}'.format(blueprint_id, res, qual_level))
        total += qual_level
    return total

def part2(blueprints):
    total = 1
    for blueprint_id, blueprint in blueprints[0:3]:
        print('Checking blueprint:', blueprint_id, blueprint)
        res = check_blueprint(blueprint, 32)
        print('Blueprint {} has max geodes {}.'.format(blueprint_id, res))
        total *= res
    return total

print('Part 1:', part1(read_input('input')))
print('Part 2:', part2(read_input('input')))