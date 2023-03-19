from typing import Any, List

import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):
    grid: List[List[Any]]

    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)

        self.cell_size = cell_size

        self.width = self.life.cols * self.cell_size
        self.height = self.life.rows * self.cell_size

        # Устанавливаем размер окна
        self.screen_size = self.width, self.height
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
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
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

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.grid = self.life.create_grid(randomize=True)

        pause = False
        gameon = True
        while self.life.is_changing and gameon and not self.life.is_max_generations_exceeded:
            for event in pygame.event.get():
                # проверить закрытие окна
                if event.type == pygame.QUIT:
                    gameon = False
                # click actions
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = event.pos
                    (
                        x,
                        y,
                    ) = (
                        x // self.cell_size,
                        y // self.cell_size,
                    )
                    self.life.curr_generation[y][x] = 0 if self.life.curr_generation[y][x] == 1 else 1
                    self.draw_grid()
                    pygame.display.flip()
                # pause
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                    pause = not pause
            if pause:
                self.draw_grid()
                self.draw_lines()
                pygame.display.flip()
                continue
