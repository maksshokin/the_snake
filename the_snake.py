from random import randint

import pygame

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

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
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
        self.position = (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT / 2 - 20)
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод"""
        pass

class Apple(GameObject):
    """Класс яблока на игровом поле"""

    def __init__(self):
        """Атрибуты яблока."""
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Метод возвращает рандомные координаты на поле"""
        cord_y = randint(0, SCREEN_WIDTH - 20) // 20 * 20
        cord_x = randint(0, SCREEN_HEIGHT - 20) // 20 * 20
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
        cord_x = head[0] + self.direction[0] * 20
        cord_y = head[1] + self.direction[1] * 20
        New_head = (cord_x, cord_y)
        self.positions.insert(0, (cord_x, cord_y))
        # Проверка на столкновение с телом
        for pos in self.positions[1:]:
            if New_head == pos:
                self.reset()

        # Телепорт на противоположную сторону
        if cord_x > SCREEN_WIDTH - 20:
            self.positions[0] = (0, self.positions[0][1])
        elif cord_x < 0:
            self.positions[0] = (SCREEN_WIDTH - 20, self.positions[0][1])
        if cord_y > SCREEN_HEIGHT - 20:
            self.positions[0] = (self.positions[0][0], 0)
        elif cord_y < 0:
            self.positions[0] = (self.positions[0][0], SCREEN_HEIGHT - 20)
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
            self.positions.pop(-1)

    def get_head_position(self):
        """Метод возыращает координаты головы."""
        return self.positions[0]

    def reset(self):
        """Метод сбрасывает все до стартовых показателей."""
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [self.position]
        self.body_color = SNAKE_COLOR
 

def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
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
        Snake.draw(snake, screen)
        Apple.draw(apple, screen)
        Snake.update_direction(snake)
        handle_keys(snake)
        Snake.move(snake)
        pygame.display.update()

        # Проверка на "столкновение" с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1

            # Создание нового яблока в месте, где нет хвоста и головы змеи
            Check = True
            while Check:
                if not apple.randomize_position() in snake.positions:
                    Check = False
                    apple.position = apple.randomize_position()
              

if __name__ == '__main__':
    main()