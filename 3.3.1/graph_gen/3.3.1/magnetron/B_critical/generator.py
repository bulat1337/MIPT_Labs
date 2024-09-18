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

# Обрабатываем каждый CSV-файл
for file_path in csv_files:
    # Извлекаем имя файла без расширения
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    # Чтение данных из CSV-файла
    data = pd.read_csv(file_path, sep=';', decimal=',')

    # Проверка названий колонок
    print(f"Обрабатываю файл: {file_name}")
    print(data.columns)

    y_label    = "B_{кр}^2, мТл"
    yerr_label = "\sigma_{B_кр^2}, мТл"
    x_label    = "U_a, В"
    xerr_label = "\sigma_{U_a}, В"

    # Значения x и y
    x_data = data[x_label]  # теперь U_a на оси X
    y_data = data[y_label]  # теперь B_{кр}^2 на оси Y

    if yerr_label in data.columns:
        print("found y errors")
        y_err = data[yerr_label]
        for elem in y_err:
            print(y_err)
    else:
        y_err = 666

    if xerr_label in data.columns:
        print("found x errors:")
        x_err = data[xerr_label]
        for elem in x_err:
            print(x_err)
    else:
        x_err = 666

    # Аппроксимация данных методом наименьших квадратов
    params, params_covariance = curve_fit(linear_func, x_data, y_data)

    # Построение графика с погрешностями
    plt.errorbar(	x_data
                 	, y_data
                    , yerr=y_err
                    , xerr=x_err
                    , fmt=''
                    , label='Данные'
                    , color='red'
                    , ecolor='black'
                    , elinewidth=1
                    , capsize=1
                    , markersize=5
                    , markeredgewidth=1
                    , linestyle='none')

    # Построение линии аппроксимации
    plt.plot(x_data, linear_func(x_data, params[0], params[1]), label='Аппроксимация', color='blue')

    # Настройка осей: график начинается с нуля
    # plt.xlim(left=0)
    # plt.ylim(bottom=0)

    # Настройка меток на осях
    plt.gca().xaxis.set_major_locator(MultipleLocator(5))   # Основные метки через 1 единицу по оси X
    plt.gca().xaxis.set_minor_locator(AutoMinorLocator(4))  # Дополнительные метки (4 на каждый интервал)

    plt.gca().yaxis.set_major_locator(MultipleLocator(0.5))
    plt.gca().yaxis.set_minor_locator(AutoMinorLocator(4))  # Дополнительные метки (4 на каждый интервал)

    # Включаем минорные деления
    plt.minorticks_on()

    # Добавление мелкой сетки для основных и дополнительных меток
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Оформление графика
    plt.xlabel('$'+x_label+'$')
    plt.ylabel('$'+y_label+'$')
    # plt.legend()

    # Сохранение графика в файл с таким же названием, как у CSV-файла
    output_file = f"{output_dir}/{file_name}.png"
    plt.savefig(output_file)

    # Очистка текущей фигуры для построения следующего графика
    plt.clf()

    # Выводим сообщение о сохранении графика
    print(f"График для {file_name} сохранён как: {output_file}")
