from copy import deepcopy


class COLORS:
    YELLOW = '\033[93m'
    END = '\033[0m'


class Board:
    def __init__(self, file):
        self.wall = ' [=] '
        self.way = '  +  '
        self.coin = ' ($) '
        self.entry = '  E  '
        self.exit = '  S  '

        self.start_pos = None
        self.end_pos = None
        self.width = None
        self.height = None
        self.size = None
        self.board = self.build(file)

    def build(self, file):
        board = []
        for line_idx, line in enumerate(open(file, 'r').readlines()):
            column = []
            for column_idx, char in enumerate(line.split(' ')):
                if char == 'E':
                    self.start_pos = (line_idx, column_idx)
                    char = self.entry
                elif char == 'S':
                    self.end_pos = (line_idx, column_idx)
                    char = self.exit

                elif '1' == char:
                    char = self.wall
                elif '0' == char:
                    char = self.way
                else:
                    char = self.coin

                column.append(char)

            board.append(column)

        self.width = len(board[0])
        self.height = len(board)
        self.size = self.width + self.height

        return board

    def move(self, pos, movement):
        if movement == 3:
            if pos[0] < self.height - 1:
                return self.__check_pos((pos[0] + 1, pos[1])), (pos[0] + 1, pos[1])

            return 1, pos

        elif movement == 2:
            if pos[0] > 0:
                return self.__check_pos((pos[0] - 1, pos[1])), (pos[0] - 1, pos[1])

            return 1, pos

        elif movement == 1:
            if pos[1] < self.width - 1:
                return self.__check_pos((pos[0], pos[1] + 1)), (pos[0], pos[1] + 1)

            return 1, pos

        elif movement == 0:
            if pos[1] > 0:
                return self.__check_pos((pos[0], pos[1] - 1)), (pos[0], pos[1] - 1)

            return 1, pos

    def get_data(self, pos):
        if pos[0] + 1 < self.height:
            top = self.__check_pos((pos[0] + 1, pos[1])) / 30
            top_distance = self.__manhattan((pos[0] + 1, pos[1])) / self.size
        else:
            top = 1
            top_distance = 1.0

        if pos[0] > 0:
            bottom = self.__check_pos((pos[0] - 1, pos[1])) / 30
            bottom_distance = self.__manhattan((pos[0] - 1, pos[1])) / self.size
        else:
            bottom = 1
            bottom_distance = 1.0

        if pos[1] + 1 < self.width:
            right = self.__check_pos((pos[0], pos[1] + 1)) / 30
            right_distance = self.__manhattan((pos[0], pos[1] + 1)) / self.size
        else:
            right = 1
            right_distance = 1.0

        if pos[1] > 0:
            left = self.__check_pos((pos[0], pos[1] - 1)) / 30
            left_distance = self.__manhattan((pos[0], pos[1] - 1)) / self.size
        else:
            left = 1
            left_distance = 1.0

        return [top, bottom, right, left, left_distance, right_distance, bottom_distance, top_distance]

    def build_execution(self, path):
        shown_board = deepcopy(self.board)

        for idx, pos in enumerate(path):
            shown_board[pos[0]][pos[1]] = f'{COLORS.YELLOW}{idx: ^5}{COLORS.END}'

        return '\n'.join(' '.join(line) for line in shown_board)

    def build_save_execution(self, path):
        shown_board = deepcopy(self.board)

        for idx, pos in enumerate(path):
            shown_board[pos[0]][pos[1]] = f'{idx: ^5}'

        return '\n'.join(' '.join(line) for line in shown_board)

    def __check_pos(self, pos):
        if self.board[pos[0]][pos[1]] == self.wall:
            return 1

        elif self.board[pos[0]][pos[1]] == self.way:
            return 10

        elif self.board[pos[0]][pos[1]] == self.coin:
            return 20

        elif self.board[pos[0]][pos[1]] == self.entry:
            return 10

        return 30

    def __manhattan(self, pos):
        return abs(pos[0] - self.end_pos[0]) + abs(pos[1] - self.end_pos[1])


if __name__ == '__main__':
    b = Board('board.txt')
    print(b)
    print(b.build_save_execution([(0, 0), (0, 1), (0, 2),
                             (1, 2),
                             (2, 2), (2, 3),
                             (3, 3),
                             (4, 3), (4, 4),
                             (5, 4),
                             (6, 4),
                             (7, 4),
                             (8, 4), (8, 5), (8, 6), (8, 7),
                             (9, 7), (9, 8), (9, 9)])
          )

    print(b.get_data((9, 8)))
