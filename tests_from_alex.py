# 1)
# В списке [14, -1, -14, 44, -44, 24, 34, -12],
# состоящем из положительных и отрицательных чисел,
# посчитайте количество отрицательных элементов.
# Выведите результат на экран.


x = [14, -1, -14, 44, -44, 24, 34, -12]
quantity = 0
for item in x:
    if item < 0:
        quantity += 1
print('Отрицательных элементов в списке: ', quantity)

# 2)
# Напиши программу, которая заполняет список пятью словами, введенными с клавиатуры,
# измеряет длину каждого слова и добавляет полученное значение в другой список.
# Например, список слов – ['yes', 'no', 'maybe', 'ok', 'what'],
# список длин – [3, 2, 5, 2, 4]. Оба списка должны выводиться на экран.

inputs = []
lens = []
while len(inputs) < 5:
    word = input()
    inputs.append(word)
    lens.append(len(word))

print('Слова: ', sum(inputs))
print('Количество букв: ', sum(lens))


# 3)
# Напишити программу, которая выводит на экран числа от 1 до 100.
# При этом вместо чисел, кратных трем, программа должна выводить слово «Fizz»,
# а вместо чисел, кратных пяти — слово «Buzz». Если число кратно и 3, и 5,
# то программа должна выводить слово «FizzBuzz»

for i in range(1, 101):
    if i % 3 == 0 and i % 5 == 0:
        print('FizzBuzz')
    elif i % 5 == 0:
        print('Buzz')
    elif i % 3 == 0:
        print('Fizz')
    else:
        print(i)

# 4)
# Дана квадратная матрица NxN, нужно найти сумму элементов главной и побочной диагоналей.
# Допустим есть матрица:
# [
#     [y, 2, x],
#     [1, z, 3],
#     [x, 1, y]
# ]
# нам надо найти сумму следуюхи элементов
# y + y + z + x + x
main = []
secondary = []
matrix =[
    ['y', 2, 'x'],
    [1, 'z', 3],
    ['x', 1, 'y']
]
x = 0
y = -1
for row in matrix:
    main.append(row[x])
    if not len(row) // 2 == x:
        secondary.append(row[y])
    x += 1
    y += -1
result = main + secondary
print(result)