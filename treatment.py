from PIL import Image, ImageDraw
import cv2
import numpy as np
import os

''' В функцию передается загруженный файл'''
image_original = Image.open('698 фаза.jpg') 
'''Меняем разрешение исходного изображения'''
image_resize = image_original.resize((1600, 1200)) 

''' обрезаем нижнюю часть изображения'''
area = (0, 0, 1600, 1115)
image_cut = image_resize.crop(area)
image_cut.save('698_crop_test.jpg', 'JPEG')

'''переходим к библиотеке OpenCV, говорим программе, что изображение ч/б и одноканальное'''
'''не работает открытие файла, постараюсь в ближайшие дни переделать'''
image_test = cv2.imread(os.path.join(‎⁨grad_project⁩, '698_crop_test.jpg'), cv2.CV_8UC1) )

''' добавляем размытие к изображению, чтобы убрать шумы'''
image_test_blurred = cv2.blur(image_test, (5,5), 0) 

''' Эти значения должны быть крайними на бегунке бинаризации'''
min_binary = 0 
max_binary =255
''' магия бинаризации'''
(_, image_test_binary) = cv2.threshold(image_test_blurred, min_binary, max_binary, cv2.THRESH_BINARY) 

'''тут на бинаризованном изображении определяются графические контуры'''
image_test_canny = cv2.Canny(image_test_binary, 100, 300)  
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
image_test_canny_closed = cv2.morphologyEx(image_test_canny, cv2.MORPH_CLOSE, kernel)

'''магия поиска контуров и определение их взаимосвязи и иерархии'''
contours, hierarchy = cv2.findContours(image_test_canny_closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 

''' Минимальное и максимальное (след.строка) значение площади частицы, ,будут на бегунке'''
min_contour_area = 0 
max_contour_area = 10000


''' Закрашиваем контуры'''
image_phasecather = cv2.imread(image_resize, cv2.CV_32FC1)
for contour in contours:
    if (cv2.contourArea(contour) > min_contour_area) and (cv2.contourArea(contour) < max_contour_area):
        cv2.drawContours(image_original, [contour], -1, (250,0,0), -1) 
cv2.imwrite('file_name.jpg', image_original) 
''' сохраняем изображение с закрашенными контурами'''



        