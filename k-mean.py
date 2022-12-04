import numpy as np
import pandas as pd
import random as rnd
from PointClass import point
import matplotlib.pyplot as plt
import copy
import matplotlib
import math

matplotlib.use("TkAgg")

def main():

    df = pd.read_excel("data.xlsx", sheet_name='Лист1')
    df.dropna(how='all')
    k = int(input('Введите количество кластеров: '))
    v = int(input('Выберите вариант метода: '))
    names = df.columns

    points = []  # список всех точек
    e = []  # список центров
    clusters = {}  # словарь кластеров ключ: индекс центра, значение: массив точек

    for name in names:  # заполняем список точек
        points.append(point(name, df[name].values))

    e_list = []
    for i in range(k):  # заполняем список центров
        t = rnd.randint(0, len(points) - 1)
        while contains(points[t], e):
            t = rnd.randint(0, len(points) - 1)
        e.append(point(
            str(f'e{i + 1}'), points[t].coords
        ))
        clusters[i] = []
        e_list.append([])

    e_coords = np.array([e])
    clusters_list = []
    e_dict = {0: copy.deepcopy(e_list)}

    flag = False
    t = 0
    while not flag:
        temp = copy.deepcopy(clusters)
        for i in range(len(e)):
            e_list[i].clear()
        if t > 0:
            for key in clusters.keys():
                clusters[key].clear()  #чистим кластеры
        for i in range(len(points)):  #заполняем кластеры
            d_min = points[i].distance(e[0])  # расстояние до центра
            index_min = 0
            for j in range(k):
                if d_min > points[i].distance(e[j]):
                    d_min = points[i].distance(e[j])
                    index_min = j
            clusters[index_min].append(points[i])
            if v == 2:
                e_new = point(e[index_min].name, np.array([]))
                for j in range(e[index_min].coords.size):
                    e_new.coords = np.append(e_new.coords, np.average([points[i].coords[j],
                                                                       e[index_min].coords[j]]))
                e[index_min] = e_new
                e_list[index_min].append(e_new)
        e_dict[t+1] = copy.deepcopy(e_list)
        if v == 1:
            for i in range(len(e)):  # пересчет центров
                e[i] = change_center(e[i], clusters[i])
        e_coords = np.vstack([e_coords, e])
        cluster_copy = copy.deepcopy(clusters)
        clusters_list.append(cluster_copy)
        if t > 0:
            flag = stop(temp, clusters)
        t += 1
        print(f'{t} итерация')
        for key in clusters.keys():
            print(f'{key} : {str([p.name for p in clusters[key]])}')
    print(f'Координаты центров: {[[p.coords] for p in e]}')
    if e[0].coords.size == 2:
        n = 0
        fig, axes = plt.subplots(nrows=math.ceil((t+1)/2), ncols=2, figsize=(15, 30))
        for ax in axes.flat:
            if n <= t:
                if n == 0:
                    ax.scatter(x=[p.coords[0] for p in points], y=[p.coords[1] for p in points])
                    ax.set(title=f'Координаты точек и начальные центры')
                else:
                    for key in clusters_list[n-1].keys():
                        ax.scatter(x=[p.coords[0] for p in clusters_list[n-1][key]],
                                   y=[p.coords[1] for p in clusters_list[n-1][key]],)
                        ax.set(title=f'{n} итерация')
                    if v == 2:
                        for i in range(len(e)):
                            ax.scatter(x=[p.coords[0] for p in e_coords[n-1]], y=[p.coords[1] for p in e_coords[n-1]],
                                       color='black')
                            ax.scatter(
                                [p.coords[0] for p in e_dict[n][i]],
                                [p.coords[1] for p in e_dict[n][i]], color='black'
                            )
                            ax.plot(
                                [p.coords[0] for p in e_dict[n][i]],
                                [p.coords[1] for p in e_dict[n][i]], color='black'
                            )
                ax.grid()
                ax.scatter(x=[p.coords[0] for p in e_coords[n]], y=[p.coords[1] for p in e_coords[n]], color='red',
                           s=100)
                for p in points:
                    ax.text(p.coords[0]+0.1, p.coords[1], p.name)
                n += 1
        plt.show()
    else:
        print('Графики строятся только размерности = 2')


def stop(temp, clusters):
    for key in clusters.keys():
        for j in range(len(clusters[key])):
            if not contains(clusters[key][j], temp[key]):
                return False
    return True


def change_center(e, cluster):
    e_new = point(e.name, np.array([]))
    for j in range(e.coords.size):
        cord = [p.coords[j] for p in cluster]
        e_new.coords = np.append(e_new.coords, np.average(cord))
    return e_new


def contains(point, e):
    if len(e) == 0:
        return False
    return any([np.array_equal(ep.coords, point.coords) for ep in e])


if __name__ == '__main__':
    main()
