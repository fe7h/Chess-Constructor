from constructor.figures import Figure


# ОБЕЗЛИЧИТЬ КЛАСС И СДЕЛАТЬ ЕГО БОЛЕЕ ВАРИАТИВНЫМ
class AttackedSquares:
    """структура которая хранит цвет:клетки которые несут опасность для этого цвета"""
    def __init__(self, colors):
        self.__under_attack = {color: set() for color in colors}

    def update(self, figure: Figure):
        figure_color = figure.color
        for color in self.__under_attack:
            if color != figure_color:
                self.__under_attack[color].update(figure.valid_moves.get())

    def clear(self):
        for color in self.__under_attack:
            self.__under_attack[color].clear()

    def get_attacked_squares(self, color: str | Figure):
        if isinstance(color, Figure):
            color = color.color
        return self.__under_attack.get(color)

    def under_attack(self):
        pass
#     добавить метод для in


# вынести в отдельный файл и довести до ума
class PriorityList:
    """Класс который сохраняет обекты в порядке их заданного прироитета
    можно использовать как декоратор для функций указав их приоритет
    """
    def __init__(self):
        self.__data = dict()

    def set(self, priority, obj):
        self.__data[priority] = obj
        self._sort()

    def _sort(self):
        self.__data = {key: self.__data[key] for key in sorted(self.__data)}

    def __iter__(self):
        return iter(tuple(val for val in self.__data.values()))

    def __call__(self, priority):
        def wrapper(func):
            self.set(priority, func)
            return func
        return wrapper