# Практическая работа #4 - Разработка механик и эффектов в 2D-игре с использованием Pygame

**Цель работы:**

Освоить реализацию простых механик, эффектов и взаимодействий в рамках 2D-игр, используя pygame. Каждая механика разрабатывается независимо от остальных на основе одной и той же базовой заготовки игры, что позволяет сосредоточиться на конкретных аспектах каждой реализации.

## Задание 1. Базовая заготовка игры

Этот код представляет собой базовую 2D-игру, созданную с помощью библиотеки Pygame. Он демонстрирует основные принципы создания игрового окна, обработки пользовательского ввода и отрисовки примитивных графических элементов.

**Ключевые моменты:**

*   **Инициализация:** Настраивает Pygame, создаёт окно игры, устанавливает основные параметры (размеры, частоту кадров).
*   **Игровые объекты:**
    *   **Персонаж:** Управляемый синий квадрат с рамкой и диагональными линиями. Его позиция хранится в `player_pos`, а скорость в `player_velocity`.
    *   **Препятствия:** Неподвижные красные квадраты, хранящиеся в списке `objects`.
    *   **Стены:** Чёрные прямоугольники по периметру окна.
*   **Управление:** Персонаж двигается с помощью клавиш-стрелок.
*   **Ограничение движения:** Персонаж не может выходить за границы окна.
*   **Рендеринг:** Экран очищается белым цветом, и на нём отрисовываются стены, персонаж и препятствия.
*   **Игровой цикл:** Управляет частотой кадров, обновляет позицию персонажа и обрабатывает пользовательские события.
*   **Столкновение:** При столкновение персонажа с препятствием, его позиция корректируется, чтобы он не мог их пройти.

## Задание 2. Ближний бой

**Реализованные функциональные возможности:**

*   **Зона атаки:**
    *   При нажатии клавиши "пробел" вокруг персонажа активируется зона атаки, представленная полупрозрачным желтым квадратом.
    *   Размер зоны атаки (квадрат со стороной 100 пикселей) и ее положение (центр совпадает с центром персонажа) можно настраивать.
*   **Активация и продолжительность атаки:**
    *   Атака активируется однократно при каждом нажатии пробела (атака не будет активироваться, пока предыдущая не закончится).
    *   Продолжительность атаки ограничена по времени (500 миллисекунд), что предотвращает бесконечную атаку.
*   **Взаимодействие с врагами:**
    *   При активации зоны атаки все враги, находящиеся внутри нее, немедленно удаляются.
*   **Визуализация:**
    *   Зона атаки отображается как полупрозрачный желтый квадрат, нарисованный под персонажем. Это позволяет видеть, что находится под зоной атаки.
    *   Прозрачность зоны атаки настраивается через альфа-канал цвета.
*   **Прозрачность:**
    *   Используется альфа-канал для отрисовки зоны атаки.

**Использованные подходы и приёмы:**

*   `pygame.Rect`: Прямоугольник используется для представления зоны атаки и столкновений с врагами.
*   `pygame.Surface`: Создана прозрачная поверхность для зоны атаки, позволяющая устанавливать прозрачность.
*   `pygame.SRCALPHA`: Указание для surface, чтобы он использовал альфа-канал при отрисовке.
*   `blit`: Метод для отрисовки одного изображения на другом (зоны атаки под персонажем).
*   **Таймеры:** Использован таймер для ограничения продолжительности атаки, что предотвращает бесконечную атаку.
*   **Флаг `attacking`:** Булева переменная, используемая для управления состоянием атаки.

**Изменения в коде:**

*   Добавлен новый цвет `TRANSPARENT_YELLOW` для полупрозрачной зоны атаки.
*   Добавлена переменная `attacking` для управления состоянием атаки.
*   Добавлена переменная `attack_timer` для отсчета времени атаки.
*   Добавлена переменная `ATTACK_DURATION` для продолжительности атаки.
*   Создание и рендер прозрачной поверхности `attack_surface` для зоны атаки.
*   Изменен порядок отрисовки, теперь зона атаки рисуется под персонажем.

**Результаты:**

*   Реализована базовая механика ближнего боя.
*   Игрок может атаковать, нажав пробел, и удалять врагов, находящихся в зоне атаки.
*   Зона атаки отображается как полупрозрачный квадрат, что визуально удобно для игрока.
*   Атака ограничена по времени, предотвращая бесконечный "спам".

## Задание 3. Гравитация и прыжки

**Основные шаги реализации:**

*   **Введение новых параметров:**
    *   `JUMP_FORCE`: определяет начальную скорость вертикального прыжка.
    *   `GRAVITY`: определяет силу притяжения, влияющую на вертикальную скорость.
    *   `player_pos`: позиция игрока, представленная как список `[x, y]`.
    *   `player_velocity`: скорость игрока, представленная как список `[vx, vy]`.
    *   `is_jumping`: булевый флаг, указывающий, находится ли персонаж в прыжке.
*   **Обработка ввода (прыжок):**
    *   При нажатии клавиши "Space" и если персонаж не находится в прыжке (`not is_jumping`):
        *   вертикальная скорость персонажа устанавливается равной `JUMP_FORCE` (отрицательное значение для движения вверх).
        *   флаг `is_jumping` устанавливается в `True`.
*   **Моделирование гравитации:**
    *   В каждом кадре, вертикальная скорость персонажа `player_velocity[1]` увеличивается на значение `GRAVITY`. Это имитирует постоянное ускорение вниз.
*   **Обновление позиции персонажа:**
    *   Позиция персонажа `player_pos` обновляется на основе его текущей скорости `player_velocity`.
    *   `player_pos[0]` обновляется на `player_velocity[0]`.
    *   `player_pos[1]` обновляется на `player_velocity[1]`.
*   **Обработка столкновений с платформами:**
    *   При столкновении персонажа с платформой и при условии, что персонаж движется вниз (вертикальная скорость `player_velocity[1] >= 0`):
        *   вертикальная позиция персонажа устанавливается на верхний край платформы.
        *   вертикальная скорость устанавливается в `0`.
        *   флаг `is_jumping` устанавливается в `False`, разрешая новый прыжок.
*   **Ограничение падения:**
    *   При достижении персонажем нижнего края экрана:
        *   вертикальная позиция персонажа фиксируется у нижней границы.
        *   вертикальная скорость сбрасывается до `0`.
        *   флаг `is_jumping` устанавливается в `False`.
*   **Флаги для управления движением**
    *   Используются `moving_left` и `moving_right` для того чтобы отслеживать какие клавиши нажаты. Движение останавливается только если другая клавиша не удерживается, это предотвращает застревание персонажа.

**Основные принципы работы:**

*   **Прыжок:** Изначальное изменение вертикальной скорости на отрицательное значение, которое движет персонажа вверх.
*   **Гравитация:** Постепенное увеличение вертикальной скорости вниз, имитирующее силу притяжения.
*   **Столкновения:** Обнаружение пересечений с платформами и землей, чтобы остановить падение и приземлить персонажа.

**Результаты:**

*   Персонаж может прыгать, набирая высоту и падая вниз под действием гравитации.
*   Персонаж останавливается на платформах и на земле, а не падает сквозь них.
*   Имеется базовая физика для платформера, которую можно расширять в дальнейшем.

## Задание 6. Сбор предметов

**Реализация:**

*   **Монеты:**
    *   Был создан список `coins` для хранения объектов-монет (прямоугольников `pygame.Rect`).
    *   Первоначально монеты размещались в случайных местах, но с учетом того, чтобы они не перекрывали платформы.
    *   Реализована проверка столкновений между персонажем и монетами, используя `colliderect()`.
    *   Собранные монеты удалялись из списка `coins` для их исчезновения с экрана.
    *   Было реализовано постепенное добавление новых монет на экран через заданный интервал, если общее их количество меньше заданного максимума (`MAX_COINS`).
*   **Счет:**
    *   Была введена переменная `score` для отслеживания количества собранных монет.
    *   При столкновении персонажа с монетой, `score` увеличивался на единицу.
    *   Счет отображался на экране в левом верхнем углу с использованием шрифта `pygame.font`.
*   **Таймер добавления монет:**
    *   Был реализован таймер `coin_timer` для контроля интервала между добавлением новых монет.
    *   Задан интервал `COIN_INTERVAL` в миллисекундах, через который происходит добавление новой монеты.
    *   Таймер обнуляется после каждого добавления.

**Результаты:**

*   В игру успешно добавлена механика сбора монет.
*   Игрок может собирать монеты, которые исчезают после столкновения с персонажем.
*   Ведется счет собранных монет, который отображается на экране.
*   Монеты постепенно добавляются на экран, если их количество меньше заданного максимума, что делает игру более динамичной.

**Проблемы и их решения:**

*   **Начальное размещение монет:** Была решена проблема с размещением монет внутри платформ путем проверки их столкновения с платформами при создании. Монеты перегенерировались до тех пор, пока не оказывались вне платформ.
*   **Динамическое добавление монет:** Изначально монеты появлялись только один раз в начале игры. Был реализован таймер и проверка на количество монет, что позволило добавить монеты на протяжении всей игры.
