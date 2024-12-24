Практическая работа #4 - Разработка механик и эффектов в
2D-игре с использованием Pygame
Цель работы
Освоить реализацию простых механик, эффектов и взаимодействий в рамках 2D-игр, используя pygame. Каждая механика разрабатывается независимо от остальных на основе одной и той же базовой заготовки игры, что позволяет
сосредоточиться на конкретных аспектах каждой реализации.

Задание 1. Базовая заготовка игры

Этот код представляет собой базовую 2D-игру, созданную с помощью библиотеки Pygame. Он демонстрирует основные принципы создания игрового окна, обработки пользовательского ввода и отрисовки примитивных графических элементов.

Ключевые моменты:

Инициализация: Настраивает Pygame, создаёт окно игры, устанавливает основные параметры (размеры, частоту кадров).

Игровые объекты:

Персонаж: Управляемый синий квадрат с рамкой и диагональными линиями. Его позиция хранится в player_pos, а скорость в player_velocity.

Препятствия: Неподвижные красные квадраты, хранящиеся в списке objects.

Стены: Чёрные прямоугольники по периметру окна.

Управление: Персонаж двигается с помощью клавиш-стрелок.

Ограничение движения: Персонаж не может выходить за границы окна.

Рендеринг: Экран очищается белым цветом, и на нём отрисовываются стены, персонаж и препятствия.

Игровой цикл: Управляет частотой кадров, обновляет позицию персонажа и обрабатывает пользовательские события.

Столкновение: При столкновение персонажа с препятствием, его позиция корректируется, чтобы он не мог их пройти.


Задание 2. Ближний бой
Реализованные функциональные возможности:

Зона атаки:

При нажатии клавиши "пробел" вокруг персонажа активируется зона атаки, представленная полупрозрачным желтым квадратом.

Размер зоны атаки (квадрат со стороной 100 пикселей) и ее положение (центр совпадает с центром персонажа) можно настраивать.

Активация и продолжительность атаки:

Атака активируется однократно при каждом нажатии пробела (атака не будет активироваться, пока предыдущая не закончится).

Продолжительность атаки ограничена по времени (500 миллисекунд), что предотвращает бесконечную атаку.

Взаимодействие с врагами:

При активации зоны атаки все враги, находящиеся внутри нее, немедленно удаляются.

Визуализация:

Зона атаки отображается как полупрозрачный желтый квадрат, нарисованный под персонажем. Это позволяет видеть, что находится под зоной атаки.

Прозрачность зоны атаки настраивается через альфа-канал цвета.

Прозрачность:

Используется альфа-канал для отрисовки зоны атаки.

Использованные подходы и приёмы:

pygame.Rect: Прямоугольник используется для представления зоны атаки и столкновений с врагами.

pygame.Surface: Создана прозрачная поверхность для зоны атаки, позволяющая устанавливать прозрачность.

pygame.SRCALPHA: Указание для surface, чтобы он использовал альфа-канал при отрисовке.

blit: Метод для отрисовки одного изображения на другом (зоны атаки под персонажем).

Таймеры: Использован таймер для ограничения продолжительности атаки, что предотвращает бесконечную атаку.

Флаг attacking: Булева переменная, используемая для управления состоянием атаки.

Изменения в коде:

Добавлен новый цвет TRANSPARENT_YELLOW для полупрозрачной зоны атаки.

Добавлена переменная attacking для управления состоянием атаки.

Добавлена переменная attack_timer для отсчета времени атаки.

Добавлена переменная ATTACK_DURATION для продолжительности атаки.

Создание и рендер прозрачной поверхности attack_surface для зоны атаки.

Изменен порядок отрисовки, теперь зона атаки рисуется под персонажем.

Результаты:

Реализована базовая механика ближнего боя.

Игрок может атаковать, нажав пробел, и удалять врагов, находящихся в зоне атаки.

Зона атаки отображается как полупрозрачный квадрат, что визуально удобно для игрока.

Атака ограничена по времени, предотвращая бесконечный "спам".

Задание 3. Гравитация и прыжки

