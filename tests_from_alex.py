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
    print('Введите слово: ')
    word = input()
    inputs.append(word)
    lens.append(len(word))


print('Слова: ', inputs)
print('Количество букв: ', lens)


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
print('Введите х: ')
x = int(input())
print('Введите y: ')
y = int(input())
print('Введите z: ')
z = int(input())
matrix =[
    [y, 2, x],
    [1, z, 3],
    [x, 1, y]
]
x = 0
y = -1
for row in matrix:
    print(row)
    main.append(row[x])
    if not len(row) // 2 == x:
        secondary.append(row[y])
    x += 1
    y += -1
result = main + secondary
print(sum(result))

y = int(input())
x = [0, 1, 3, 4, 6, 7, 8, 11, 13, 14, 16, 17, 18, 19]
def binary_search(y, x):
        middle = len(x) // 2
        if len(x) > 1:
            if x[middle-1] > y:
                print('меньше')
                x = x[:middle-1]
                print(x)
                middle = len(x) // 2
                if x[middle-1] == y:
                    return middle
                else:
                    binary_search(y, x)
            elif x[middle-1] < y:
                print('больше')
                x = x[(middle-1):]
                print(x)
                middle = len(x) // 2
                if x[middle-1] == y:
                    return middle
                else:
                    binary_search(y, x)
        else:
            return middle
print(binary_search(y, x))

