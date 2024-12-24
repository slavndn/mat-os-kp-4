import pygame
import sys

# Инициализация Pygame
pygame.init()

# Параметры окна
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Размеры персонажа и объектов
PLAYER_SIZE = 50
PLAYER_BORDER_THICKNESS = 2
OBJECT_SIZE = 50
WALL_THICKNESS = 5

# Скорость движения персонажа
PLAYER_SPEED = 5
JUMP_FORCE = -15  # Начальная скорость прыжка (отрицательное значение для движения вверх)
GRAVITY = 1  # Сила гравитации

# Инициализация окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Гравитация и прыжки")
clock = pygame.time.Clock()

# Переменные персонажа
player_pos = [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2]
player_velocity = [0, 0]  # Скорость по X и Y
is_jumping = False  # Флаг, указывающий, находится ли персонаж в прыжке

# Платформы
platforms = [
    pygame.Rect(200, 400, 200, 20),  # Пример платформ
    pygame.Rect(500, 300, 200, 20),
    pygame.Rect(300, 500, 200, 20)
]

# Добавляем флаги для управления движением
moving_left = False
moving_right = False


# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moving_left = True
                player_velocity[0] = -PLAYER_SPEED
            elif event.key == pygame.K_RIGHT:
                moving_right = True
                player_velocity[0] = PLAYER_SPEED
            elif event.key == pygame.K_SPACE and not is_jumping:  # Прыжок
                player_velocity[1] = JUMP_FORCE
                is_jumping = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
                if not moving_right:  # Сбрасываем скорость, только если не двигаемся вправо
                    player_velocity[0] = 0
            elif event.key == pygame.K_RIGHT:
                moving_right = False
                if not moving_left:  # Сбрасываем скорость, только если не двигаемся влево
                    player_velocity[0] = 0

    # Обновление вертикальной скорости под действием гравитации
    player_velocity[1] += GRAVITY

    # Обновление позиции персонажа
    player_pos[0] += player_velocity[0]
    player_pos[1] += player_velocity[1]

    # Ограничение движения персонажа внутри окна
    player_pos[0] = max(WALL_THICKNESS, min(player_pos[0], WINDOW_WIDTH - PLAYER_SIZE - WALL_THICKNESS))

    # Проверка столкновений с платформами
    player_rect = pygame.Rect(player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE)
    on_ground = False
    for platform in platforms:
        if player_rect.colliderect(platform) and player_velocity[1] >= 0:  # Проверка на нахождение сверху
            player_pos[1] = platform.top - PLAYER_SIZE  # Установка позиции поверх платформы
            player_velocity[1] = 0  # Сброс вертикальной скорости
            is_jumping = False
            on_ground = True
            break

    # Ограничение падения до нижней границы окна
    if player_pos[1] + PLAYER_SIZE >= WINDOW_HEIGHT:
        player_pos[1] = WINDOW_HEIGHT - PLAYER_SIZE
        player_velocity[1] = 0
        is_jumping = False
        on_ground = True

    # Рендеринг объектов
    screen.fill(WHITE)

    # Отрисовка стен
    pygame.draw.rect(screen, BLACK, (0, 0, WINDOW_WIDTH, WALL_THICKNESS))  # Верхняя стена
    pygame.draw.rect(screen, BLACK, (0, 0, WALL_THICKNESS, WINDOW_HEIGHT))  # Левая стена
    pygame.draw.rect(screen, BLACK, (0, WINDOW_HEIGHT - WALL_THICKNESS, WINDOW_WIDTH, WALL_THICKNESS))  # Нижняя стена
    pygame.draw.rect(screen, BLACK, (WINDOW_WIDTH - WALL_THICKNESS, 0, WALL_THICKNESS, WINDOW_HEIGHT))  # Правая стена

    # Отрисовка персонажа с перекрестием
    pygame.draw.rect(screen, BLUE, (*player_pos, PLAYER_SIZE, PLAYER_SIZE), PLAYER_BORDER_THICKNESS)  # Рамка
    pygame.draw.line(screen, BLUE,
                     (player_pos[0], player_pos[1]),
                     (player_pos[0] + PLAYER_SIZE, player_pos[1] + PLAYER_SIZE),
                     2)  # Диагональная линия
    pygame.draw.line(screen, BLUE,
                     (player_pos[0] + PLAYER_SIZE, player_pos[1]),
                     (player_pos[0], player_pos[1] + PLAYER_SIZE),
                     2)  # Обратная диагональ

    # Отрисовка платформ
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, platform)

    # Обновление экрана
    pygame.display.flip()
    clock.tick(FPS)