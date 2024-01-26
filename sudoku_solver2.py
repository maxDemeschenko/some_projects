import copy
import random

import numpy as np


tables = []


def sudoku_solver(table, required_number_of_solutions=100):
    global tables
    for i in range(9):
        for j in range(9):
            if table[i, j]:
                continue
            numbers = possible_numbers(table, i, j)
            if not numbers:
                return
            if len(numbers) == 1:
                table[i, j] = list(numbers)[0]

    for i in range(9):
        for j in range(9):
            if len(tables) >= required_number_of_solutions:
                return
            if table[i, j]:
                continue
            numbers = possible_numbers(table, i, j)
            for number in numbers:
                table[i, j] = number
                sudoku_solver(np.copy(table))
            return
        if i == 8:
            tables.append(table)
        if i == 8 and not len(tables) % 100:
            print(len(tables) // 100)


def place_first_numbers():
    table = np.reshape([0 for _ in range(81)], newshape=(9, 9))
    counter = 0
    while counter < 25:
        i = random.randint(0, 8)
        j = random.randint(0, 8)
        if table[i, j]:
            continue
        counter += 1
        numbers = possible_numbers(table, i, j)
        if not numbers:
            continue
        table[i, j] = random.choice(list(numbers))
    return table


def possible_numbers(table, i, j):
    banned_numbers = np.concatenate((table[i, :], table[:, j],
                                     np.reshape(table[i - i % 3:i - i % 3 + 3, j - j % 3:j - j % 3 + 3],
                                                newshape=9)))
    banned_numbers = set(banned_numbers)
    numbers = set([numb for numb in range(1, 10)])
    numbers -= banned_numbers
    return numbers


def create_sudoku_table():
    counter = 0
    global tables
    while not len(tables):
        counter += 1
        initial_table = place_first_numbers()
        sudoku_solver(initial_table, 5)
    return random.choice(tables).tolist()


def main():
    sudoku = [[9, 0, 0, 0, 0, 0, 0, 1, 0],
              [3, 0, 0, 9, 0, 0, 0, 8, 6],
              [0, 0, 2, 0, 0, 3, 0, 0, 0],
              [0, 7, 0, 0, 5, 0, 0, 0, 0],
              [2, 0, 0, 8, 0, 0, 0, 3, 9],
              [0, 0, 0, 0, 0, 0, 4, 0, 0],
              [0, 0, 5, 0, 8, 0, 0, 6, 4],
              [0, 0, 0, 4, 0, 0, 2, 0, 0],
              [6, 0, 0, 0, 0, 0, 1, 0, 0]]
    table = [0 for _ in range(81)]
    table = np.array(table)
    table = np.reshape(table, newshape=(9, 9))
    sudoku_solver(np.array(sudoku))
    global tables
    print(len(tables))
    print(tables[0])


def check_table_for_more_than_one_solution(table):
    global tables
    tables = []
    sudoku_solver(table, 1)
    if len(tables) == 2:
        return True
    return False


def unfilled_sudoku_table():
    result = create_sudoku_table()
    initial_table = copy.deepcopy(result)
    counter = 0
    while counter < 40:
        i = random.randint(0, 8)
        j = random.randint(0, 8)
        if not initial_table[i][j]:
            continue
        prev_value = initial_table[i][j]
        initial_table[i][j] = 0
        if check_table_for_more_than_one_solution(np.array(initial_table)):
            initial_table[i][j] = prev_value
            continue
        counter += 1
        global tables
        tables = []
    return initial_table, result


if __name__ == '__main__':
    init_t, res = unfilled_sudoku_table()
    print(init_t)
    print(res)
