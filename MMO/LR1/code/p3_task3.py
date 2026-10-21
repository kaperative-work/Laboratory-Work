import time


class TrafficLight:
    _order = ("красный", "жёлтый", "зелёный")
    _duration = {"красный": 7, "жёлтый": 2, "зелёный": 5}

    def __init__(self):
        self.__color = None
        self.__step = 0

    def __set_color(self, color):
        expected = self._order[self.__step % len(self._order)]
        if color != expected:
            print(f"Нарушен порядок режимов: ожидался {expected}, получен {color}. Скрипт завершён.")
            raise SystemExit(1)
        self.__color = color
        self.__step += 1

    def running(self):
        for color in self._order:
            self.__set_color(color)
            seconds = self._duration[color]
            print(f"{self.__color}: {seconds} с")
            time.sleep(seconds)
        print("Цикл красный - жёлтый - зелёный завершён")


light = TrafficLight()
light.running()

print("--- проверка нарушения порядка ---")
broken = TrafficLight()
try:
    broken._TrafficLight__set_color("зелёный")
except SystemExit:
    print("Работа светофора остановлена из-за неверного порядка")
