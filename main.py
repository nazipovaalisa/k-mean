# from filecmp import cmp

import numpy as np
import pandas as pd
import random as rnd
from PointClass import point
import matplotlib.pyplot as plt
import copy
import matplotlib
from typing import Dict


# matplotlib.use("TkAgg")

def main():
    df = pd.read_excel("data.xlsx", sheet_name='Лист2')
    df.dropna(how='all')
    k = int(input('Введите количество кластеров: '))
    v = int(input('Выберите вариант метода: '))
    names = df.columns

    points = []  # список всех точек
    e = []  # список центров
    clusters = {}  # словарь кластеров ключ: индекс центра, значение: массив точек

    for name in names:  # заполняем список точек
        points.append(point(name, df[name].values))

    for i in range(k):  # заполняем список центров
        t = rnd.randint(0, len(points) - 1)
        while contains(points[t], e):
            t = rnd.randint(0, len(points) - 1)
        e.append(point(
            str(f'e{i + 1}'), points[t].coords
        ))
        clusters[i] = []

    flag = False
    t = 0
    while not flag:
        temp = copy.deepcopy(clusters)
        for key in clusters.keys():
            clusters[key].clear()  # чистим кластеры
        for i in range(len(points)):  # заполняем кластеры
            d_min = points[i].distance(e[0])  # расстояние до центра
            index_min = 0
            for j in range(k):
                if d_min > points[i].distance(e[j]):
                    d_min = points[i].distance(e[j])
                    index_min = j
            clusters[index_min].append(points[i])
            if v == 2:
                e[index_min] = change_center(e[index_min], clusters[index_min])
        if v == 1:
            for i in range(len(e)):  # пересчет центров
                e[i] = change_center(e[i], clusters[i])
        if t > 0:
            flag = stop(temp, clusters)
        t += 1
    print()


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
    for i in range(len(e)):
        if np.array_equal(e[i].coords, point.coords):
            return True
    return False


if __name__ == '__main__':
    main()
