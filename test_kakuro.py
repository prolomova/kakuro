#!/usr/bin/env python3
"""
Реализация решателя головоломки какуро
"""

import unittest
import slover as s
import kakuro as t


class Test(unittest.TestCase):
    """
    Тесты на логику головоломки какуро
    """

    @staticmethod
    def process(f_data):
        """
         Функция, которая убирает пустые строки и лишние пробелы
        """
        return [i.strip()
                for i in f_data.split('\n')
                if i.strip() != '']

    def test_simple(self):
        """
        Тест, проверяющий корректность алгоритма
        """
        field = t.Board(self.process("""
            X,  X,  X/7,X/6,X
            X,  4/4,0,  0,  X
            7/X,0,  0,  0,  X
            6/X,0,  0,  0,  X
            X,  X,  X,  X,  X
            """))
        excpected = set()
        excpected.add("""X X X X X
X X 1 3 X
X 1 4 2 X
X 3 2 1 X
X X X X X""")
        answers = set(str(i) for i in s.start(field, 1))
        self.assertSetEqual(answers, excpected)

    def test_many_answers(self):
        """
        Тест, проверяющий случаи с несколькими ответами
        """
        field = t.Board(self.process("""
            X,  X/4,X/6,X
            5/X,0,  0,  X
            5/X,0,  0,  X
            X,  X,  X,  X
                    """))
        excpected = set()
        excpected.add("""X X X X
X 1 4 X
X 3 2 X
X X X X""")
        excpected.add("""X X X X
X 3 2 X
X 1 4 X
X X X X""")
        answers = set(str(i) for i in s.start(field, 3))
        self.assertSetEqual(answers, excpected)

    def test_big_board(self):
        """
        Тест, проверяющий корректность при вводе больших данных
        """
        field = t.Board(self.process("""
            X,   X,   X/10,X/17,X,   X,  X
            X,   13/X,0,   0,   X/13,X/3,X
            X,   14/3,0,   0,   0,   0,  X
            4/X, 0,   0,   6/10,0,   0,  X
            11/X,0,   0,   0,   0,   X,  X
            X,   X,   8/X, 0,   0,   X,  X
            X,   X,   X,   X,   X,   X,  X
            """))
        excpected = set()
        excpected.add("""X X X X X X X
X X 4 9 X X X
X X 2 8 3 1 X
X 1 3 X 4 2 X
X 2 1 3 5 X X
X X X 7 1 X X
X X X X X X X""")
        answers = set(str(i) for i in s.start(field, 1))
        self.assertSetEqual(answers, excpected)

    def test_incorrect_input(self):
        """
        Тест, проверяющий работу алгоритма при неправильном формате ввода
        """
        try:
            res = t.Board(
                self.process("""
            X,   X,    X/17,X/29, X,  X
            X,   17/12,0,   0,    X/8,X
            14/X,0,    0,   0,    0,  X
            29/X,0,    0,   0,    0,  X
            X,   6/X,  0,   0,    X,  X
            X,   X,    X,   X,    X,  A""")).board
        except t.FormatException:
            res = None
        self.assertEqual(None, res)

    def test_not_enought_horizontal_data(self):
        """
        Тест, проверяющий работу при недостатке данных по горизонтали
        """
        try:
            board = t.Board(
                self.process("""
            X,   X,    X/17,X/29, X,  X
            X,   17/12,0,   0,    X/8,X
            14/X,0,    0,   0,    0,  X
            X,   0,    0,   0,    0,  X
            X,   6/X,  0,   0,    X,  X
            X,   X,    X,   X,    X,  X""")).board
        except t.FormatException:
            board = None
        self.assertEqual(None, board)

    def test_not_enought_vertical_data(self):
        """
        Тест, проверяющий работу при недостатке данных по вертикали
        """
        try:
            board = t.Board(
                self.process("""
            X,   X,    X,X/29, X,  X
            X,   17/12,0,0,    X/8,X
            14/X,0,    0,0,    0,  X
            29/X,0,    0,0,    0,  X
            X,   6/X,  0,0,    X,  X
            X,   X,    X,X,    X,  X""")).board
        except t.FormatException:
            board = None
        self.assertEqual(None, board)

    def test_incorrect_vertical_data(self):
        """
        Тест, проверяющий работу алгоритма при вводе некорректных значений по вертикали
        """
        try:
            board = t.Board(
                self.process("""
            X,   X,    X/17,X/90, X,  X
            X,   17/12,0,   0,    X/8,X
            14/X,0,    0,   0,    0,  X
            29/X,0,    0,   0,    0,  X
            X,   6/X,  0,   0,    X,  X
            X,   X,    X,   X,    X,  X""")).board
        except t.FormatException:
            board = None
        self.assertEqual(None, board)

    def test_incorrect_horizontal_data(self):
        """
        Тест, проверяющий работу алгоритма при вводе некорректных значений по горизонтали
        """
        try:
            board = t.Board(
                self.process("""
            X,   X,    X/17,X/29, X,  X
            X,   17/12,0,   0,    X/8,X
            14/X,0,    0,   0,    0,  X
            90/X,0,    0,   0,    0,  X
            X,   6/X,  0,   0,    X,  X
            X,   X,    X,   X,    X,  X""")).board
        except t.FormatException:
            board = None
        self.assertEqual(None, board)

    def test_no_answer(self):
        """
        Тест, проверяющий случай отсутствия ответа
        """
        field = t.Board(self.process("""
            X,   X,    X/18,X/29,X,  X
            X,   17/12,0,   0,   X/8,X
            14/X,0,    0,   0,   0,  X
            29/X,0,    0,   0,   0,  X
            X,   6/X,  0,   0,   X,  X
            X,   X,    X,   X,   X,  X
            """))
        excpected = set()
        answers = set(str(i) for i in s.start(
            field, 1, [[(1, 2), (2, 1)], [(3, 3)]]))
        self.assertSetEqual(answers, excpected)

    def test_filled_cells(self):
        """
        Тест, проверяющий правильность ответа при наличии фиксированных значений
        """
        field = t.Board(self.process("""
            X,  X,  X/7,X/6,X
            X,  4/4,0,  0,  X
            7/X,0,  0,  0,  X
            6/X,0,  0,  0,  X
            X,  X,  X,  X,  X
                        """))
        excpected = set()
        excpected.add("""X X X X X
X X 1 3 X
X 1 4 2 X
X 3 2 1 X
X X X X X""")

        answers = set(str(i) for i in s.start(field, 3, [[(1, 1)]]))
        self.assertSetEqual(answers, excpected)

    def test_filled_cells_no_answer(self):
        """
        Тест, проверяющий случай отсутствия ответа при наличии фиксированных значений
        """
        field = t.Board(self.process("""
            X,   X,   X/10,X/17,X,   X,  X
            X,   13/X,0,   0,   X/13,X/3,X
            X,   14/3,0,   0,   0,   0,  X
            4/X, 0,   0,   6/10,0,   0,  X
            11/X,0,   0,   0,   0,   X,  X
            X,   X,   8/X, 0,   0,   X,  X
            X,   X,   X,   X,   X,   X,  X
            """))
        excpected = set()

        answers = set(str(i) for i in s.start(
            field, 1, [[(3, 4), (4, 2)], [(5, 5)]]))
        self.assertSetEqual(answers, excpected)

    def test_find_incorrect_char_line(self):
        """
        Тест, проверяющий правильность определения строчки с некорректным символом
        """
        try:
            res = t.Board(
                self.process("""
            X,   X,    X/17,X/29, X,  X
            X,   17/12,0,   0,    X/8,X
            14/X,0,    0,   0,    0,  X
            29/X,0,    0,   0,    0,  X
            X,   6/X,  0,   0,    X,  X
            X,   X,    X,   X,    X,  A""")).board
        except t.FormatException as err:
            res = str(err).split(' ')[-1]
        self.assertEqual('6', res)

    def test_find_incorrect_value_line(self):
        """
        Тест, проверяющий правильность определения строчки с неправильным значением
        """
        try:
            res = t.Board(
                self.process("""
            X,   X,    X/17,X/29, X,  X
            X,   17/12,0,   0,    X/8,X
            14/X,0,    0,   0,    0,  X
            29/X,0,    0,   0,    0,  X
            X,   90/X,  0,   0,    X,  X
            X,   X,    X,   X,    X,  X""")).board
        except t.FormatException as err:
            res = str(err).split(' ')[-1]
        self.assertEqual('5', res)


if __name__ == '__main__':
    unittest.main()
