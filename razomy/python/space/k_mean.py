import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import random


# --- 1. Генерация неравномерного мира ---
def generate_data(num_points, width, height):
    points = []
    # Создаем 3 "города" (плотных кластера)
    centers = [(width * 0.2, height * 0.2), (width * 0.8, height * 0.7), (width * 0.5, height * 0.5)]

    for _ in range(num_points):
        # 70% точек кучкуются вокруг центров, 30% - случайный шум
        if random.random() < 0.7:
            center = random.choice(centers)
            x = np.random.normal(center[0], width * 0.08)
            y = np.random.normal(center[1], height * 0.08)
        else:
            x = random.uniform(0, width)
            y = random.uniform(0, height)
        points.append([x, y])
    return np.array(points)


# --- 2. Алгоритм K-Means (Ллойда) ---
# Это и есть "Симуляция": центры сами ползут в гущу событий
def find_optimal_positions(points, k_modems, iterations=10):
    # 1. Случайно ставим модемы
    # Берем k случайных точек из данных как стартовые позиции
    indices = np.random.choice(points.shape[0], k_modems, replace=False)
    centroids = points[indices]

    for i in range(iterations):
        # Шаг А: Для каждой точки находим ближайший модем
        # Расчет дистанций от всех точек до всех центроидов
        distances = np.linalg.norm(points[:, np.newaxis] - centroids, axis=2)
        closest_modem_index = np.argmin(distances, axis=1)

        # Шаг Б: Двигаем модем в центр масс его группы
        new_centroids = []
        for modem_id in range(k_modems):
            # Берем все точки, которые относятся к этому модему
            modem_points = points[closest_modem_index == modem_id]

            if len(modem_points) > 0:
                # Новая позиция = среднее арифметическое координат
                new_pos = modem_points.mean(axis=0)
                new_centroids.append(new_pos)
            else:
                # Если модем потерял все точки, кидаем его в случайное место (респавн)
                new_centroids.append(points[np.random.choice(len(points))])

        centroids = np.array(new_centroids)

    return centroids, closest_modem_index


# --- 3. Визуализация ---
def visualize(points, centroids, labels, width, height, radius=None):
    fig, ax = plt.subplots(figsize=(10, 8))

    # Рисуем Диаграмму Вороного (Границы влияния модемов)
    # Добавляем фиктивные точки далеко за краями, чтобы ворогой корректно рисовал границы на краях
    dummy_points = np.array([[-width, -height], [2 * width, -height],
                             [-width, 2 * height], [2 * width, 2 * height]])
    vor_points = np.vstack([centroids, dummy_points])
    vor = Voronoi(vor_points)
    voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='orange', line_width=2, line_alpha=0.6, point_size=0)

    # Рисуем обычные точки, раскрашенные по принадлежности к модему
    ax.scatter(points[:, 0], points[:, 1], c=labels, cmap='viridis', s=10, alpha=0.5, label='Пользователи')

    # Рисуем Модемы
    ax.scatter(centroids[:, 0], centroids[:, 1], c='red', s=150, marker='X', edgecolors='black',
               label='МОДЕМЫ (Центры)')

    # Рисуем радиус покрытия (если есть задача про "5 литров" или дальность связи)
    if radius:
        for c in centroids:
            circle = plt.Circle((c[0], c[1]), radius, color='red', fill=False, linestyle='--', linewidth=1.5)
            ax.add_patch(circle)

    ax.set_xlim(0, width)
    ax.set_ylim(0, height)
    ax.set_title("Оптимизация размещения (K-Means + Voronoi)\nОранжевые линии - границы секторов влияния")
    plt.legend()
    plt.show()


# --- ЗАПУСК ---
W, H = 1000, 1000
N_POINTS = 500
N_MODEMS = 5  # Сколько у нас ресурсов (модемов / ведер воды)
COVERAGE_R = 150  # Радиус действия модема

# 1. Создаем мир
data_points = generate_data(N_POINTS, W, H)

# 2. Ищем идеальные места (Симуляция 20 итераций)
best_positions, clusters = find_optimal_positions(data_points, N_MODEMS, iterations=20)

# 3. Рисуем результат
visualize(data_points, best_positions, clusters, W, H, radius=COVERAGE_R)