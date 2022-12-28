from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd

"""its a panda!"""


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """
    # check check
    choize = ["up", "right"]
    i, j = coord[0], coord[1]
    direction = choice(choize)
    if direction == "up":
        if i == 1:
            grid[i][j + 1] = " "
        else:
            grid[i - 1][j] = " "
    else:
        if j == len(grid) - 2:
            grid[i - 1][j] = " "
        else:
            grid[i][j + 1] = " "
    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

    for cell in empty_cells:
        remove_wall(grid, cell)

    if grid[1][len(grid) - 1] != "■":
        grid[1][len(grid) - 1] = "■"
    # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """
    possibles = []
    exits = []
    for i in range(0, len(grid)):
        possibles.append([0, i])
        possibles.append([i, 0])
        possibles.append([len(grid) - 1, i])
        possibles.append([i, len(grid) - 1])
    for j in range(len(possibles)):
        x, y = possibles[j][0], possibles[j][1]
        if grid[x][y] == "X" and (x, y) not in exits:
            exits.append((x, y))
    # print(exits)
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """
    cells = []
    for i in range(0, len(grid)):
        for j in range(0, len(grid)):
            if grid[i][j] == k:
                cells.append([i, j])
    for q in range(len(cells)):
        x, y = cells[q][0], cells[q][1]
        if y != 0 and grid[x][y - 1] == " ":
            grid[x][y - 1] = k + 1
        elif y != 0 and grid[x][y - 1] == 0:
            grid[x][y - 1] = k + 1
        if x != 0 and grid[x - 1][y] == " ":
            grid[x - 1][y] = k + 1
        elif x != 0 and grid[x - 1][y] == 0:
            grid[x - 1][y] = k + 1
        if y != len(grid) - 1 and grid[x][y + 1] == " ":
            grid[x][y + 1] = k + 1
        elif y != len(grid) - 1 and grid[x][y + 1] == 0:
            grid[x][y + 1] = k + 1
        if x != len(grid) - 1 and grid[x + 1][y] == " ":
            grid[x + 1][y] = k + 1
        elif x != len(grid) - 1 and grid[x + 1][y] == 0:
            grid[x + 1][y] = k + 1
    return grid


def shortest_path(grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]):
    # -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    a, b = exit_coord[0], exit_coord[1]
    ex = grid[a][b]
    k = int(grid[a][b]) - 1
    dawae = []
    current = a, b
    dawae.append(current)
    while k != 0:
        if a + 1 < len(grid):
            if grid[a + 1][b] == k:
                current = a + 1, b
                a += 1
        if a - 1 >= 0:
            if grid[a - 1][b] == k:
                current = a - 1, b
                a -= 1
        if b + 1 < len(grid):
            if grid[a][b + 1] == k:
                current = a, b + 1
                b += 1
        if b - 1 >= 0:
            if grid[a][b - 1] == k:
                current = a, b - 1
                b -= 1
        dawae.append(current)
        k -= 1
    if len(dawae) != ex:
        x = dawae[-1][0]
        y = dawae[-1][1]
        grid[x][y] = " "
        q, w = dawae[-2][0], dawae[-2][1]
        shortest_path(grid, (q, w))
    return dawae


# List[List[Union[str, int]]] : Tuple[int, int]
def encircled_exit(grid, coord) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """

    x, y = coord[0], coord[1]
    if (
        (x == 0 and y == 0)
        or (x == 0 and y == len(grid) - 1)
        or (x == len(grid) - 1 and y == 0)
        or (x == len(grid) - 1 and y == len(grid))
    ):
        return True
    if y == 0 and grid[x][y + 1] == "■":
        return True
    if y == len(grid) - 1 and grid[x][y - 1] == "■":
        return True
    if x == 0 and grid[x + 1][y] == "■":
        return True
    if x == len(grid) - 1 and grid[x - 1][y] == "■":
        return True
    return False


# : List[List[Union[str, int]]]
def solve_maze(
    grid,
):
    # -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """

    exits = get_exits(grid)
    if len(exits) != 2:
        return grid, None
    # print(exits)
    x, y = exits[0][0], exits[0][1]
    a, b = exits[1][0], exits[1][1]
    if encircled_exit(grid, (x, y)):
        return grid, None
    if encircled_exit(grid, (a, b)):
        return grid, None
    k = 1
    grid[x][y], grid[a][b] = 1, 0
    while grid[a][b] == 0:
        make_step(grid, k)
        k += 1
    dawae = shortest_path(grid, (a, b))
    return grid, dawae


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
                if str(grid[i][j]).isdigit():
                    grid[i][j] = " "
    return grid


if __name__ == "__main__":
    # print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
