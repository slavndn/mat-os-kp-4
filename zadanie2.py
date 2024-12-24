import pygame
import sys
import random

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
YELLOW = (255, 255, 0)
TRANSPARENT_YELLOW = (255, 255, 0, 100)  # Прозрачный желтый (последнее число - альфа-канал)


# Размеры персонажа и объектов
PLAYER_SIZE = 50
PLAYER_BORDER_THICKNESS = 2
OBJECT_SIZE = 50
WALL_THICKNESS = 5
ATTACK_SIZE = 100  # Размер зоны атаки

# Скорость движения персонажа
PLAYER_SPEED = 5

# Инициализация окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Ближний бой 2D-игра")
clock = pygame.time.Clock()

# Враги
objects = [
    pygame.Rect(200, 150, OBJECT_SIZE, OBJECT_SIZE),
    pygame.Rect(400, 300, OBJECT_SIZE, OBJECT_SIZE),
    pygame.Rect(600, 450, OBJECT_SIZE, OBJECT_SIZE)
]

# Начальная позиция персонажа вне объектов
def get_valid_starting_position(excluded_objects):
    while True:
        x = random.randint(WALL_THICKNESS, WINDOW_WIDTH - PLAYER_SIZE - WALL_THICKNESS)
        y = random.randint(WALL_THICKNESS, WINDOW_HEIGHT - PLAYER_SIZE - WALL_THICKNESS)
        rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        if not any(rect.colliderect(obj) for obj in excluded_objects):
            return [x, y]

player_pos = get_valid_starting_position(objects)
player_velocity = [0, 0]  # Скорость по X и Y

# Проверка столкновений персонажа с врагами
def check_collision_with_objects(new_rect, objects):
    return any(new_rect.colliderect(obj) for obj in objects)


# Периодическое появление врагов
def spawn_enemy():
    if len(objects) >= 10:
        return
    while True:
        x = random.randint(WALL_THICKNESS, WINDOW_WIDTH - OBJECT_SIZE - WALL_THICKNESS)
        y = random.randint(WALL_THICKNESS, WINDOW_HEIGHT - OBJECT_SIZE - WALL_THICKNESS)
        new_enemy = pygame.Rect(x, y, OBJECT_SIZE, OBJECT_SIZE)
        if not new_enemy.colliderect(pygame.Rect(*player_pos, PLAYER_SIZE, PLAYER_SIZE)) and \
                not any(new_enemy.colliderect(obj) for obj in objects):
            objects.append(new_enemy)
            break
SPAWN_INTERVAL = 3000  # Интервал в миллисекундах
time_since_last_spawn = 0

# Переменная для отслеживания активности атаки
attacking = False
attack_timer = 0
ATTACK_DURATION = 500 # Продолжительность атаки в миллисекундах


# Основной игровой цикл
running = True
while running:
    delta_time = clock.tick(FPS)
    time_since_last_spawn += delta_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_velocity[0] = -PLAYER_SPEED
            elif event.key == pygame.K_RIGHT:
                player_velocity[0] = PLAYER_SPEED
            elif event.key == pygame.K_UP:
                player_velocity[1] = -PLAYER_SPEED
            elif event.key == pygame.K_DOWN:
                player_velocity[1] = PLAYER_SPEED
            elif event.key == pygame.K_SPACE and not attacking: # Атака ближнего боя
                 attacking = True
                 attack_timer = 0 # Запускаем таймер атаки

        elif event.type == pygame.KEYUP:
            if event.key in {pygame.K_LEFT, pygame.K_RIGHT}:
                player_velocity[0] = 0
            elif event.key in {pygame.K_UP, pygame.K_DOWN}:
                player_velocity[1] = 0

    # Атака
    if attacking:
        attack_timer += delta_time
        attack_zone = pygame.Rect(
                player_pos[0] - (ATTACK_SIZE - PLAYER_SIZE) // 2,
                player_pos[1] - (ATTACK_SIZE - PLAYER_SIZE) // 2,
                ATTACK_SIZE,
                ATTACK_SIZE
            )
        # Удаление врагов, попавших в зону атаки
        objects = [obj for obj in objects if not attack_zone.colliderect(obj)]
        if attack_timer >= ATTACK_DURATION:
            attacking = False


    # Появление нового врага
    if time_since_last_spawn >= SPAWN_INTERVAL:
        spawn_enemy()
        time_since_last_spawn = 0

    # Обновление позиции персонажа
    new_pos_x = player_pos[0] + player_velocity[0]
    new_pos_y = player_pos[1] + player_velocity[1]

    # Проверка на столкновения с врагами
    new_rect = pygame.Rect(new_pos_x, new_pos_y, PLAYER_SIZE, PLAYER_SIZE)
    if not check_collision_with_objects(new_rect, objects):
        player_pos[0] = new_pos_x
        player_pos[1] = new_pos_y

    # Ограничение движения персонажа внутри игрового окна с учётом стен
    player_pos[0] = max(WALL_THICKNESS, min(player_pos[0], WINDOW_WIDTH - PLAYER_SIZE - WALL_THICKNESS))
    player_pos[1] = max(WALL_THICKNESS, min(player_pos[1], WINDOW_HEIGHT - PLAYER_SIZE - WALL_THICKNESS))

    # Рендеринг объектов
    screen.fill(WHITE)

    # Отрисовка стен
    pygame.draw.rect(screen, BLACK, (0, 0, WINDOW_WIDTH, WALL_THICKNESS))  # Верхняя стена
    pygame.draw.rect(screen, BLACK, (0, 0, WALL_THICKNESS, WINDOW_HEIGHT))  # Левая стена
    pygame.draw.rect(screen, BLACK, (0, WINDOW_HEIGHT - WALL_THICKNESS, WINDOW_WIDTH, WALL_THICKNESS))  # Нижняя стена
    pygame.draw.rect(screen, BLACK, (WINDOW_WIDTH - WALL_THICKNESS, 0, WALL_THICKNESS, WINDOW_HEIGHT))  # Правая стена

    # Отрисовка зоны атаки, если она активна
    if attacking:
        attack_surface = pygame.Surface((ATTACK_SIZE, ATTACK_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(attack_surface, TRANSPARENT_YELLOW, (0, 0, ATTACK_SIZE, ATTACK_SIZE))
        screen.blit(attack_surface, (player_pos[0] - (ATTACK_SIZE - PLAYER_SIZE) // 2, player_pos[1] - (ATTACK_SIZE - PLAYER_SIZE) // 2))


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

    # Отрисовка врагов
    for obj in objects:
        pygame.draw.rect(screen, RED, obj)

    # Обновление экрана
    pygame.display.flip()