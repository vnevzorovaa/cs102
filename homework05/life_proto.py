import copy
import random
import typing as tp
from typing import Any, List

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    grid: tp.List[tp.List[Any]]

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        # Первая отрисовка поля
        self.grid = [[]]

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_grid()
            self.draw_lines()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.grid = self.get_next_generation()
            self.draw_grid()
            self.draw_lines()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        grid = [
            [random.randint(0, 1) if randomize else 0 for j in range(self.cell_width)] for i in range(self.cell_height)
        ]
        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                rect = (
                    j * self.cell_size,
                    i * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(
                    self.screen,
                    pygame.Color("green") if self.grid[i][j] == 1 else pygame.Color("white"),
                    rect,
                )

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        y, x = cell
        neighbours = []
        if 0 < x < len(self.grid[0]) - 1 and 0 < y < len(self.grid) - 1:
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    neighbours.append(self.grid[y + i][x + j])
            del neighbours[4]
        if x == 0 and y == 0:  # верхний левый угол
            neighbours = [self.grid[y][x + 1], self.grid[y + 1][x], self.grid[y + 1][x + 1]]
        if x == 0 and y == len(self.grid) - 1:  # нижний левый угол
            neighbours = [self.grid[y][x + 1], self.grid[y - 1][x], self.grid[y - 1][x + 1]]
        if x == len(self.grid[0]) - 1 and y == 0:  # верхний правый угол
            neighbours = [self.grid[y][x - 1], self.grid[y + 1][x], self.grid[y + 1][x - 1]]
        if x == len(self.grid[0]) - 1 and y == len(self.grid) - 1:  # нижний правый угол
            neighbours = [self.grid[y][x - 1], self.grid[y - 1][x], self.grid[y - 1][x - 1]]
        if 0 < x < len(self.grid[0]) - 1 and y == 0:  # верх
            neighbours = [
                self.grid[y][x + 1],
                self.grid[y + 1][x],
                self.grid[y + 1][x + 1],
                self.grid[y][x - 1],
                self.grid[y + 1][x - 1],
            ]
        if x == len(self.grid[0]) - 1 and 0 < y < len(self.grid) - 1:  # право
            neighbours = [
                self.grid[y][x - 1],
                self.grid[y + 1][x],
                self.grid[y + 1][x - 1],
                self.grid[y - 1][x],
                self.grid[y - 1][x - 1],
            ]
        if 0 < x < len(self.grid[0]) - 1 and y == len(self.grid) - 1:  # низ
            neighbours = [
                self.grid[y][x + 1],
                self.grid[y - 1][x],
                self.grid[y - 1][x + 1],
                self.grid[y][x - 1],
                self.grid[y - 1][x - 1],
            ]
        if x == 0 and 0 < y < len(self.grid) - 1:  # лево
            neighbours = [
                self.grid[y][x + 1],
                self.grid[y + 1][x],
                self.grid[y + 1][x + 1],
                self.grid[y - 1][x],
                self.grid[y - 1][x + 1],
            ]
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        next_generation = copy.deepcopy(self.grid)
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                n = sum(self.get_neighbours((i, j)))
                if self.grid[i][j] == 1:
                    if n == 2 or n == 3:
                        next_generation[i][j] = 1
                    else:
                        next_generation[i][j] = 0
                else:
                    if n == 3:
                        next_generation[i][j] = 1
                    else:
                        next_generation[i][j] = 0
        return next_generation


if __name__ == "__main__":
    life = GameOfLife()
    life.run()
