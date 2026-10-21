class Calculator:
    def read(self):
        self.a = float(input("Первое число: "))
        self.operation = input("Операция (+ - * /): ").strip()
        self.b = float(input("Второе число: "))
        print("Введено:", self.a, self.operation, self.b)

    def add(self, a, b):
        return a + b

    def sub(self, a, b):
        return a - b

    def mul(self, a, b):
        return a * b

    def div(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Деление на ноль")
        return a / b

    def compute(self):
        operations = {
            "+": self.add,
            "-": self.sub,
            "*": self.mul,
            "/": self.div,
        }
        if self.operation not in operations:
            print("Неизвестная операция")
            return None
        result = operations[self.operation](self.a, self.b)
        print("Результат:", result)
        return result

calc = Calculator()
calc.read()
calc.compute()
