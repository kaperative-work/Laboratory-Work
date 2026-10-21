word = input("Слово: ")
print("Введено:", word)
lower_pairs = 0
upper_pairs = 0
for left, right in zip(word, word[1:]):
    if left.islower() and right.islower():
        lower_pairs += 1
    elif left.isupper() and right.isupper():
        upper_pairs += 1

vowels = set("аеёиоуыэюяaeiouy")
vowel_count = sum(ch.lower() in vowels for ch in word)
print("Пар нижнего регистра:", lower_pairs)
print("Пар верхнего регистра:", upper_pairs)
print("Гласных букв:", vowel_count)
