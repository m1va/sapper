from random import randint


class Cell:
    def __init__(self):
        self.around_mines = 0
        self.mine = False
        self.fl_open = False


class GamePole:
    def __init__(self, N, M):
        self.N = N  # Длина и ширина поля
        self.M = M  # Кол-во мин
        self.pole = []
        self.init()

    def init(self):
        # Формирование поля N * N заполненного нулями
        self.pole = [[0 for j in range(self.N)] for i in range(self.N)]

        # Заполнение поля объектами класса Cell
        for i in range(self.N):
            for j in range(self.N):
                self.pole[i][j] = Cell()

        # Расстановка мин на поле M штук
        i = 0
        while i < self.M:
            a = randint(0, self.N - 1)
            b = randint(0, self.N - 1)
            if not self.pole[a][b].mine:
                self.pole[a][b].mine = True
                i += 1

        # self.show()

        # Подсчет количества мин вокруг каждой пустой клетки(без мин)
        self.count_mines_for_pole()

    def count_mines_for_pole(self):
        for i in range(self.N):
            for j in range(self.N):
                self.pole[i][j].around_mines = self.count_around_mines_for_cell(i, j)

    def count_around_mines_for_cell(self, _i, _j):
        count_mines = 0
        for i in range(_i - 1, _i + 2):
            if -1 < i < self.N:
                for j in range(_j - 1, _j + 2):
                    if -1 < j < self.N and (i, j) != (_i, _j):
                        if self.pole[i][j].mine:
                            count_mines += 1

        return count_mines

    # Метод для отладки
    def show_full_open_pole(self):
        for row in self.pole:
            for cell in row:
                if cell.mine:
                    print('m', end=' ')
                else:
                    print(cell.around_mines, end=' ')

            print(end='\n')

    def show(self, game_over=False):
        for row in self.pole:
            for cell in row:
                if cell.fl_open or game_over:
                    if cell.mine:
                        print('m', end=' ')
                    else:
                        print(cell.around_mines, end=' ')
                else:
                    print('#', end=' ')

            print(end='\n')

    def input_cell_pos_for_open(self):
        while True:
            i, j = self.pos_input()
            if self.check_correct_pos_input(i) and self.check_correct_pos_input(j):
                return i - 1, j - 1
            else:
                print(f"Некорректный ввод! Позиция не может быть больше размерности поля: {self.N}")

    def open_cells(self, _i, _j):
        if self.pole[_i][_j].around_mines == 0:
            for i in range(_i - 1, _i + 2):
                if -1 < i < self.N:
                    for j in range(_j - 1, _j + 2):
                        if -1 < j < self.N:
                            self.pole[i][j].fl_open = True
        else:
            self.pole[_i][_j].fl_open = True

    def check_for_win(self):
        for i in range(self.N):
            for j in range(self.N):
                if self.pole[i][j].mine is False:
                    if self.pole[i][j].fl_open is False:
                        return False

        return True

    def check_correct_pos_input(self, pos):
        return 0 < pos < self.N + 1

    def pos_input(self):
        while True:
            _input = list(input("Введите позицию поля: ").split())
            if len(_input) == 2:
                i, j = _input
                if i.isdigit() and j.isdigit():
                    return int(i), int(j)
                print("Ошибка! Вы ввели не цифры!")
            else:
                print("Некорректный ввод! Введите 2 цифры через пробел!")

    @staticmethod
    def size_input():
        while True:
            size_input = input("Введите размерность игрового поля: ")
            if size_input.isdigit():
                return int(size_input)
            print("Ошибка! Введите число!")

    @staticmethod
    def number_of_mines_input(size):
        while True:
            number_of_mines = input("Введите количество мин на поле: ")
            if number_of_mines.isdigit():
                if 0 < int(number_of_mines) < size * size + 1:
                    return int(number_of_mines)
                print(f"Ошибка! Количество мин должно быть не больше длины поля: {size * size}")
            else:
                print(f"Ошибка! Введите число!")


if __name__ == '__main__':
    size = GamePole.size_input()
    amount_mines = GamePole.number_of_mines_input(size)
    gpole = GamePole(size, amount_mines)
    #gpole.show_full_open_pole()
    while True:
        gpole.show()
        i, j = gpole.input_cell_pos_for_open()
        if gpole.pole[i][j].mine:
            gpole.show(game_over=True)
            print("БАБАХ! Вы подорвались на мине!")
            break

        gpole.open_cells(i, j)
        if gpole.check_for_win():
            gpole.show(game_over=True)
            print("Ура! Победа!")
            break
