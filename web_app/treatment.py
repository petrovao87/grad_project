from PIL import Image, ImageDraw
import cv2
import numpy as np
import os
import math
import matplotlib.pyplot as plt
import scipy.stats as stats
from numpy import histogram, std


def treatment(filename, min_binary, max_binary, min_contour_area, max_contour_area):
    basedir = os.path.abspath(os.path.dirname(__file__))
    UPLOAD_FOLDER = os.path.join(basedir, r'uploads/')
    print(UPLOAD_FOLDER)

    print(''' В функцию передается загруженный файл''')
    image_original = Image.open(UPLOAD_FOLDER + filename)
    print('''Меняем разрешение исходного изображения''')
    image_resize = image_original.resize((1600, 1200))

    print(''' обрезаем нижнюю часть изображения''')
    area = (0, 0, 1600, 1115)
    image_cut = image_resize.crop(area)
    image_cut.save(UPLOAD_FOLDER + r'workdir/crop_'+ filename, 'JPEG')

    print('''переходим к библиотеке OpenCV, говорим программе, что изображение ч/б и одноканальное''')
    '''не работает открытие файла, постараюсь в ближайшие дни переделать'''
    image_test = cv2.imread(UPLOAD_FOLDER + r'workdir/crop_' + filename, cv2.CV_8UC1)

    print(''' добавляем размытие к изображению, чтобы убрать шумы''')
    image_test_blurred = cv2.blur(image_test, (5, 5), 0)

    print(''' Эти значения должны быть крайними на бегунке бинаризации''')
    #min_binary = 60
    #max_binary = 255
    print(''' магия бинаризации''')
    (_, image_test_binary) = cv2.threshold(image_test_blurred, min_binary, max_binary, cv2.THRESH_BINARY)
    cv2.imwrite(UPLOAD_FOLDER + r'workdir/binar_' + filename, image_test_binary)

    print('''тут на бинаризованном изображении определяются графические контуры''')
    image_test_canny = cv2.Canny(image_test_binary, 100, 300)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    image_test_canny_closed = cv2.morphologyEx(image_test_canny, cv2.MORPH_CLOSE, kernel)
    cv2.imwrite(UPLOAD_FOLDER + r'workdir/canny_' + filename, image_test_canny_closed)

    print('''магия поиска контуров и определение их взаимосвязи и иерархии''')
    contours, hierarchy = cv2.findContours(image_test_canny_closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    print(''' Минимальное и максимальное (след.строка) значение площади частицы, ,будут на бегунке''')
    #min_contour_area = 0
    #max_contour_area = 10000

    print(''' Закрашиваем контуры''')
    image_phasecather = cv2.imread(UPLOAD_FOLDER + r'workdir/crop_' + filename, cv2.CV_32FC1)
    for contour in contours:
        #print(contour)
        #if cv2.contourArea(contour) > 1500:
        if (cv2.contourArea(contour) > min_contour_area) and (cv2.contourArea(contour) < max_contour_area):
            cv2.drawContours(image_phasecather, [contour], -1, (250, 0, 0), -1)
    print(''' сохраняем изображение с закрашенными контурами''')
    cv2.imwrite(UPLOAD_FOLDER + r'workdir/final_' + filename, image_phasecather)

    '''отсортируем "лишние" мелкие контуры по площади, остальные перепишем в новый список'''
    contour_in_nano = []
    for contour in contours:

        if 1500 <= cv2.contourArea(contour):
            a = cv2.contourArea(contour)
            contour_in_nano.append(a)
    print(contour_in_nano)

    '''Переведем пиксели в нанометры (1:4), а таже из площади получим диаметр каждой частички 
    (пока по формуле для круга)'''
    scale = 4
    for i in range(len(contour_in_nano)):
        contour_in_nano[i] = int((math.sqrt((contour_in_nano[i] * 4) / (math.pi))) * scale)

    '''Найдем средний размер (диаметр) частички'''
    if len(contour_in_nano) > 0:
        medium_phase_size = (sum(contour_in_nano))/(len(contour_in_nano))
    else:
        medium_phase_size = (sum(contour_in_nano))
    print('Средний диаметр - ', '%.2f' % medium_phase_size, 'нм, ', 'количество исследованных частиц - ',
            len(contour_in_nano))

    '''Теперь графически покажем распределение частиц по размеру. Построим график равномерного распределения и 
    совместив с графиком нормального (гаусова) распределения'''
    sorted_contour_in_nano = sorted(contour_in_nano)
    mu = medium_phase_size
    sigma = std(contour_in_nano)
    gaus = stats.norm.pdf(sorted_contour_in_nano, mu, sigma)
    plt.plot(sorted_contour_in_nano, gaus, '-o')
    plt.hist(contour_in_nano, bins=20, normed=True, facecolor='red', edgecolor='black')
    # save_file = filename.split('.')[0]
    # try:
    #     os.remove(UPLOAD_FOLDER + r'\workdir\graph_' + save_file + '.png')
    #     print('файл создан')
    #     plt.savefig(UPLOAD_FOLDER + r'\workdir\graph_' + save_file + '.png')
    # except FileNotFoundError:
    #     print('Файла нет')
    # plt.savefig(UPLOAD_FOLDER + r'\workdir\graph_' + save_file + '.png')

    try:
        os.remove(UPLOAD_FOLDER + r'/workdir/graph_' + filename)
        print('файл создан')
        plt.savefig(UPLOAD_FOLDER + r'/workdir/graph_' + filename)
    except FileNotFoundError:
        print('Файла нет')
    plt.savefig(UPLOAD_FOLDER + r'/workdir/graph_' + filename)

    # plt.show()

    return {'final_image': r'/workdir/final_'+filename, 'graph_image': r'/workdir/graph_'+filename,
           'medium_phase_size': medium_phase_size, 'sigma': sigma, 'particle_count': len(contour_in_nano)}

if __name__ == '__main__':
    treatment('test.jpg', 55, 255)
