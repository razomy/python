import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import random

# --- 1. Классы для QuadTree ---

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = x # Центр X
        self.y = y # Центр Y
        self.w = w # Половина ширины
        self.h = h # Половина высоты

    def contains(self, point):
        return (point.x >= self.x - self.w and
                point.x < self.x + self.w and
                point.y >= self.y - self.h and
                point.y < self.y + self.h)

    def intersects(self, range):
        return not (range.x - range.w > self.x + self.w or
                    range.x + range.w < self.x - self.w or
                    range.y - range.h > self.y + self.h or
                    range.y + range.h < self.y - self.h)

class QuadTree:
    def __init__(self, boundary, capacity):
        self.boundary = boundary # Объект Rectangle
        self.capacity = capacity # Макс точек в секторе до деления
        self.points = []
        self.divided = False

        # Дочерние узлы
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None

    def subdivide(self):
        x = self.boundary.x
        y = self.boundary.y
        w = self.boundary.w
        h = self.boundary.h

        ne = Rectangle(x + w/2, y + h/2, w/2, h/2)
        self.northeast = QuadTree(ne, self.capacity)

        nw = Rectangle(x - w/2, y + h/2, w/2, h/2)
        self.northwest = QuadTree(nw, self.capacity)

        se = Rectangle(x + w/2, y - h/2, w/2, h/2)
        self.southeast = QuadTree(se, self.capacity)

        sw = Rectangle(x - w/2, y - h/2, w/2, h/2)
        self.southwest = QuadTree(sw, self.capacity)

        self.divided = True

    def insert(self, point):
        if not self.boundary.contains(point):
            return False

        if len(self.points) < self.capacity:
            self.points.append(point)
            return True
        else:
            if not self.divided:
                self.subdivide()
                # Перемещаем существующие точки в детей, чтобы этот узел стал только узлом ветвления
                # (Опционально, но полезно для чистых структур)

            if self.northeast.insert(point): return True
            if self.northwest.insert(point): return True
            if self.southeast.insert(point): return True
            if self.southwest.insert(point): return True

        return False

# --- 2. Генерация неравномерных данных ---

def generate_cluster_data(num_points, width, height):
    points = []

    # 1. Случайный шум (равномерное распределение)
    for _ in range(int(num_points * 0.2)):
        points.append(Point(random.uniform(0, width), random.uniform(0, height)))

    # 2. Плотные кластеры (Гауссово распределение)
    centers = [(width*0.2, height*0.2), (width*0.8, height*0.7), (width*0.5, height*0.5)]
    for _ in range(int(num_points * 0.8)):
        center = random.choice(centers)
        # Разброс (sigma) влияет на плотность кластера
        px = random.gauss(center[0], width * 0.05)
        py = random.gauss(center[1], height * 0.05)

        # Обрезаем, чтобы не вылетели за границы
        px = max(0, min(width, px))
        py = max(0, min(height, py))

        points.append(Point(px, py))

    return points

# --- 3. Визуализация ---

def draw_quadtree(qt, ax):
    # Рисуем прямоугольник текущего узла
    rect = patches.Rectangle(
        (qt.boundary.x - qt.boundary.w, qt.boundary.y - qt.boundary.h),
        qt.boundary.w * 2,
        qt.boundary.h * 2,
        linewidth=1,
        edgecolor='r',
        facecolor='none',
        alpha=0.5
    )
    ax.add_patch(rect)

    if qt.divided:
        draw_quadtree(qt.northeast, ax)
        draw_quadtree(qt.northwest, ax)
        draw_quadtree(qt.southeast, ax)
        draw_quadtree(qt.southwest, ax)

# --- Запуск ---

# Параметры мира
WORLD_W = 800
WORLD_H = 800
NUM_POINTS = 600
SECTOR_CAPACITY = 10 # Если точек больше чем это число, сектор делится

# Создание данных
point_objects = generate_cluster_data(NUM_POINTS, WORLD_W, WORLD_H)

# Инициализация дерева
domain = Rectangle(WORLD_W/2, WORLD_H/2, WORLD_W/2, WORLD_H/2)
qtree = QuadTree(domain, SECTOR_CAPACITY)

# Заполнение дерева
for p in point_objects:
    qtree.insert(p)

# Рисование
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(0, WORLD_W)
ax.set_ylim(0, WORLD_H)
ax.set_aspect('equal')
ax.set_title(f"QuadTree Декомпозиция (Capacity={SECTOR_CAPACITY})\nМаленькие квадраты = Высокая плотность")

# Рисуем точки
x_coords = [p.x for p in point_objects]
y_coords = [p.y for p in point_objects]
ax.scatter(x_coords, y_coords, s=2, c='blue', alpha=0.6, label='Точки')

# Рисуем сетку дерева
draw_quadtree(qtree, ax)

plt.show()