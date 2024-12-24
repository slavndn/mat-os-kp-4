import pygame
import sys

# Инициализация Pygame
pygame.init()

# Параметры окна
WINDOW_WIDTH = 800  # Ширина окна
WINDOW_HEIGHT = 600  # Высота окна
FPS = 60  # Частота обновления кадров

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Размеры персонажа и объектов
PLAYER_SIZE = 50  # Размер стороны квадрата персонажа
PLAYER_BORDER_THICKNESS = 2  # Толщина рамки персонажа
OBJECT_SIZE = 50  # Размер неподвижных объектов
WALL_THICKNESS = 5  # Толщина стен

# Скорость движения персонажа
PLAYER_SPEED = 5  # Пикселей за кадр

# Инициализация окна и часов
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Базовая 2D-игра")
clock = pygame.time.Clock()

# Инициализация персонажа
player_x = WINDOW_WIDTH // 2  # Начальная позиция персонажа по X
player_y = WINDOW_HEIGHT // 2  # Начальная позиция персонажа по Y
player_dx = 0  # Скорость по X
player_dy = 0  # Скорость по Y

# Инициализация неподвижных объектов
objects = [
    pygame.Rect(200, 150, OBJECT_SIZE, OBJECT_SIZE),
    pygame.Rect(400, 300, OBJECT_SIZE, OBJECT_SIZE),
    pygame.Rect(600, 450, OBJECT_SIZE, OBJECT_SIZE),
]

# Основной игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Закрытие окна
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:  # Нажатие клавиши
            if event.key == pygame.K_LEFT:
                player_dx = -PLAYER_SPEED
            elif event.key == pygame.K_RIGHT:
                player_dx = PLAYER_SPEED
            elif event.key == pygame.K_UP:
                player_dy = -PLAYER_SPEED
            elif event.key == pygame.K_DOWN:
                player_dy = PLAYER_SPEED
        elif event.type == pygame.KEYUP:  # Отпускание клавиши
            if event.key in {pygame.K_LEFT, pygame.K_RIGHT}:
                player_dx = 0
            elif event.key in {pygame.K_UP, pygame.K_DOWN}:
                player_dy = 0

    # Обновление позиции персонажа
    player_x += player_dx
    player_y += player_dy

    # Ограничение движения персонажа внутри границ окна
    player_x = max(WALL_THICKNESS, min(player_x, WINDOW_WIDTH - PLAYER_SIZE - WALL_THICKNESS))
    player_y = max(WALL_THICKNESS, min(player_y, WINDOW_HEIGHT - PLAYER_SIZE - WALL_THICKNESS))

    # Проверка столкновений с объектами
    player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
    for obj in objects:
        if player_rect.colliderect(obj):  # Столкновение
            if player_dx > 0:  # Движение вправо
                player_x = obj.left - PLAYER_SIZE - 1
            elif player_dx < 0:  # Движение влево
                player_x = obj.right + 1
            elif player_dy > 0:  # Движение вниз
                player_y = obj.top - PLAYER_SIZE - 1
            elif player_dy < 0:  # Движение вверх
                player_y = obj.bottom + 1

    # Рендеринг объектов
    screen.fill(WHITE)  # Очистка экрана

    # Отрисовка стен
    pygame.draw.rect(screen, BLACK, (0, 0, WINDOW_WIDTH, WALL_THICKNESS))  # Верхняя стена
    pygame.draw.rect(screen, BLACK, (0, 0, WALL_THICKNESS, WINDOW_HEIGHT))  # Левая стена
    pygame.draw.rect(screen, BLACK, (0, WINDOW_HEIGHT - WALL_THICKNESS, WINDOW_WIDTH, WALL_THICKNESS))  # Нижняя стена
    pygame.draw.rect(screen, BLACK, (WINDOW_WIDTH - WALL_THICKNESS, 0, WALL_THICKNESS, WINDOW_HEIGHT))  # Правая стена

    # Отрисовка персонажа
    pygame.draw.rect(screen, BLUE, (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE), PLAYER_BORDER_THICKNESS)
    pygame.draw.line(screen, BLUE, (player_x, player_y), (player_x + PLAYER_SIZE, player_y + PLAYER_SIZE), 2)
    pygame.draw.line(screen, BLUE, (player_x + PLAYER_SIZE, player_y), (player_x, player_y + PLAYER_SIZE), 2)

    # Отрисовка неподвижных объектов
    for obj in objects:
        pygame.draw.rect(screen, RED, obj)

    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)  # Ограничение FPS
