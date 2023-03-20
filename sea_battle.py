import random
import time

# Я написал эту программу, не смотря в какие-либо подскази
# Я ориентировался только на задание, а так же на алгоритм, указанный в задании
#
# Для удобства, я изменил название клеток на более привычные:
#   по вертикали - латинская строчная буква, по горизонтали - цифра. Напимер b3, d5 и т.д.


abc = 'abcdef'   # просто константа с буквами по вертикали


# класс точки - в соответствии с заданием
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if other == None:
            return False
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'Dot: {self.x, self.y}'


# класс корабля - в соответствии с заданием
class Ship:
    lifes = None

    def __init__(self, x, y, h, d):
        self.x = x
        self.y = y
        self.h = h # горизонтальный: True/False
        self.d = d # количество палуб
        self.lifes = d

    def dots(self):
        result = list()
        x_, y_ = self.x, self.y
        for i in range(self.d):
            dot_ = Dot(x_, y_)
            result.append(dot_)
            if self.h:
                x_ += 1
            else:
                y_ += 1
        return result


# класс игрового поля - в соответствии с заданием
class Board:
    def __init__(self, hid):
        self.hid = hid
        self.clear()

    def clear(self):
        self.fields = [
            ['◯', '◯', '◯', '◯', '◯', '◯'],
            ['◯', '◯', '◯', '◯', '◯', '◯'],
            ['◯', '◯', '◯', '◯', '◯', '◯'],
            ['◯', '◯', '◯', '◯', '◯', '◯'],
            ['◯', '◯', '◯', '◯', '◯', '◯'],
            ['◯', '◯', '◯', '◯', '◯', '◯']]
        self.ships = []

    def add_ship(self, ship):   # возвращает True, если корабль успешно дабавлен на поле, и False если ошибка
        x = ship.x
        y = ship.y
        # проверяем возможность добавления корабля
        for i in range(ship.d):
            if self.fields[y-1][x-1] != '◯':
                return False
            if ship.h:
                x += 1
            else:
                y += 1
        # добавляем корабль
        self.ships.append(ship)
        # рисуем корабль на матрице
        dots = ship.dots()
        for i in range(len(dots)):
            self.fields[dots[i].y-1][dots[i].x-1] = '■'
        return True

    def out(self, dot):
        if (dot.x < 1) or (dot.x > 6) or (dot.y < 1) or (dot.y > 6):
            return True
        return False

    def contour(self, ship):
        x = ship.x
        y = ship.y
        # добавляем в список все возможные точки
        p = []
        p.append([x-1, y-1])
        p.append([x, y-1])
        p.append([x-1, y])
        for i in range(ship.d):
            p.append([x-1, y+1])
            p.append([x+1, y-1])
            if i == ship.d-1:
                break
            if ship.h:
                x += 1
            else:
                y += 1
        p.append([x, y+1])
        p.append([x+1, y+1])
        p.append([x+1, y])
        # теперь переносим в игровое поле только те точки, которые не выходят за пределы поля
        for i in range(len(p)):
            dot = Dot(p[i][0], p[i][1])
            if not self.out(dot):
                self.fields[dot.y - 1][dot.x - 1] = '.'

    def get_free_dots(self):
        result = []
        for y in range(6):
            for x in range(6):
                if self.fields[y][x] == '◯':
                    dot = Dot(x+1, y+1)
                    result.append(dot)
        return result

    # функция random_boyard рандомно расставляет корабли
    # возвращает True, если удалось расставать корабли, и False - если не удалось
    def random_boyard(self):
        d_list = [3, 2, 2, 1, 1, 1, 1]  # какие корабли нужно создать
        counter = 0
        for i in range(len(d_list)):
            d = d_list[i]
            while True:
                if random.choice([True, False]):
                    ship = Ship(random.randint(1, 6 - d + 1), random.randint(1, 6), True, d)  # горизонтальный
                else:
                    ship = Ship(random.randint(1, 6), random.randint(1, 6 - d), False, d)  # вертикальный
                if self.add_ship(ship):
                    self.contour(ship)
                    break
                # если вдруг закончились поля
                free_dots = self.get_free_dots()
                if len(free_dots) == 0:
                    return False
                # если корабль однопалубный, пробуем поставить его по упрощённой схеме, чтобы не гонять циклы
                if d == 1:
                    step = random.randint(0, len(free_dots) - 1)
                    ship = Ship(free_dots[step].x, free_dots[step].y, True, 1)
                    if self.add_ship(ship):
                        self.contour(ship)
                        break
                    else:
                        return False

                counter += 1
                if counter > 30:  # на случай непредвиденной ошибки
                    return False
        # теперь оставшиеся клетки "" пометим точками, чтобы они не отличались
        free_dots = self.get_free_dots()
        for i in range(len(free_dots)):
            self.fields[free_dots[i].y - 1][free_dots[i].x - 1] = '.'
        return True

    def get_alive_count(self):
        a = 0
        for ship in self.ships:
            if ship.lifes > 0:
                a += 1
        return a

    def shot(self, dot):
        for ship in self.ships:
            if dot in ship.dots():
                ship.lifes -= 1
                if ship.lifes == 0:
                    self.fields[dot.y-1][dot.x-1] = 'X'
                    return ship
                else:
                    self.fields[dot.y - 1][dot.x - 1] = 'X'
                    return ship
        return None


# класс Player - в соответствии с заданием
class Player:
    def __init__(self):
        self.tagert = []  # если корабль ранен, то ПК будет добивать
        self.my_board = Board(False)
        while True:
            try:
                result = self.my_board.random_boyard()  # пробую расставить корабли
            except ValueError as e:
                result = False
            if result == True:
                break
            # Не удалось расставить корабли --> пробую ещё раз (по циклу)
            self.my_board.clear()


        self.opp_board = Board(True)

    def ask(self):  # в соотвестстии, оставляю данную функцию для наследников
        ...

    def move(self, opp_board1):
        dot = self.ask()
        if dot == None:
            return -1  # ошибка
        print(f'Выполняю ход {abc[dot.y-1]}{dot.x}...')
        if self.opp_board.fields[dot.y-1][dot.x-1] != '◯':
            return -1  # ошибка

        ship = opp_board1.shot(dot)
        if ship == None:
            self.opp_board.fields[dot.y - 1][dot.x - 1] = 'T'    # мимо
            return 0  # мимо
        else:
            self.opp_board.fields[dot.y - 1][dot.x - 1] = 'X'    # есть попадание!
            if ship.lifes == 0:
                self.opp_board.contour(ship)
                self.tagert = []  # очищаем список ранений
                return 2  # убит
            else:
                self.tagert.append(dot)
                return 1 # ранен


# класс User - в соответствии с заданием
class User(Player):
    def ask(self):
        s = input('Ваш ход:')
        if (len(s) != 2) or (abc.find(s[0]) == -1) or (int(s[1]) < 1) or (int(s[1]) > 6):
            print('Ошибка: ход указывается в формате английская строчная буква + цифра (например "b4").')
            return None
        dot = Dot(int(s[1]), abc.find(s[0]) + 1)
        if self.opp_board.fields[dot.y - 1][dot.x - 1] != '◯':
            print('Ошибка: в это поле ходить нельзя.')
            return None
        return dot

# класс AI -  в соответствии с заданием
class AI(Player):
    def ask(self):
        steps = []
        # если имеется раненый корабль с одним ранением
        if len(self.tagert) == 1:
            x = self.tagert[0].x
            y = self.tagert[0].y
            # пробуем слева
            if (x != 1) and (self.opp_board.fields[y-1][x-2] == '◯'):
                dot = Dot(x-1, y)
                return dot
            # пробуем справа
            if (x != 6) and (self.opp_board.fields[y-1][x] == '◯'):
                dot = Dot(x+1, y)
                return dot
            # пробуем сверху
            if (y != 1) and (self.opp_board.fields[y-2][x-1] == '◯'):
                dot = Dot(x, y-1)
                return dot
            # пробуем снизу
            if (y != 6) and (self.opp_board.fields[y][x-1] == '◯'):
                dot = Dot(x, y+1)
                return dot
        # если имеется раненый корабль с двумя ранениями
        if len(self.tagert) == 2:
            x1, x2 = self.tagert[0].x, self.tagert[1].x
            y1, y2 = self.tagert[0].y, self.tagert[1].y
            if y1 == y2:
                # пробуем слева
                x = min(x1, x2)
                if (x != 1) and (self.opp_board.fields[y1 - 1][x - 2] == '◯'):
                    dot = Dot(x - 1, y1)
                    return dot
                # пробуем справа
                x = max(x1, x2)
                if (x != 6) and (self.opp_board.fields[y1 - 1][x] == '◯'):
                    dot = Dot(x + 1, y1)
                    return dot
            if x1 == x2:
                # пробуем сверху
                y = min(y1, y2)
                if (y != 1) and (self.opp_board.fields[y - 2][x1 - 1] == '◯'):
                    dot = Dot(x1, y-1)
                    return dot
                # пробуем снизу
                y = max(y1, y2)
                if (y != 6) and (self.opp_board.fields[y][x1 - 1] == '◯'):
                    dot = Dot(x1, y+1)
                    return dot

        # если нет раненых кораблей
        free_dots = self.opp_board.get_free_dots()
        step = random.randint(0, len(free_dots) - 1)
        dot = free_dots[step]
        return dot


# класс Game -  в соответствии с заданием
class Game:
    user = None
    ai = None

    def __init__(self):
        self.user = User()
        self.ai =AI()

    def draw(self):
        print('Корабли противника:    Ваши корабли:')
        print('  1 2 3 4 5 6            1 2 3 4 5 6')
        for y in range(6):
            # игровое поле игрока
            print(abc[y], end = ' ')
            for x in range(6):
                print(self.user.opp_board.fields[y][x] + ' ', end = '')
            print('        ', abc[y], end = ' ')
            for x in range(6):
                print(self.user.my_board.fields[y][x] + ' ', end='')
            print()


    def loop(self):
        msg = ''
        while True:
            # ход игрока
            while True:
                self.draw()
                if msg != '':
                    print(msg)
                try:
                    result = self.user.move(self.ai.my_board)
                except ValueError as e:
                    print('Непредвиденная ошибка.')
                    return None
                if result == -1:
                    return None
                if self.ai.my_board.get_alive_count() == 0:
                    self.draw()
                    print('Вы победили!')
                    return None
                if result == 0:
                    msg = 'Мимо'
                    break
                if result == 1:
                    msg = 'Корабль ранен!'
                if result == 2:
                    msg = 'Корабль убит!'
            # ход компьютера
            while True:
                self.draw()
                if msg != '':
                    print(msg)
                print('Ход компьютера...')
                time.sleep(2)
                try:
                    result = self.ai.move(self.user.my_board)
                except ValueError as e:
                    print('Непредвиденная ошибка.')
                    return None
                if result == -1:
                    return None
                if self.user.my_board.get_alive_count() == 0:
                    self.draw()
                    print('Вы проиграли!')
                    return None
                if result == 0:
                    msg = 'Мимо'
                    break
                if result == 1:
                    msg = 'Корабль ранен!'
                if result == 2:
                    msg = 'Корабль убит!'


game = Game()
game.loop()







