import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from scipy.spatial import Voronoi, voronoi_plot_2d
import random


class InteractiveModemOptimizer:
    def __init__(self, num_points=500, width=1000, height=1000):
        self.width = width
        self.height = height
        self.points = self.generate_data(num_points)
        self.n_modems = 5  # Начинаем с 1 модема
        self.coverage_radius = 150

        # Настройка графиков
        self.fig, self.ax = plt.subplots(figsize=(10, 9))
        plt.subplots_adjust(bottom=0.2)  # Оставим место внизу для кнопок

        # Кнопки
        self.ax_btn_add = plt.axes([0.7, 0.05, 0.2, 0.075])
        self.btn_add = Button(self.ax_btn_add, 'Добавить (+)')
        self.btn_add.on_clicked(self.add_modem)

        self.ax_btn_rem = plt.axes([0.4, 0.05, 0.2, 0.075])
        self.btn_rem = Button(self.ax_btn_rem, 'Убрать (-)')
        self.btn_rem.on_clicked(self.remove_modem)

        # Первый запуск
        self.update_plot()
        plt.show()

    def generate_data(self, num_points):
        """Генерация кластеров (городов)"""
        points = []
        centers = [(self.width * 0.2, self.height * 0.2),
                   (self.width * 0.8, self.height * 0.7),
                   (self.width * 0.5, self.height * 0.5)]

        for _ in range(num_points):
            if random.random() < 0.7:  # 70% жителей в городах
                center = random.choice(centers)
                x = np.random.normal(center[0], self.width * 0.08)
                y = np.random.normal(center[1], self.height * 0.08)
            else:  # 30% живут в лесу
                x = random.uniform(0, self.width)
                y = random.uniform(0, self.height)
            points.append([x, y])
        return np.array(points)

    def run_k_means(self):
        """Алгоритм Ллойда для поиска центров"""
        k = self.n_modems
        # Случайная инициализация
        indices = np.random.choice(self.points.shape[0], k, replace=False)
        centroids = self.points[indices]

        closest_indices = np.zeros(len(self.points))

        # 10 итераций симуляции для стабилизации
        for _ in range(10):
            # 1. Считаем расстояния
            distances = np.linalg.norm(self.points[:, np.newaxis] - centroids, axis=2)
            closest_indices = np.argmin(distances, axis=1)

            # 2. Перемещаем центры
            new_centroids = []
            for i in range(k):
                cluster_points = self.points[closest_indices == i]
                if len(cluster_points) > 0:
                    new_centroids.append(cluster_points.mean(axis=0))
                else:
                    # Респавн если модем остался без работы
                    new_centroids.append(self.points[np.random.choice(len(self.points))])
            centroids = np.array(new_centroids)

        return centroids, closest_indices

    def update_plot(self):
        self.ax.clear()
        self.ax.set_xlim(0, self.width)
        self.ax.set_ylim(0, self.height)
        self.ax.set_title(f"Количество модемов: {self.n_modems}\nАлгоритм ищет оптимальное покрытие", fontsize=14)

        centroids, labels = self.run_k_means()

        # 1. Рисуем зоны Вороного (только если модемов > 1)
        if self.n_modems > 1:
            # Добавляем фиктивные точки далеко за пределами, чтобы линии не улетали в бесконечность
            dummy = np.array([[-self.width, -self.height], [2 * self.width, -self.height],
                              [-self.width, 2 * self.height], [2 * self.width, 2 * self.height]])
            vor_pts = np.vstack([centroids, dummy])
            vor = Voronoi(vor_pts)
            voronoi_plot_2d(vor, ax=self.ax, show_vertices=False, line_colors='orange', line_alpha=0.5, point_size=0)

        # 2. Рисуем жителей (раскрашиваем по кластерам)
        self.ax.scatter(self.points[:, 0], self.points[:, 1], c=labels, cmap='tab20', s=15, alpha=.5)

        # 3. Рисуем Модемы и Радиусы
        self.ax.scatter(centroids[:, 0], centroids[:, 1], c='red', s=120, marker='X', edgecolors='white', alpha=0.5, zorder=10)

        for c in centroids:
            circle = plt.Circle((c[0], c[1]), self.coverage_radius, color='red', fill=True, alpha=0.1)
            self.ax.add_patch(circle)
            circle_border = plt.Circle((c[0], c[1]), self.coverage_radius, color='red', fill=False, alpha=0.2, linestyle='--')
            self.ax.add_patch(circle_border)

        self.fig.canvas.draw_idle()

    def add_modem(self, event):
        self.n_modems += 1
        self.update_plot()

    def remove_modem(self, event):
        if self.n_modems > 1:
            self.n_modems -= 1
            self.update_plot()


# Запуск
app = InteractiveModemOptimizer(num_points=400)