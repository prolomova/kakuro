#!/usr/bin/env python3
"""
Реализация решателя головоломки какуро
"""

from copy import deepcopy

def is_passed(board, groups):
    """
    Функция, которая проверяет корректность значений клеток с одинаковыми значениями
    """
    for group in groups:
        if not group:
            continue
        if isinstance(board[group[0][0]][group[0][1]], str):
            value = -1
        else:
            value = board[group[0][0]][group[0][1]].value
        for x, y in group:
            if isinstance(board[x][y], str):
                if value != -1:
                    return False
            elif board[x][y].value != value:
                return False
    return True


def start(board, count, groups=None):
    """
    Функция, которая возвращает решенные поля
    """
    if groups is None:
        groups = []
    ans = []
    boards = []
    boards.append(board)
    while boards and count > len(ans):
        board = boards.pop()
        next_free = try_find_next_free(board.board)
        x = next_free[1][0]
        y = next_free[1][1]
        if not next_free[0]:
            if is_passed(board.board, groups):
                ans.append(board)
        else:
            possible_values = get_possible_values(x, y, board.board)
            for value in possible_values:
                cur_sum_horizontal = 0
                cur_sum_vertical = 0
                new_board = deepcopy(board)
                if new_board.board[x][y - 1] != 'X':
                    cur_sum_horizontal = \
                        new_board.board[x][y - 1].cur_sum_horizontal
                if new_board.board[x - 1][y] != 'X':
                    cur_sum_vertical = \
                        new_board.board[x - 1][y].cur_sum_vertical

                if (board.board[x][y + 1] == 'X' and
                        cur_sum_horizontal + value !=
                        board.board[x][y].sum_horizontal):
                    continue
                elif (board.board[x + 1][y] == 'X' and
                      cur_sum_vertical + value !=
                      board.board[x][y].sum_vertical):
                    continue
                elif int(cur_sum_horizontal + value) > \
                        int(board.board[x][y].sum_horizontal):
                    continue
                elif cur_sum_vertical + value > board.board[x][y].sum_vertical:
                    continue
                new_board.board[x][y].change_value(value, cur_sum_horizontal,
                                                   cur_sum_vertical)
                boards.append(new_board)
    return ans


def get_possible_values(x, y, board):
    """
    Функция, возвращающая доступные значения для клетки с координатами x, y
    """
    height = len(board)
    width = len(board[0])
    possible_values = set(range(1, 10))
    for i in range(height):
        if str((board[i][y])) != 'X' and board[i][y].value in possible_values:
            possible_values.remove(board[i][y].value)
    for i in range(width):
        if str((board[x][i])) != 'X' and board[x][i].value in possible_values:
            possible_values.remove(board[x][i].value)
    return possible_values


def try_find_next_free(board):
    """
    Функция, возвращающая координаты свободной клетки
    """
    height = len(board)
    width = len(board[0])
    for i in range(height):
        for j in range(width):
            if str((board[i][j])) != 'X' and board[i][j].value == 0:
                return (True, (i, j))
    return (False, (-1, -1))
