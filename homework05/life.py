import copy
import pathlib
import random
import typing as tp
from typing import List

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = [[random.randint(0, 1) if randomize else 0 for j in range(self.cols)] for i in range(self.rows)]
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        y, x = cell
        neighbours = []
        if 0 < x < len(self.curr_generation[0]) - 1 and 0 < y < len(self.curr_generation) - 1:
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    neighbours.append(self.curr_generation[y + i][x + j])
            del neighbours[4]
        if x == 0 and y == 0:  # левый верхний угол
            neighbours = [
                self.curr_generation[y][x + 1],
                self.curr_generation[y + 1][x],
                self.curr_generation[y + 1][x + 1],
            ]
        if x == len(self.curr_generation[0]) - 1 and y == 0:  # правый верхний угол
            neighbours = [
                self.curr_generation[y][x - 1],
                self.curr_generation[y + 1][x],
                self.curr_generation[y + 1][x - 1],
            ]
        if x == 0 and y == len(self.curr_generation) - 1:  # левый нижний угол
            neighbours = [
                self.curr_generation[y][x + 1],
                self.curr_generation[y - 1][x],
                self.curr_generation[y - 1][x + 1],
            ]
        if x == len(self.curr_generation[0]) - 1 and y == len(self.curr_generation) - 1:  # правый верхний угол
            neighbours = [
                self.curr_generation[y][x - 1],
                self.curr_generation[y - 1][x],
                self.curr_generation[y - 1][x - 1],
            ]
        if 0 < x < len(self.curr_generation[0]) - 1 and y == 0:  # верх
            neighbours = [
                self.curr_generation[y][x + 1],
                self.curr_generation[y + 1][x],
                self.curr_generation[y + 1][x + 1],
                self.curr_generation[y][x - 1],
                self.curr_generation[y + 1][x - 1],
            ]
        if 0 < x < len(self.curr_generation[0]) - 1 and y == len(self.curr_generation) - 1:  # низ
            neighbours = [
                self.curr_generation[y][x + 1],
                self.curr_generation[y - 1][x],
                self.curr_generation[y - 1][x + 1],
                self.curr_generation[y][x - 1],
                self.curr_generation[y - 1][x - 1],
            ]
        if x == 0 and 0 < y < len(self.curr_generation) - 1:  # лево
            neighbours = [
                self.curr_generation[y][x + 1],
                self.curr_generation[y + 1][x],
                self.curr_generation[y + 1][x + 1],
                self.curr_generation[y - 1][x],
                self.curr_generation[y - 1][x + 1],
            ]
        if x == len(self.curr_generation[0]) - 1 and 0 < y < len(self.curr_generation) - 1:  # право
            neighbours = [
                self.curr_generation[y][x - 1],
                self.curr_generation[y + 1][x],
                self.curr_generation[y + 1][x - 1],
                self.curr_generation[y - 1][x],
                self.curr_generation[y - 1][x - 1],
            ]
        return neighbours

    def get_next_generation(self) -> Grid:
        new_generation = copy.deepcopy(self.curr_generation)
        for i in range(len(self.curr_generation)):
            for j in range(len(self.curr_generation[0])):
                n = sum(self.get_neighbours((i, j)))
                if self.curr_generation[i][j] == 1:
                    if n == 2 or n == 3:
                        new_generation[i][j] = 1
                    else:
                        new_generation[i][j] = 0
                else:
                    if n == 3:
                        new_generation[i][j] = 1
                    else:
                        new_generation[i][j] = 0
        return new_generation

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.generations += 1
        self.prev_generation = copy.deepcopy(self.curr_generation)
        self.curr_generation = self.get_next_generation()

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations and self.generations >= self.max_generations:
            return True
        return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.prev_generation != self.curr_generation:
            return True
        return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        grid = []
        with open(f"{filename}") as file:
            lines = file.readlines()
        for i in range(len(lines)):
            row = []
            for j in range(len(lines[0])):
                row.append(int(lines[i][j]))
            grid.append(row)
        game = GameOfLife((len(grid), len(grid[0])))
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(f"{filename}", "w") as file:
            for i in range(len(self.curr_generation)):
                row = ""
                for j in range(len(self.curr_generation)):
                    row += str(self.curr_generation[i][j])
                file.write(row)
                #done
