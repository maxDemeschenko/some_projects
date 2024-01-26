import numpy as np

sudoku = [[1, 0, 0, 0, 2, 0, 0, 5, 0],
          [0, 3, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 7, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 9, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 0, 0]]


def solve(table):
    for i in range(9):
        for j in range(9):
            if table[i][j]:
                continue
            banned_numbers = table[i] + np.array(table)[:, j].tolist()
            banned_numbers = set(banned_numbers)
            numbers = set([numb for numb in range(1, 10)])
            numbers -= banned_numbers
            if not numbers:
                # return table
                return np.array(table)
            for number in numbers:
                table1 = table.copy()
                table1[i][j] = number
                if i == 8 and j == 8:
                    print(np.array(table))
                solve(table1)


if __name__ == '__main__':
    # zeroes = np.reshape(np.zeros(81), newshape=[9, 9])
    # for zero1 in zeroes:
    #     for zero in zero1:
    #         zero = int(zero)
    # print(zeroes)

    print(solve(sudoku))
