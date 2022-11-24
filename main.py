import numpy as np
import pandas as pd
import random as rnd
from PointClass import point
import matplotlib.pyplot as plt
import copy
import matplotlib

# matplotlib.use("TkAgg")

def main():
    df = pd.read_excel("data.xlsx")
    df.dropna(how='all')
    k = int(input('Введите количество кластеров: '))
    names = df.columns

    points = []  # список всех точек
    e = []  # список центров
    clusters = {}  # словарь кластеров ключ: индекс центра, значение: массив точек

    for name in names: #заполняем список точек
        points.append(point(name, df[name].values))

    for i in range(k): #заполняем список центров
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
        for key in clusters.keys():
            clusters[key].clear() #чистим кластеры
        temp = copy.deepcopy(e)
        for i in range(len(points)):  # заполняем кластеры
            d_min = points[i].distance(e[0])  # расстояние до центра
            index_min = 0
            for j in range(k):
                if d_min > points[i].distance(e[j]):
                    d_min = points[i].distance(e[j])
                    index_min = j
            clusters[index_min].append(points[i])
        for i in range(len(e)):  # пересчет центров
            e_new = point(e[i].name, np.array([]))
            for j in range(e[i].coords.size):
                cord = [p.coords[j] for p in clusters[i]]
                e_new.coords = np.append(e_new.coords, np.average(cord))
            e[i] = e_new
        t += 1
        flag = stop(e, temp)
    print()


def stop(e, temp):
    for i in range(len(e)):
        if not np.array_equal(e[i].coords, temp[i].coords):
            return False
    return True

def contains(point, e):
    for i in range(len(e)):
        if np.array_equal(e[i].coords, point.coords):
            return True
    return False


if __name__ == '__main__':
    main()
