import os

import cv2
from PIL import Image, ImageDraw

import math
import matplotlib.pyplot as plt
import numpy as np
from numpy import histogram, std
import scipy.stats as stats


# Функция поиска границ на изображении
def treatment(filename, min_binary, max_binary, min_contour_area, max_contour_area):
    basedir = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(basedir, r'uploads\\')
    print(UPLOAD_FOLDER)

    # загрузка изображения, изменения его размера и обрезка нижней части (библиотека Pillow)
    image_original = Image.open(UPLOAD_FOLDER + filename)
    image_resize = image_original.resize((1600, 1200))
    image_resize.save(UPLOAD_FOLDER + r'workdir/rs_' + filename, 'JPEG')
    area = (0, 0, 1600, 1115)
    image_cut = image_resize.crop(area)
    image_cut.save(UPLOAD_FOLDER + r'workdir/crop_'+ filename, 'JPEG')

    # Подготовка изображения к поиску контуров (библиотека OpenCV-Python)
    # Операции: размытие - бинаризация - контуры Сanny
    image_test = cv2.imread(UPLOAD_FOLDER + r'workdir/crop_' + filename, cv2.CV_8UC1)
    image_test_blurred = cv2.blur(image_test, (5, 5), 0)
    (_, image_test_binary) = cv2.threshold(image_test_blurred, min_binary, max_binary,
                            cv2.THRESH_BINARY)
    cv2.imwrite(UPLOAD_FOLDER + r'workdir/binar_' + filename, image_test_binary)
    image_test_canny = cv2.Canny(image_test_binary, 100, 300)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    image_test_canny_closed = cv2.morphologyEx(image_test_canny, cv2.MORPH_CLOSE, kernel)
    cv2.imwrite(UPLOAD_FOLDER + r'workdir/canny_' + filename, image_test_canny_closed)

    # Поиск и нанесение контуров на исходное изображение
    # Операции: findContours - contourArea - drawContours
    contours, hierarchy = cv2.findContours(image_test_canny_closed.copy(),
                            cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    image_phasecather = cv2.imread(UPLOAD_FOLDER + r'workdir/rs_' + filename, cv2.CV_32FC1)
    for contour in contours:
        if ((cv2.contourArea(contour) > min_contour_area) and
            (cv2.contourArea(contour) < max_contour_area)):
            cv2.drawContours(image_phasecather, [contour], -1, (250, 0, 0), -1)
    cv2.imwrite(UPLOAD_FOLDER + r'workdir/final_' + filename, image_phasecather)

    # Сортировка контуров по размеру
    contour_in_nano = []
    for contour in contours:
        if 1500 <= cv2.contourArea(contour):
            a = cv2.contourArea(contour)
            contour_in_nano.append(a)

    # Переводим размеры из пикселей в нанометры
    scale = 4
    for i in range(len(contour_in_nano)):
        contour_in_nano[i] = int((math.sqrt((contour_in_nano[i] * 4) / (math.pi))) * scale)

    # Математические вычисления
    if len(contour_in_nano) > 0:
        medium_phase_size = (sum(contour_in_nano))/(len(contour_in_nano))
    else:
        medium_phase_size = (sum(contour_in_nano))
    # print('Средний диаметр - ', '%.2f' % medium_phase_size, 'нм, ', 'количество исследованных частиц - ', len(contour_in_nano))

    # Построение гистограммы распределения размера частиц
    sorted_contour_in_nano = sorted(contour_in_nano)
    mu = medium_phase_size
    sigma = std(contour_in_nano)
    gaus = stats.norm.pdf(sorted_contour_in_nano, mu, sigma)
    plt.plot(sorted_contour_in_nano, gaus, '-o')
    plt.hist(contour_in_nano, bins=20, normed=True, facecolor='red', edgecolor='black')
    try:
        os.remove(UPLOAD_FOLDER + r'/workdir/graph_' + filename)
        print('файл создан')
        plt.savefig(UPLOAD_FOLDER + r'/workdir/graph_' + filename)
    except FileNotFoundError:
        print('Файла нет')
    plt.savefig(UPLOAD_FOLDER + r'/workdir/graph_' + filename)
    return {'final_image': r'/workdir/final_'+filename,
            'graph_image': r'/workdir/graph_'+save_file+'.png',
            'medium_phase_size': medium_phase_size,
            'sigma': sigma, 'particle_count': len(contour_in_nano)}

if __name__ == '__main__':
    treatment()
