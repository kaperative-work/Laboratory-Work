first = input("Первое слово: ").strip()
second = input("Второе слово: ").strip()
print("Введено:", first, "и", second)

def letters(word):
    return sorted(ch for ch in word.lower() if ch.isalpha())

if letters(first) == letters(second):
    print("Слова являются анаграммами")
else:
    print("Слова не являются анаграммами")
