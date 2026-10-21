def is_password_good(password):
    long_enough = len(password) >= 8
    has_upper = any(ch.isupper() for ch in password)
    has_digit = any(ch.isdigit() for ch in password)
    return long_enough and has_upper and has_digit

examples = ["abc", "abcdefgh", "Abcdefgh", "Abcdefg1", "qwerty12"]
for password in examples:
    print(password, "->", is_password_good(password))

password = input("Введите пароль: ")
print("Введено:", password)
print(is_password_good(password))
