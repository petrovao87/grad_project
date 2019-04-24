# # 1)
# # В списке [14, -1, -14, 44, -44, 24, 34, -12],
# # состоящем из положительных и отрицательных чисел,
# # посчитайте количество отрицательных элементов.
# # Выведите результат на экран.
#
#
# x = [14, -1, -14, 44, -44, 24, 34, -12]
# quantity = 0
# for item in x:
#     if item < 0:
#         quantity += 1
# print('Отрицательных элементов в списке: ', quantity)
#
# # 2)
# # Напиши программу, которая заполняет список пятью словами, введенными с клавиатуры,
# # измеряет длину каждого слова и добавляет полученное значение в другой список.
# # Например, список слов – ['yes', 'no', 'maybe', 'ok', 'what'],
# # список длин – [3, 2, 5, 2, 4]. Оба списка должны выводиться на экран.
#
# inputs = []
# lens = []
# while len(inputs) < 5:
#     print('Введите слово: ')
#     word = input()
#     inputs.append(word)
#     lens.append(len(word))
#
#
# print('Слова: ', inputs)
# print('Количество букв: ', lens)
#
#
# # 3)
# # Напишити программу, которая выводит на экран числа от 1 до 100.
# # При этом вместо чисел, кратных трем, программа должна выводить слово «Fizz»,
# # а вместо чисел, кратных пяти — слово «Buzz». Если число кратно и 3, и 5,
# # то программа должна выводить слово «FizzBuzz»
#
# for i in range(1, 101):
#     if i % 3 == 0 and i % 5 == 0:
#         print('FizzBuzz')
#     elif i % 5 == 0:
#         print('Buzz')
#     elif i % 3 == 0:
#         print('Fizz')
#     else:
#         print(i)
#
# # 4)
# # Дана квадратная матрица NxN, нужно найти сумму элементов главной и побочной диагоналей.
# # Допустим есть матрица:
# # [
# #     [y, 2, x],
# #     [1, z, 3],
# #     [x, 1, y]
# # ]
# # нам надо найти сумму следуюхи элементов
# # y + y + z + x + x
# main = []
# secondary = []
# print('Введите х: ')
# x = int(input())
# print('Введите y: ')
# y = int(input())
# print('Введите z: ')
# z = int(input())
# matrix =[
#     [y, 2, x],
#     [1, z, 3],
#     [x, 1, y]
# ]
# x = 0
# y = -1
# for row in matrix:
#     print(row)
#     main.append(row[x])
#     if not len(row) // 2 == x:
#         secondary.append(row[y])
#     x += 1
#     y += -1
# result = main + secondary
# print(sum(result))

y = int(input())
x = [0, 1, 3, 4, 6, 7, 8, 11, 13, 14, 16, 17, 18, 19]


def binary_search(y, x):
        min = 0
        max = len(x) - 1
        while min <= max:
            middle = (min + max) // 2
            if x[middle+1] == y:
                return middle
            if x[middle] > y:
                x = x[:middle]
                binary_search(y, x)
            else:
                x = x[middle+1:]
                binary_search(y, x)
        return 'нет такого'


print(binary_search(y, x))

# def binary_search(x, y):
#     low = 0
#     high = len(x) - 1
#     while low <= high:
#         mid = (low + high) // 2
#         guess = x[mid]
#         if guess == y:
#             return mid
#         if guess > y:
#             high = mid - 1
#         else:
#             low = mid + 1
#     return None
#
#
# print(binary_search(x, y))