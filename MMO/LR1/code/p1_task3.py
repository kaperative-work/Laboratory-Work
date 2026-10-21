raw = input("Элементы списка через пробел: ")
print("Введено:", raw)
items = []
for part in raw.split():
    items.append(int(part) if part.lstrip("-").isdigit() else float(part))

even_items = items[0::2]
product = 1
for value in even_items:
    product *= value
if not even_items:
    product = 0

print("Элементы с чётными номерами:", even_items)
print("Их произведение:", product)
print("Длина списка:", len(items))
