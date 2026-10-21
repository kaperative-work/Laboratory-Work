number = int(input("Натуральное число: "))
print("Введено:", number)
digits = [int(ch) for ch in str(number)]
has_even = any(d % 2 == 0 for d in digits)
odd_sum = sum(d for d in digits if d % 2 == 1)
if not has_even:
    result = 0
    print("Чётных цифр нет, поэтому результат: 0")
else:
    result = odd_sum
    print("Сумма нечётных цифр:", result)
