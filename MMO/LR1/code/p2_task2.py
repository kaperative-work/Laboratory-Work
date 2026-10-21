def process(value):
    if isinstance(value, list):
        if not value or any(x <= 0 for x in value):
            raise ValueError("Для среднего геометрического нужны положительные числа")
        product = 1
        for number in value:
            product *= number
        return product ** (1 / len(value))
    if isinstance(value, dict):
        return dict(sorted(value.items(), key=lambda item: item[1], reverse=True))
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        number = int(value)
        if number < 2 or number != value:
            return False
        divisor = 2
        while divisor * divisor <= number:
            if number % divisor == 0:
                return False
            divisor += 1
        return True
    if isinstance(value, str):
        words = value.split()
        if not words:
            return 0, ""
        longest = max(words, key=len)
        return len(words), longest
    raise TypeError("Ожидался список, словарь, число или строка")

numbers = [1, 3, 9, 27]
print("Список", numbers, "-> среднее геометрическое", process(numbers))

prices = {"кольцо": 1500, "серьги": 80, "цепочка": 400}
print("Словарь", prices, "->", process(prices))

for number in (1, 2, 7, 9, 15):
    print(f"Число {number}: простое = {process(number)}")

text = "выбор обрыв самое длинное"
count, longest = process(text)
print("Строка:", text)
print("Слов:", count)
print("Самое длинное слово:", longest)
