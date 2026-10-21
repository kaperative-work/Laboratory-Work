first_raw = input("Первое множество, числа через пробел: ")
second_raw = input("Второе множество, числа через пробел: ")
print("Введено:", first_raw, "|", second_raw)
first = set(int(x) for x in first_raw.split())
second = set(int(x) for x in second_raw.split())
common = first & second
if common:
    print("Элементы первого множества, которые есть во втором:", *sorted(common))
else:
    print("Общих элементов нет")
