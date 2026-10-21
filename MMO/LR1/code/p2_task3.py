n = int(input("Число строк n: "))
m = int(input("Число столбцов m: "))
print("Введено: n =", n, ", m =", m)

board = []
for i in range(n):
    row = []
    for j in range(m):
        if i == 0 and j == 0:
            row.append(".")
        elif (i + j) % 2 == 0:
            row.append("%")
        else:
            row.append("&")
    board.append(row)

for row in board:
    print(*row)
