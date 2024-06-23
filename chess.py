from abc import abstractmethod, ABC
import re
import sys
import math

args = sys.argv[1:]
if "in" in args:
    f_in = open("test-in.txt")
    sys.stdin = f_in
if "out" in args:
    f_out = open("test-out.txt", "wt")
    sys.stdout = f_out


class CoordinateUtility:
    @staticmethod
    def index_to_cartesian(r, c):
        y = 8 - r
        x = c + 1
        return (x, y)

    @staticmethod
    def cartesian_to_index(x, y):
        r = 8 - y
        c = x - 1
        return (r, c)


class User:
    username: str = ""
    password: str = ""
    score = 0
    wins = 0
    draws = 0
    loses = 0
    undo_limit = 2
    users: list = []

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.score = 0
        self.wins = 0
        self.draws = 0
        self.loses = 0
        self.undo_limit = 2

    def __eq__(self, other):
        if isinstance(other, User):
            return self.username == other.username and self.password == other.password
        elif isinstance(other, str):
            return self.username == other

    def __repr__(self):
        return self.username

    @staticmethod
    def register(username, password):
        if not username.isascii():
            print("username format is invalid")
            return
        if not password.isascii():
            print("password format is invalid")
            return
        if re.findall(r"\W", username):
            print("username format is invalid")
            return
        if re.findall(r"\W", password):
            print("password format is invalid")
            return
        if username in User.users:
            print("a user exists with this username")
            return
        u1 = User(username, password)
        User.users.append(u1)
        print("register successful")

    @staticmethod
    def user_login(username, password=""):
        if not username.isascii():
            print("username format is invalid")
            return
        if re.findall(r"\W", username):
            print("username format is invalid")
            return
        if username not in User.users:
            print("no user exists with this username")
            return
        if password == "":
            return User.users[User.users.index(username)]
        if not password.isascii():
            print("password format is invalid")
            return
        if re.findall(r"\W", password):
            print("password format is invalid")
            return
        u1 = User(username, password)
        if u1 not in User.users:
            print("incorrect password")
            return
        return User.users[User.users.index(u1)]

    @staticmethod
    def remove_user(username, password):
        if not username.isascii():
            print("username format is invalid")
            return
        if not password.isascii():
            print("password format is invalid")
            return
        if re.findall(r"\W", username):
            print("username format is invalid")
            return
        if re.findall(r"\W", password):
            print("password format is invalid")
            return
        if username not in User.users:
            print("no user exists with this username")
            return
        u1 = User(username, password)
        if u1 not in User.users:
            print("incorrect password")
            return
        User.users.remove(User.users[User.users.index(u1)])
        print(f"removed {username} successfully")
        return

    @staticmethod
    def show_users():
        print(*(sorted(User.users, key=lambda e: e.username)), sep="\n")
        return

    @staticmethod
    def scoreboard():
        users = sorted(User.users, key=lambda e: (e.score, e.wins, e.draws), reverse=True)
        # TODO
        # users = sorted(users, key=lambda e: e.loses)
        # users = sorted(users, key=lambda e: e.username)
        for u in users:
            print(f"{u.username} {u.score} {u.wins} {u.draws} {u.loses}")
        return

    @staticmethod
    def logout_users(game):
        game.user_white = None
        game.user_black = None
        print("logout successful")
        return

    @staticmethod
    def forfeit(chs):
        user_black = User.users[User.users.index(chs.user_black)]
        user_white = User.users[User.users.index(chs.user_white)]
        if chs.white_turn:
            user_black.score = user_black.score + 2
            if user_white.score > 0:
                user_white.score = user_white.score - 1
            print("you have forfeited")
            print(f"player {user_black.username} with color black won")
            chs.user_black = None
            return
        user_white.score = user_white.score + 2
        if user_black.score > 0:
            user_black.score = user_black.score - 1
        print("you have forfeited")
        print(f"player {user_white.username} with color white won")
        chs.user_black = None
        return


class Piece(ABC):
    name = ""
    color = ""
    x = 0
    y = 0

    def __init__(self, name, color, x, y):
        self.name = name
        self.color = color
        self.x = x
        self.y = y

    def __repr__(self):
        return self.name + self.color

    # ???????
    @abstractmethod
    def move(self, x, y, board):
        pass
    # create your abstract methods here


# in these classes implement method that you abstracted in Piece  class
class Pawn(Piece):
    def __init__(self, color, x, y):
        super().__init__("P", color, x, y)

    def move(self, x, y, board):
        start_r, start_c = CoordinateUtility.cartesian_to_index(self.x, self.y)
        end_r, end_c = CoordinateUtility.cartesian_to_index(x, y)
        pawn = board[start_r][start_c]
        can_destroy_left = False
        can_destroy_right = False
        if pawn.color == "w":
            # checks pawn going forward
            if y <= self.y:
                print("cannot move to the spot")
                return False
            if not -1 <= x - self.x <= 1:
                print("cannot move to the spot")
                return False
            # checks if white pawn can destroy right
            if self.x < 8:
                if (right_side := board[start_r - 1][start_c + 1]) is not None:
                    if right_side.color != pawn.color:
                        can_destroy_right = True
            # checks if white pawn can destroy left
            if self.x > 1:
                if (left_side := board[start_r - 1][start_c - 1]) is not None:
                    if left_side.color != pawn.color:
                        can_destroy_left = True

            # if pawn didnt move
            if self.y == 2:
                if x == self.x:
                    if board[end_r][end_c] is not None:
                        print("cannot move to the spot")
                        return False
                    elif y - self.y <= 2:
                        board[end_r][end_c] = board[start_r][start_c]
                        board[start_r][start_c] = None
                        x, y = CoordinateUtility.index_to_cartesian(end_r, end_c)
                        self.x = x
                        self.y = y
                        print('moved')
                        return True
                    else:
                        print("cannot move to the spot")
                        return
                elif can_destroy_right and x - self.x == 1:
                    board[end_r][end_c] = board[start_r][start_c]
                    board[start_r][start_c] = None
                    x, y = CoordinateUtility.index_to_cartesian(end_r, end_c)
                    self.x = x
                    self.y = y
                    print('rival piece destroyed')
                    return True
                elif can_destroy_left and x - self.x == -1:
                    board[end_r][end_c] = board[start_r][start_c]
                    board[start_r][start_c] = None
                    x, y = CoordinateUtility.index_to_cartesian(end_r, end_c)
                    self.x = x
                    self.y = y
                    print('rival piece destroyed')
                    return True
                else:
                    print("cannot move to the spot")
                    return False
            # if pawn moved
            else:
                if x == self.x:
                    if board[end_r][end_c] is not None:
                        print("cannot move to the spot")
                        return False
                    elif y - self.y == 1:
                        board[end_r][end_c] = board[start_r][start_c]
                        board[start_r][start_c] = None
                        x, y = CoordinateUtility.index_to_cartesian(end_r, end_c)
                        self.x = x
                        self.y = y
                        print('moved')
                        return True
                    else:
                        print("cannot move to the spot")
                        return False
                elif can_destroy_right and x - self.x == 1:
                    board[end_r][end_c] = board[start_r][start_c]
                    board[start_r][start_c] = None
                    x, y = CoordinateUtility.index_to_cartesian(end_r, end_c)
                    self.x = x
                    self.y = y
                    print('rival piece destroyed')
                    return True
                elif can_destroy_left and x - self.x == -1:
                    board[end_r][end_c] = board[start_r][start_c]
                    board[start_r][start_c] = None
                    x, y = CoordinateUtility.index_to_cartesian(end_r, end_c)
                    self.x = x
                    self.y = y
                    print('rival piece destroyed')
                    return True
                else:
                    print("cannot move to the spot")
                    return False

        if pawn.color == "b":
            # checks pawn going forward
            if y >= self.y:
                print("cannot move to the spot")
                return False
            if not -1 <= x - self.x <= 1:
                print("cannot move to the spot")
                return False
            # checks if white pawn can destroy right
            if self.x < 8:
                if (right_side := board[start_r + 1][start_c + 1]) is not None:
                    if right_side.color != pawn.color:
                        can_destroy_right = True
            # checks if white pawn can destroy left
            if self.x > 1:
                if (left_side := board[start_r + 1][start_c - 1]) is not None:
                    if left_side.color != pawn.color:
                        can_destroy_left = True

            # if pawn didnt move
            if self.y == 7:
                if x == self.x:
                    if board[end_r][end_c] is not None:
                        print("cannot move to the spot")
                        return False
                    elif self.y - y <= 2:
                        board[end_r][end_c] = board[start_r][start_c]
                        board[start_r][start_c] = None
                        x, y = CoordinateUtility.index_to_cartesian(end_r, end_c)
                        self.x = x
                        self.y = y
                        print('moved')
                        return True
                    else:
                        print("cannot move to the spot")
                        return False
                elif can_destroy_right and x - self.x == 1:
                    board[end_r][end_c] = board[start_r][start_c]
                    board[start_r][start_c] = None
                    x, y = CoordinateUtility.index_to_cartesian(end_r, end_c)
                    self.x = x
                    self.y = y
                    print('rival piece destroyed')
                    return True
                elif can_destroy_left and x - self.x == -1:
                    board[end_r][end_c] = board[start_r][start_c]
                    board[start_r][start_c] = None
                    x, y = CoordinateUtility.index_to_cartesian(end_r, end_c)
                    self.x = x
                    self.y = y
                    print('rival piece destroyed')
                    return True
                else:
                    print("cannot move to the spot")
                    return False
            # if pawn moved
            else:
                if x == self.x:
                    if board[end_r][end_c] is not None:
                        print("cannot move to the spot")
                        return False
                    elif self.y - y == 1:
                        board[end_r][end_c] = board[start_r][start_c]
                        board[start_r][start_c] = None
                        x, y = CoordinateUtility.index_to_cartesian(end_r, end_c)
                        self.x = x
                        self.y = y
                        print('moved')
                        return True
                    else:
                        print("cannot move to the spot")
                        return False
                elif can_destroy_right and x - self.x == 1:
                    board[end_r][end_c] = board[start_r][start_c]
                    board[start_r][start_c] = None
                    x, y = CoordinateUtility.index_to_cartesian(end_r, end_c)
                    self.x = x
                    self.y = y
                    print('rival piece destroyed')
                    return True
                elif can_destroy_left and x - self.x == -1:
                    board[end_r][end_c] = board[start_r][start_c]
                    board[start_r][start_c] = None
                    x, y = CoordinateUtility.index_to_cartesian(end_r, end_c)
                    self.x = x
                    self.y = y
                    print('rival piece destroyed')
                    return True
                else:
                    print("cannot move to the spot")
                    return False


class Rook(Piece):

    def __init__(self, color, x, y):
        super().__init__("R", color, x, y)

    def move(self, x, y, board):
        start_r, start_c = CoordinateUtility.cartesian_to_index(self.x, self.y)
        end_r, end_c = CoordinateUtility.cartesian_to_index(x, y)
        if self.x == x and self.y == y:
            print("cannot move to the spot")
            return False
        elif self.x == x:
            move_range = start_r - end_r
            if move_range > 0:
                spots = [board[start_r - i][start_c] for i in range(1, move_range)]
            else:
                move_range = abs(move_range)
                spots = [board[start_r + i][start_c] for i in range(1, move_range)]
            can_move = not any(spots)
            if can_move:
                if (destination := board[end_r][end_c]) is None:
                    board[end_r][end_c] = board[start_r][start_c]
                    board[start_r][start_c] = None
                    x, y = CoordinateUtility.index_to_cartesian(end_r, end_c)
                    self.x = x
                    self.y = y
                    print('moved')
                    return True
                else:
                    if (peice := board[start_r][start_c]).color == destination.color:
                        print('cannot move to the spot')
                        return False
                    elif peice.color != destination.color:
                        board[end_r][end_c] = board[start_r][start_c]
                        board[start_r][start_c] = None
                        x, y = CoordinateUtility.index_to_cartesian(end_r, end_c)
                        self.x = x
                        self.y = y
                        print('rival piece destroyed')
                        return True
            else:
                print('cannot move to the spot')
                return False

        elif self.y == y:
            move_range = start_c - end_c
            if move_range > 0:
                spots = [board[start_r][start_c - i] for i in range(1, move_range)]
            else:
                move_range = abs(move_range)
                spots = [board[start_r][start_c + i] for i in range(1, move_range)]
            can_move = not any(spots)
            if can_move:
                if (destination := board[end_r][end_c]) is None:
                    board[end_r][end_c] = board[start_r][start_c]
                    board[start_r][start_c] = None
                    x, y = CoordinateUtility.index_to_cartesian(end_r, end_c)
                    self.x = x
                    self.y = y
                    print('moved')
                    return True
                else:
                    if (peice := board[start_r][start_c]).color == destination.color:
                        print('cannot move to the spot')
                        return False
                    elif peice.color != destination.color:
                        board[end_r][end_c] = board[start_r][start_c]
                        board[start_r][start_c] = None
                        x, y = CoordinateUtility.index_to_cartesian(end_r, end_c)
                        self.x = x
                        self.y = y
                        print('rival piece destroyed')
                        return True
            else:
                print('cannot move to the spot')
                return False
        else:
            print("cannot move to the spot")
            return False


class Knight(Piece):

    def __init__(self, color, x, y):
        super().__init__("N", color, x, y)

    def move(self, x, y, board):
        start_r, start_c = CoordinateUtility.cartesian_to_index(self.x, self.y)
        end_r, end_c = CoordinateUtility.cartesian_to_index(x, y)
        if x == self.x and y == self.y:
            print('cannot move to the spot')
            return False
        # rast bala
        elif x - self.x == 2 and y - self.y == 1:
            pass
        # rast pain
        elif x - self.x == 2 and y - self.y == -1:
            pass
        # chap bala
        elif x - self.x == -2 and y - self.y == 1:
            pass
        # chap pain
        elif x - self.x == -2 and y - self.y == -1:
            pass
        # bala rast
        elif x - self.x == 1 and y - self.y == 2:
            pass
        # bala chap
        elif x - self.x == -1 and y - self.y == 2:
            pass
        # pain rast
        elif x - self.x == 1 and y - self.y == -2:
            pass
        # pain chap
        elif x - self.x == -1 and y - self.y == -2:
            pass
        else:
            print('cannot move to the spot')
            return False
        if (destination := board[end_r][end_c]) is None:
            board[end_r][end_c] = board[start_r][start_c]
            board[start_r][start_c] = None
            x, y = CoordinateUtility.index_to_cartesian(end_r, end_c)
            self.x = x
            self.y = y
            print('moved')
            return True
        else:
            if (peice := board[start_r][start_c]).color == destination.color:
                print('cannot move to the spot')
                return False
            elif peice.color != destination.color:
                board[end_r][end_c] = board[start_r][start_c]
                board[start_r][start_c] = None
                x, y = CoordinateUtility.index_to_cartesian(end_r, end_c)
                self.x = x
                self.y = y
                print('rival piece destroyed')
                return True


class Bishop(Piece):
    def __init__(self, color, x, y):
        super().__init__("B", color, x, y)

    def move(self, x, y, board):
        start_r, start_c = CoordinateUtility.cartesian_to_index(self.x, self.y)
        end_r, end_c = CoordinateUtility.cartesian_to_index(x, y)
        x_range = x - self.x
        y_range = y - self.y
        move_range = abs(x_range)

        if x == self.x or y == self.y:
            print('cannot move to the spot')
            return False
        elif abs(x_range) != abs(y_range):
            print('cannot move to the spot')
            return False
        # bala rast
        elif 0 < x_range and 0 < y_range:
            spots = [board[start_r - i][start_c + i] for i in range(1, move_range)]
        # bala chap
        elif x_range < 0 < y_range:
            spots = [board[start_r - i][start_c - i] for i in range(1, move_range)]
        # pain rast
        elif y_range < 0 < x_range:
            spots = [board[start_r + i][start_c + i] for i in range(1, move_range)]
        # pain chap
        elif x_range < 0 and y_range < 0:
            spots = [board[start_r + i][start_c - i] for i in range(1, move_range)]
        else:
            print('cannot move to the spot')
            return False
        can_move = not any(spots)
        if can_move:
            if (destination := board[end_r][end_c]) is None:
                board[end_r][end_c] = board[start_r][start_c]
                board[start_r][start_c] = None
                x, y = CoordinateUtility.index_to_cartesian(end_r, end_c)
                self.x = x
                self.y = y
                print('moved')
                return True
            else:
                if (peice := board[start_r][start_c]).color == destination.color:
                    print('cannot move to the spot')
                    return False
                elif peice.color != destination.color:
                    board[end_r][end_c] = board[start_r][start_c]
                    board[start_r][start_c] = None
                    x, y = CoordinateUtility.index_to_cartesian(end_r, end_c)
                    self.x = x
                    self.y = y
                    print('rival piece destroyed')
                    return True
        else:
            print('cannot move to the spot')
            return False


class Queen(Piece):

    def __init__(self, color, x, y):
        super().__init__("Q", color, x, y)

    def move(self, x, y, board):
        start_r, start_c = CoordinateUtility.cartesian_to_index(self.x, self.y)
        end_r, end_c = CoordinateUtility.cartesian_to_index(x, y)
        x_range = x - self.x
        y_range = y - self.y
        move_range = abs(x_range)

        if x == self.x and y == self.y:
            print('cannot move to the spot')
            return False
        elif self.x == x:
            move_range = start_r - end_r
            if move_range > 0:
                spots = [board[start_r - i][start_c] for i in range(1, move_range)]
            else:
                move_range = abs(move_range)
                spots = [board[start_r + i][start_c] for i in range(1, move_range)]
            can_move = not any(spots)
            if can_move:
                if (destination := board[end_r][end_c]) is None:
                    board[end_r][end_c] = board[start_r][start_c]
                    board[start_r][start_c] = None
                    x, y = CoordinateUtility.index_to_cartesian(end_r, end_c)
                    self.x = x
                    self.y = y
                    print('moved')
                    return True
                else:
                    if (peice := board[start_r][start_c]).color == destination.color:
                        print('cannot move to the spot')
                        return False
                    elif peice.color != destination.color:
                        board[end_r][end_c] = board[start_r][start_c]
                        board[start_r][start_c] = None
                        x, y = CoordinateUtility.index_to_cartesian(end_r, end_c)
                        self.x = x
                        self.y = y
                        print('rival piece destroyed')
                        return True
            else:
                print('cannot move to the spot')
                return False
        elif self.y == y:
            move_range = start_c - end_c
            if move_range > 0:
                spots = [board[start_r][start_c - i] for i in range(1, move_range)]
            else:
                move_range = abs(move_range)
                spots = [board[start_r][start_c + i] for i in range(1, move_range)]
            can_move = not any(spots)
            if can_move:
                if (destination := board[end_r][end_c]) is None:
                    board[end_r][end_c] = board[start_r][start_c]
                    board[start_r][start_c] = None
                    x, y = CoordinateUtility.index_to_cartesian(end_r, end_c)
                    self.x = x
                    self.y = y
                    print('moved')
                    return True
                else:
                    if (peice := board[start_r][start_c]).color == destination.color:
                        print('cannot move to the spot')
                        return False
                    elif peice.color != destination.color:
                        board[end_r][end_c] = board[start_r][start_c]
                        board[start_r][start_c] = None
                        x, y = CoordinateUtility.index_to_cartesian(end_r, end_c)
                        self.x = x
                        self.y = y
                        print('rival piece destroyed')
                        return True
            else:
                print('cannot move to the spot')
                return False
        elif abs(x_range) != abs(y_range):
            print('cannot move to the spot')
            return False
        # bala rast
        elif 0 < x_range and 0 < y_range:
            spots = [board[start_r - i][start_c + i] for i in range(1, move_range)]
        # bala chap
        elif x_range < 0 < y_range:
            spots = [board[start_r - i][start_c - i] for i in range(1, move_range)]
        # pain rast
        elif y_range < 0 < x_range:
            spots = [board[start_r + i][start_c + i] for i in range(1, move_range)]
        # pain chap
        elif x_range < 0 and y_range < 0:
            spots = [board[start_r + i][start_c - i] for i in range(1, move_range)]
        else:
            print('cannot move to the spot')
            return False
        can_move = not any(spots)
        if can_move:
            if (destination := board[end_r][end_c]) is None:
                board[end_r][end_c] = board[start_r][start_c]
                board[start_r][start_c] = None
                x, y = CoordinateUtility.index_to_cartesian(end_r, end_c)
                self.x = x
                self.y = y
                print('moved')
                return True
            else:
                if (peice := board[start_r][start_c]).color == destination.color:
                    print('cannot move to the spot')
                    return False
                elif peice.color != destination.color:
                    board[end_r][end_c] = board[start_r][start_c]
                    board[start_r][start_c] = None
                    x, y = CoordinateUtility.index_to_cartesian(end_r, end_c)
                    self.x = x
                    self.y = y
                    print('rival piece destroyed')
                    return True
        else:
            print('cannot move to the spot')
            return False


class King(Piece):

    def __init__(self, color, x, y):
        super().__init__("K", color, x, y)

    def move(self, x, y, board):
        if x == self.x and y == self.y:
            print('cannot move to the spot')
            return False
        if 1 < abs(x - self.x) or 1 < abs(y - self.y):
            print('cannot move to the spot')
            return False
        start_r, start_c = CoordinateUtility.cartesian_to_index(self.x, self.y)
        end_r, end_c = CoordinateUtility.cartesian_to_index(x, y)
        if (destination := board[end_r][end_c]) is None:
            board[end_r][end_c] = board[start_r][start_c]
            board[start_r][start_c] = None
            x, y = CoordinateUtility.index_to_cartesian(end_r, end_c)
            self.x = x
            self.y = y
            print('moved')
            return True
        else:
            if (peice := board[start_r][start_c]).color == destination.color:
                print('cannot move to the spot')
                return False
            elif peice.color != destination.color:
                board[end_r][end_c] = board[start_r][start_c]
                board[start_r][start_c] = None
                x, y = CoordinateUtility.index_to_cartesian(end_r, end_c)
                self.x = x
                self.y = y
                print('rival piece destroyed')
                return True


class Chess:
    board = []
    user_white = None
    user_black = None
    white_turn = True
    selected_piece = None
    moved = False
    did_undo = False
    limit = 0

    last_destroyed_piece = None
    last_piece_coordination = []
    moved_piece_coordination = []

    def __init__(self, user_white, user_black, limit):
        self.user_white = user_white
        self.user_black = user_black
        self.limit = limit
        self.selected_piece = None
        self.moved = False
        self.did_undo = False

        self.last_destroyed_piece = None
        self.last_piece_coordination = []
        self.moved_piece_coordination = []

    def initialize(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        # White pieces
        self.board[6] = [Pawn("w", x, 2) for x in range(1, 9)]
        self.board[7][0] = Rook("w", 1, 1)
        self.board[7][1] = Knight("w", 2, 1)
        self.board[7][2] = Bishop("w", 3, 1)
        self.board[7][3] = Queen("w", 4, 1)
        self.board[7][4] = King("w", 5, 1)
        self.board[7][5] = Bishop("w", 6, 1)
        self.board[7][6] = Knight("w", 7, 1)
        self.board[7][7] = Rook("w", 8, 1)
        # Black pieces
        self.board[1] = [Pawn("b", x, 7) for x in range(1, 9)]
        self.board[0][0] = Rook("b", 1, 8)
        self.board[0][1] = Knight("b", 2, 8)
        self.board[0][2] = Bishop("b", 3, 8)
        self.board[0][3] = Queen("b", 4, 8)
        self.board[0][4] = King("b", 5, 8)
        self.board[0][5] = Bishop("b", 6, 8)
        self.board[0][6] = Knight("b", 7, 8)
        self.board[0][7] = Rook("b", 8, 8)

    def print(self):
        print(*["|".join([str(cell) if cell is not None else "  " for cell in row]) for row in self.board], sep="|\n",
              end="|\n")

    def set_user(self, user, limit):
        if user is None:
            return
        if self.user_white is None:
            self.user_white = user
            print("login successful")
            return
        if not self.set_limit(limit) and limit is not None:
            return
        if self.user_white == user:
            print("you must choose another player to start a game")
            return
        self.user_black = user
        return True

    def set_limit(self, limit):
        if int(limit) < 0:
            print("number should be positive to have a limit or 0 for no limit")
            return
        self.limit = int(limit)
        return True


chess = Chess(None, None, limit=0)
while True:
    txt = input().strip().split()
    if chess.user_white is None:
        if txt[0] == "help" and len(txt) == 1:
            print("register [username] [password]")
            print("login [username] [password]")
            print("remove [username] [password]")
            print("list_users")
            print("help")
            print("exit")

        elif txt[0] == "register" and len(txt) == 3:
            User.register(txt[1], txt[2])

        elif txt[0] == "login" and len(txt) == 3:
            chess.set_user(User.user_login(txt[1], txt[2]), None)

        elif txt[0] == "remove" and len(txt) == 3:
            User.remove_user(txt[1], txt[2])

        elif txt[0] == "list_users" and len(txt) == 1:
            User.show_users()

        elif txt[0] == "exit" and len(txt) == 1:
            print("program ended")
            exit(0)

        else:
            print("invalid command")
    elif chess.user_white is not None and chess.user_black is None:
        if txt[0] == "help" and len(txt) == 1:
            print("new_game [username] [limit]")
            print("scoreboard")
            print("list_users")
            print("help")
            print("logout")

        elif txt[0] == "new_game" and len(txt) == 3:
            if not txt[2].isdigit():
                print("invalid command")
            elif chess.set_user(User.user_login(txt[1]), txt[2]):
                print(
                    f"new game started successfully between {chess.user_white} and {chess.user_black} with limit {chess.limit}")
                chess.initialize()

        elif txt[0] == "scoreboard" and len(txt) == 1:
            User.scoreboard()
        elif txt[0] == "list_users" and len(txt) == 1:
            User.show_users()
        elif txt[0] == "logout" and len(txt) == 1:
            User.logout_users(chess)
        else:
            print("invalid command")
    else:
        if txt[0] == "help" and len(txt) == 1:
            print("select [x],[y]")
            print("deselect")
            print("move [x],[y]")
            print("next_turn")
            print("show_turn")
            print("undo")
            print("undo_number")
            print("show_moves [-all]")
            print("show_killed [-all]")
            print("show_board")
            print("help")
            print("forfeit")
        elif txt[0] == "show_board" and len(txt) == 1:
            chess.print()
        elif txt[0] == "select" and len(txt) == 2:
            moves = txt[1].split(",")
            y = int(moves[0])
            x = int(moves[1])
            if not (1 <= x <= 8 and 1 <= y <= 8):
                print("wrong coordination")
            else:
                spot = chess.board[8 - y][x - 1]
                if spot is None:
                    print("no piece on this spot")
                else:
                    if chess.white_turn:
                        if spot.color != "w":
                            print("you can only select one of your pieces")
                        else:
                            chess.selected_piece = spot
                            chess.last_piece_coordination = [8 - y, x - 1]
                            print("selected")
                    else:
                        if spot.color != "b":
                            print("you can only select one of your pieces")
                        else:
                            chess.selected_piece = spot
                            chess.last_piece_coordination = [8 - y, x - 1]
                            print("selected")
        elif txt[0] == "deselect" and len(txt) == 1:
            if chess.selected_piece is None:
                print("no piece is selected")
            else:
                chess.selected_piece = None
                print("deselected")
        elif txt[0] == "forfeit" and len(txt) == 1:
            User.forfeit(chess)
        elif txt[0] == "move" and len(txt) == 2:
            # TODO
            if chess.moved:
                print("already moved")
            else:
                moves = txt[1].split(",")
                y = int(moves[0])
                x = int(moves[1])
                if not (1 <= x <= 8 and 1 <= y <= 8):
                    print("wrong coordination")
                elif chess.selected_piece is None:
                    print("do not have any selected piece")
                else:
                    chess.last_destroyed_piece = chess.board[8 - y][x - 1]
                    move = chess.selected_piece.move(x, y, chess.board)
                    if move:
                        chess.moved = True
                        chess.moved_piece_coordination = [8 - y, x - 1]
        elif txt[0] == "next_turn" and len(txt) == 1:
            if not chess.moved:
                print("you must move then proceed to next turn")
            else:
                chess.moved = False
                chess.did_undo = False
                chess.white_turn = not chess.white_turn
                chess.selected_piece =  None
                print("turn completed")
        elif txt[0] == "show_turn" and len(txt) == 1:
            if chess.white_turn:
                print(f"it is player {chess.user_white.username} turn with color white")
            else:
                print(f"it is player {chess.user_black.username} turn with color black")

        elif txt[0] == "undo" and len(txt) == 1:
            active_user = None
            if chess.white_turn:
                active_user = chess.user_white
            else:
                active_user = chess.user_black

            if active_user.undo_limit == 0:
                print("you cannot undo anymore")
            else:
                if not chess.moved:
                    print("you must move before undo")
                else:
                    if chess.did_undo:
                        print("you have used your undo for this turn")
                    else:
                        chess.did_undo = True
                        active_user.undo_limit -= 1

                        last_row = chess.last_piece_coordination[0]
                        last_col = chess.last_piece_coordination[1]

                        moved_row = chess.moved_piece_coordination[0]
                        moved_col = chess.moved_piece_coordination[1]

                        piece = chess.board[moved_row][moved_col]
                        x, y = CoordinateUtility.index_to_cartesian(last_row, last_col)
                        piece.x = x
                        piece.y = y

                        chess.board[last_row][last_col] = piece

                        chess.board[moved_row][moved_col] = chess.last_destroyed_piece

                        chess.moved = False
                        print("undo completed")

        elif txt[0] == "undo_number" and len(txt) == 1:
            active_user = None
            if chess.white_turn:
                active_user = chess.user_white
            else:
                active_user = chess.user_black
            print(f"you have {active_user.undo_limit} undo moves")

        else:
            print("invalid command")