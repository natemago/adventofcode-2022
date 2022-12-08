def read_input(inpf):
    with open(inpf) as f:
        return [line.strip().split() for line in f]
Rock = 'A'
Paper = 'B'
Scissors = 'C'
shapes = {
    Rock: (1, Scissors, Paper),
    Paper: (2, Rock, Scissors),
    Scissors: (3, Paper, Rock),
}

def play(game, strategy):
    total = 0
    for shp, my_shp in game:
        my_shp = strategy[my_shp]
        if shp != my_shp:
            points, beats, _ = shapes[my_shp]
            if beats == shp:
                total += points + 6
            else:
                total += points
        else:  # draw
            total += shapes[my_shp][0] + 3
    return total



def part1(game):
    strategy = {'X': 'A', 'Y': 'B', 'Z': 'C'}
    return play(game, strategy)

def part2(game):
    total = 0
    for shp, my_shp in game:
        _, beats, beaten_by = shapes[shp]
        if my_shp == 'X':
            # need to loose
            my_shp = beats
        elif my_shp == 'Y':
            # draw
            my_shp = shp
        else:
            # need to win
            my_shp = beaten_by

        if shp != my_shp:
            points, beats, _ = shapes[my_shp]
            if beats == shp:
                total += points + 6
            else:
                total += points
        else:  # draw
            total += shapes[my_shp][0] + 3
    return total


print('Part 1: ', part1(read_input('input')))
print('Part 2: ', part2(read_input('input')))

