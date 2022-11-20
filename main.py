import numpy as np
import pandas as pd
import random as rnd
from PointClass import point
import matplotlib.pyplot as plt
import copy

def main():

    df = pd.read_excel("data.xlsx")
    df.dropna(how='all')
    k = int(input('Введите количество кластеров: '))
    names = df['Name'].values
    x = df['X'].values
    y = df['Y'].values

    points = [] #список всех точек
    e = [] #список центров
    clusters = {} #словарь кластеров ключ: индекс центра, значение: массив точек
    for i in range(df.shape[0]):
        points.append(point(df['Name'].iloc[i],
                            df['X'].iloc[i],
                            df['Y'].iloc[i]))
    for i in range(k):
        t = rnd.randint(0, len(points)-1)
        while contains(points[t], e):
            t = rnd.randint(0, len(points) - 1)
        e.append(point(
            str(f'e{i+1}'), points[t].x, points[t].y
        ))
        clusters[i] = []
    flag = False
    t = 0
    while not flag:
        for key in clusters.keys():
            clusters[key].clear()
        temp = copy.deepcopy(e)
        for i in range(len(points)): #заполняем кластеры
            d_min = points[i].distance(e[0]) #расстояние до центра
            index_min = 0
            for j in range(k):
                if d_min > points[i].distance(e[j]):
                    d_min = points[i].distance(e[j])
                    index_min = j
            clusters[index_min].append(points[i])
        for i in range(len(e)): #пересчет центров
            e[i].x = sum([p.x for p in clusters[i]])/len(clusters[i])
            e[i].y = sum([p.y for p in clusters[i]])/len(clusters[i])
        t += 1
        # plt.scatter(x=[p.x for p in e], y=[p.y for p in e], c='black')
        # plt.title(f'{t}')
        # plt.grid()
        # plt.show()
        # ax = fig.add_subplot(t, 1, t)
        # ax.scatter(x=[p.x for p in e], y=[p.y for p in e], c='black')
        # ax.set_title(f'{t}')
        flag = stop(e, temp)
        print('')
    print('')

def stop(e, temp):

    for i in range(len(e)):
        if not e[i].equal(temp[i]):
            return False
    return True


def contains(point, e):
    for i in range(len(e)):
        if e[i].equal(point):
            return True
    return False

if __name__ == '__main__':
    main()


