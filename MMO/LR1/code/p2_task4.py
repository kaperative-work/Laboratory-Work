def divide(a, b):
    try:
        result = a / b
        print("Частное:", result)
        return result
    except ZeroDivisionError:
        print("Ошибка: деление на ноль")
    except TypeError:
        print("Ошибка: нужны числа")
    finally:
        print("Блок finally выполнен")

divide(10, 2)
print("---")
divide(10, 0)
print("---")
divide("10", 2)

print("---")
try:
    raw = input("Целое число для преобразования: ")
    print("Введено:", raw)
    value = int(raw)
    print("Преобразовано:", value)
except ValueError:
    print("Ошибка: это не целое число")
finally:
    print("Ввод завершён, блок finally выполнен")
