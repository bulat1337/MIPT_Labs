from ast import Param
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
import os
import glob
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

# Директории для CSV файлов и для сохранения графиков
data_dir = 'data'
output_dir = 'graphs'

# Проверяем существование директории для графиков и создаем, если её нет
os.makedirs(output_dir, exist_ok=True)

# Получаем список всех файлов с расширением .csv в папке data
csv_files = glob.glob(os.path.join(data_dir, '*.csv'))

# Функция для линейной аппроксимации
def linear_func(x, a, b):
    return a * x + b

# Проверка, что файлов достаточно для построения двух графиков
if len(csv_files) < 2:
    print("Необходимо минимум два CSV-файла для построения двух графиков.")
else:
    # Обрабатываем первые два CSV-файла для примера
    for i in range(2):  # Только два первых файла
        file_path = csv_files[i]
        file_name = os.path.splitext(os.path.basename(file_path))[0]

        # Чтение данных из CSV-файла
        data = pd.read_csv(file_path, sep=';', decimal=',')

        # Проверка названий колонок
        print(f"Обрабатываю файл: {file_name}")
        print(data.columns)

        x_label    = "f / f_0"
        xerr_label = "\sigma_{f / f_0}"
        y_label    = "U_c / U_c(1)"
        yerr_label = "\sigma_{U_c / U_c(1)}"

        # Значения x и y
        x_data = data[x_label]
        y_data = data[y_label]

        if yerr_label in data.columns:
            y_err = data[yerr_label]
        else:
            y_err = None

        if xerr_label in data.columns:
            x_err = data[xerr_label]
        else:
            x_err = None

        # Аппроксимация данных методом наименьших квадратов
        params, params_covariance = curve_fit(linear_func, x_data, y_data)

        # Построение графика с погрешностями
        plt.errorbar(	  x_data
                     	, y_data
                     	, yerr=y_err
                     	, xerr=x_err
                     	, fmt='o'
                     	, label=f'${file_name}$'
                     	, color=f'C{i}'  # Автоматически разные цвета для разных графиков
                		, ecolor='black'
						, elinewidth=1
                        , capsize=2
                        , markersize=5
						, markeredgewidth=0.5
             			, markerfacecolor='none')       # Пустой центр точки (колечко)

        # Построение линии аппроксимации
        # plt.plot(x_data, linear_func(x_data, Param[0], params[1]), label=f'Аппроксимация {file_name}', color=f'C{i}')

    # Настройка осей: график начинается с нуля
    # plt.xlim(left=0)
    # plt.ylim(bottom=0)

    # Настройка меток на осях
    plt.gca().xaxis.set_major_locator(MultipleLocator(0.01))   # Основные метки через ... единицу по оси X
    plt.gca().xaxis.set_minor_locator(AutoMinorLocator(4))  # Дополнительные метки (... на каждый интервал)

    plt.gca().yaxis.set_major_locator(MultipleLocator(0.05)) # Основные метки через ... единиц по оси Y
    plt.gca().yaxis.set_minor_locator(AutoMinorLocator(4))  # Дополнительные метки (... на каждый интервал)

    # Включаем минорные деления
    plt.minorticks_on()

    # Добавление мелкой сетки для основных и дополнительных меток
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Оформление графика
    plt.xlabel('$'+x_label+'$')
    plt.ylabel('$'+y_label+'$')
    plt.legend()

    # Сохранение графика в файл с общим названием для двух наборов данных
    output_file = f"{output_dir}/combined_graph.png"
    plt.savefig(output_file)

    # Очистка текущей фигуры для построения следующего графика
    plt.clf()

    # Выводим сообщение о сохранении графика
    print(f"Общий график для двух файлов сохранён как: {output_file}")
