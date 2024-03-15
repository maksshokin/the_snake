from random import randint, choice

import pygame

import sys

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета фона и игровых объектов:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс"""

    body_color = BOARD_BACKGROUND_COLOR  # Будет перезадан в дочерних классах

    def __init__(self, body_color=SNAKE_COLOR):
        """Метод инициализирует базовые атрибуты объекта"""
        self.position = (
            SCREEN_WIDTH // 2 - GRID_SIZE,
            SCREEN_HEIGHT // 2 - GRID_SIZE
        )
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод"""
        NotImplementedError


class Apple(GameObject):
    """Класс яблока на игровом поле"""

    def __init__(self):
        """Атрибуты яблока."""
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Метод возвращает рандомные координаты на поле"""
        cord_x = randint(0, SCREEN_WIDTH - GRID_SIZE) // GRID_SIZE * GRID_SIZE
        cord_y = randint(0, SCREEN_HEIGHT - GRID_SIZE) // GRID_SIZE * GRID_SIZE
        return (cord_x, cord_y)

    def draw(self, surface):
        """Метод draw класса Apple."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс персонажа, за которого будет играть игкрок (змейки)."""

    def __init__(self):
        """Стартовые атрибуты змеи."""
        super().__init__(self)
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [self.position]
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод, отвечающий за движение змейки."""
        head = self.get_head_position()
        directed_right = head[0] + self.direction[0] * GRID_SIZE
        directed_left = head[1] + self.direction[1] * GRID_SIZE
        new_head = (directed_right, directed_left)
        self.positions.insert(0, (directed_right, directed_left))
        # Проверка на столкновение с телом
        for pos in self.positions[1:]:
            if new_head == pos:
                self.reset()

        # Телепорт на противоположную сторону
        height = SCREEN_HEIGHT - GRID_SIZE
        width = SCREEN_WIDTH - GRID_SIZE
        if directed_right > width:
            self.positions[0] = (0, self.positions[0][1])
        elif directed_right < 0:
            self.positions[0] = (width, self.positions[0][1])
        if directed_left > height:
            self.positions[0] = (self.positions[0][0], 0)
        elif directed_left < 0:
            self.positions[0] = (self.positions[0][0], height)
        pass

    def draw(self, surface):
        """Метод draw класса Snake."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Удаление последнего сегмента из списка
        if len(self.positions) != self.length:
            self.positions.pop()

    def get_head_position(self):
        """Метод возыращает координаты головы."""
        return self.positions[0]

    def reset(self):
        """Метод сбрасывает все до стартовых показателей."""
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.positions = [self.position]
        self.body_color = SNAKE_COLOR


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Главная функция игры"""
    snake = Snake()
    apple = Apple()
    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        snake.update_direction()
        handle_keys(snake)
        snake.move()
        pygame.display.update()

        # Проверка на "столкновение" с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1

            # Создание нового яблока в месте, где нет хвоста и головы змеи
            place_not_found = True
            while place_not_found:
                checker = apple.randomize_position()
                if checker not in snake.positions:
                    place_not_found = False
                    apple.position = checker


if __name__ == '__main__':
    main()
