from pathlib import Path


def extract_matrix():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    matrix = []

    with open(input_path.resolve(), "r") as file:
        for line in file:
            matrix.append([])
            for i in range(len(line) - 1):
                c = line[i]
                matrix[-1].append(c)
    return matrix


def search(matrix, word, i, j, m1, m2):
    n, m = len(matrix), len(matrix[0])
    new_row, new_col = i + m1, j + m2
    idx = 0
    while (
        0 <= new_row < n
        and 0 <= new_col < m
        and idx + 1 < len(word)
        and matrix[new_row][new_col] == word[idx + 1]
    ):
        idx += 1
        new_row += m1
        new_col += m2

    return 1 if idx == len(word) - 1 else 0


def calc_num_of_words(matrix, word):
    count = 0
    n, m = len(matrix), len(matrix[0])

    for i in range(n):
        for j in range(m):
            if matrix[i][j] == "X":
                # search right
                count += search(matrix, word, i, j, 0, 1)

                # search bottom
                count += search(matrix, word, i, j, 1, 0)

                # search left
                count += search(matrix, word, i, j, 0, -1)

                # search top
                count += search(matrix, word, i, j, -1, 0)

                # search top right diag
                count += search(matrix, word, i, j, -1, 1)

                # search bottom right diag
                count += search(matrix, word, i, j, 1, 1)

                # search bottom left diag
                count += search(matrix, word, i, j, 1, -1)

                # search top left diag
                count += search(matrix, word, i, j, -1, -1)
    return count


def calc_number_x_mas(matrix):
    count = 0
    n, m = len(matrix), len(matrix[0])

    for i in range(n):
        for j in range(m):
            if matrix[i][j] == "A":
                top_left_diag = (i - 1, j - 1)
                top_right_diag = (i - 1, j + 1)
                bottom_left_diag = (i + 1, j - 1)
                bottom_right_diag = (i + 1, j + 1)

                # Check out of bounds
                if (
                    top_left_diag[0] < 0
                    or top_left_diag[0] >= n
                    or top_left_diag[1] < 0
                    or top_left_diag[1] >= m
                    or top_right_diag[0] < 0
                    or top_right_diag[0] >= n
                    or top_right_diag[1] < 0
                    or top_right_diag[1] >= m
                    or bottom_left_diag[0] < 0
                    or bottom_left_diag[0] >= n
                    or bottom_left_diag[1] < 0
                    or bottom_left_diag[1] >= m
                    or bottom_right_diag[0] < 0
                    or bottom_right_diag[0] >= n
                    or bottom_right_diag[1] < 0
                    or bottom_right_diag[1] >= m
                ):
                    continue

                if (
                    (
                        matrix[top_left_diag[0]][top_left_diag[1]] == "M"
                        and matrix[bottom_right_diag[0]][bottom_right_diag[1]] == "S"
                    )
                    or (
                        matrix[top_left_diag[0]][top_left_diag[1]] == "S"
                        and matrix[bottom_right_diag[0]][bottom_right_diag[1]] == "M"
                    )
                ) and (
                    (
                        matrix[top_right_diag[0]][top_right_diag[1]] == "M"
                        and matrix[bottom_left_diag[0]][bottom_left_diag[1]] == "S"
                    )
                    or (
                        matrix[top_right_diag[0]][top_right_diag[1]] == "S"
                        and matrix[bottom_left_diag[0]][bottom_left_diag[1]] == "M"
                    )
                ):
                    count += 1
    return count


def main():
    matrix = extract_matrix()
    num_of_xmas = calc_num_of_words(matrix, "XMAS")
    num_of_x_mas_in_cross_format = calc_number_x_mas(matrix)

    print(f"Number of times the word XMAS appears -> {num_of_xmas}")
    print(
        f"Number of times the word X-MAS appears as a cross -> {num_of_x_mas_in_cross_format}"
    )


main()
