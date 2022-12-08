
def get_scenic_score():
    scores = []
    grid = []
    with open(f"../inputs/day_08.txt", 'r') as input_file:
        for line in input_file.readlines():
            grid.append([int(x) for x in list(line.strip())])
    for row_index, row in enumerate(grid):
        for col_index, tree in enumerate(row):
            if row_index == 0 or col_index == 0 or col_index == len(grid) - 1 or row_index == len(grid) - 1:
                continue
            column = [grid[r][col_index] for r in range(len(grid))]
            directions = [
                reversed(column[0:row_index]),  # North/Up
                column[row_index+1:],  # South/Down
                reversed(row[0:col_index]),  # West/Left
                row[col_index+1:],  # East/Right
            ]
            score = 1
            for direction in directions:
                dist = 0
                for step in direction:
                    dist += 1
                    if step >= tree:
                        break
                score *= dist
            scores.append(score)
    return max(scores)

def do():
    count = 0
    grid = []
    with open(f"../inputs/day_08.txt", 'r') as input_file:
        for line in input_file.readlines():
            grid.append([int(x) for x in list(line.strip())])
    for row_index, row in enumerate(grid):
        for col_index, tree in enumerate(row):
            column = [grid[r][col_index] for r in range(len(grid))]
            if any([
                row_index == 0,
                col_index == 0,
                row_index == len(grid) - 1,
                col_index == len(row) - 1,
                max(row[0:col_index] or [1000]) < tree,
                max(row[col_index + 1:] or [1000]) < tree,
                max(column[0:row_index] or [1000]) < tree,
                max(column[row_index + 1:] or [1000]) < tree,
            ]):
                if not any([
                row_index == 0,
                col_index == 0,
                row_index == len(grid) - 1,
                col_index == len(row) - 1,]):
                    print(f"({row_index}, {col_index}), tree={tree}")
                count += 1
    return count


def part_1():
    x = do()
    print(x)


def part_2():
    print(get_scenic_score())
        
        
if __name__ == '__main__':
    # part_1()
    part_2()
