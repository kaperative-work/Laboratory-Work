shop = {
    "Кольцо": ["золото, бриллиант", 1500, 4],
    "Серьги": ["серебро", 80, 10],
    "Цепочка": ["золото", 400, 6],
    "Браслет": ["серебро, фианит", 220, 5],
}

total_price = 0
running = True
while running:
    print("\nЮвелирный магазин")
    print("1. Просмотр описания")
    print("2. Просмотр цены")
    print("3. Просмотр количества")
    print("4. Вся информация")
    print("5. Покупка")
    print("6. До свидания")
    choice = input("Выберите пункт меню: ").strip()
    print("Выбрано:", choice)

    if choice == "1":
        for name, info in shop.items():
            print(f"{name} – {info[0]}")
    elif choice == "2":
        for name, info in shop.items():
            print(f"{name} – {info[1]}")
    elif choice == "3":
        for name, info in shop.items():
            print(f"{name} – {info[2]}")
    elif choice == "4":
        for name, (composition, price, qty) in shop.items():
            print(f"{name}: состав — {composition}, цена — {price}, количество — {qty}")
    elif choice == "5":
        while True:
            name = input("Название изделия (n — выход): ").strip()
            print("Введено название:", name)
            if name.lower() == "n":
                running = False
                break
            if name not in shop:
                print("Такого изделия нет")
                continue
            qty_text = input("Количество: ").strip()
            print("Введено количество:", qty_text)
            if not qty_text.isdigit() or int(qty_text) <= 0:
                print("Количество должно быть натуральным числом")
                continue
            qty = int(qty_text)
            if qty > shop[name][2]:
                print("Недостаточно товара, в наличии:", shop[name][2])
                continue
            shop[name][2] -= qty
            total_price += shop[name][1] * qty
            print("Добавлено в покупку")
        print("Цена выбранных товаров:", total_price)
        print("Осталось в магазине:")
        for name, info in shop.items():
            print(f"{name} – {info[2]}")
    elif choice == "6":
        print("До свидания")
        running = False
    else:
        print("Нет такого пункта")
