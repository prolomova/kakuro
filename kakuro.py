#!/usr/bin/env python3
"""
Реализация решателя головоломки какуро
"""

import sys
import re
import argparse
import slover


def main(args):
    '''
    Главная функция
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count', required=False, type=int,
                        help='This argument is a number of answers', default=1)
    parser.add_argument('-f', '--filename', required=False, type=str,
                        help='This argument is a file name, without '
                             'it you have to input data')
    parser.add_argument('-g', '--groups', nargs='+', required=False,
                        help='This argument are the coordinates of '
                             'cells whose values ​​are the same, '
                             'groups must be separated by "/", x and y '
                             'values must be separated by ",", '
                             'coordinate values must be separated by spaces')
    namespace = parser.parse_args(args)
    groups = []
    if namespace.groups is not None:
        groups.append([])
        cell = 0
        is_splited = False
        for item in namespace.groups:
            if item == ',':
                continue
            elif is_splited:
                groups[-1].append((cell, int(item)))
                is_splited = False
            elif re.search(re.compile(r'\d+,\d+'), item):
                coord = item.split(',')
                groups[-1].append((int(coord[0]), int(coord[1])))
            elif re.search(re.compile(r'\d+,'), item):
                cell = int(item[:-1])
                is_splited = True
            elif re.search(re.compile(r'\d+'), item):
                cell = int(item)
                is_splited = True
            elif item == '/':
                groups.append([])
    count = namespace.count
    strings = read_data(namespace.filename)
    try:
        board = Board(strings)
    except FormatException as err:
        print(err, file=sys.stderr)
        sys.exit(1)
    ans = list(map(str, slover.start(board, count, groups)))
    if ans:
        for answer in ans:
            print(answer)
            print()
        sys.exit(0)
    sys.exit(1)


def read_data(fname):
    """
    Функция, которая считывает входные данные
    """
    strings = []
    open_file = None
    if fname is not None:
        open_file = open(fname)
    else:
        open_file = sys.stdin
    with open_file as file:
        while True:
            line = file.readline()
            if not line.rstrip():
                break
            else:
                if line.strip() != "":
                    strings.append(line.strip())
    return strings


class FormatException(Exception):
    """
    Класс ошибки неправильного формата входных данных
    """
    def __init__(self, msg, line):
        super(FormatException, self).__init__(msg, line)
        self.type = msg
        self.line = line

    def __str__(self):
        return "{}: line {}".format(self.type, self.line)


class Cell:
    """
    Класс, описывающий клетку поля
    """
    def __init__(self, sum_vertical, sum_horizontal,
                 cur_sum_vertical, cur_sum_horizontal):
        self.cur_sum_horizontal = cur_sum_horizontal
        self.sum_horizontal = sum_horizontal
        self.sum_vertical = sum_vertical
        self.cur_sum_vertical = cur_sum_vertical
        self.value = 0

    def change_value(self, value, sum_horizontal, sum_vertical):
        """
        Функция, изменяющая значение клетки
        """
        self.cur_sum_horizontal = sum_horizontal + value - self.value
        self.cur_sum_vertical = sum_vertical + value - self.value
        self.value = value

    def __str__(self):
        return str(self.value)

class Board:
    """
    Класс, реализующий игровое поле
    """
    CELL_FORMAT = re.compile(r'(\d+|X)/(\d+|X)')

    def __init__(self, file):
        self.board = self.read(self.CELL_FORMAT, file)

    @staticmethod
    def read(cell_format, f_data):
        """
        Функция, считывающая данные в формат поля
        """
        def check_format(sum_board, is_vertical):
            for i in range(height):
                curr_sum = -1
                count = 0
                for j in range(width):
                    cell = sum_board[i][j]
                    if is_vertical:
                        cell = sum_board[j][i]
                    if cell != '0':
                        if curr_sum > (9 + 10 - count) * count / 2:
                            raise FormatException(
                                "Too large value of the sum", str(i + 1))
                        if cell != 'X':
                            curr_sum = int(cell)
                        if is_vertical:
                            sum_board[j][i] = 'X'
                        else:
                            sum_board[i][j] = 'X'
                    elif cell == '0':
                        count += 1
                        if curr_sum <= 0:
                            raise FormatException(
                                "Insufficient value of the sum", str(i + 1))
                        if is_vertical:
                            sum_board[j][i] = curr_sum
                        else:
                            sum_board[i][j] = curr_sum

        height = 0
        width = len(f_data[0].split(','))
        vertical_sum_board = []
        horizontal_sum_board = []
        for line in f_data:
            line_data = [i.strip() for i in line.split(',')
                         if (i.strip() != '')]
            horizontal_sum_board.append([])
            vertical_sum_board.append([])
            for cell in line_data:
                if cell in ('', '\n'):
                    continue
                found_cell = re.search(cell_format, cell)
                if found_cell is not None:
                    horizontal_sum_board[height].append(found_cell.group(1))
                    vertical_sum_board[height].append(found_cell.group(2))
                elif cell in ('X', '0'):
                    horizontal_sum_board[height].append(cell)
                    vertical_sum_board[height].append(cell)
                else:
                    raise FormatException("Wrong char", height + 1)
            height += 1

        check_format(horizontal_sum_board, False)
        check_format(vertical_sum_board, True)

        result = []
        for i in range(height):
            result.append([])
            for j in range(width):
                if vertical_sum_board[i][j] == 'X':
                    result[i].append('X')
                else:
                    result[i].append(Cell(vertical_sum_board[i][j],
                                          horizontal_sum_board[i][j], 0, 0))
        return result

    def __str__(self):
        lines = [' '.join(map(str, self.board[i]))
                 for i in range(len(self.board))]
        return '\n'.join(lines)


if __name__ == '__main__':
    main(sys.argv[1:])
