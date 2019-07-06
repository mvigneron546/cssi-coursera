# python3

EPS = 1e-6
PRECISION = 20

class Equation:
    def __init__(self, a, b):
        self.a = a
        self.b = b

class Position:
    def __init__(self, column, row):
        self.column = column
        self.row = row

def ReadEquation():
    size = int(input())
    a = []
    b = []
    for row in range(size):
        line = list(map(float, input().split()))
        a.append(line[:size])
        b.append(line[size])
    # print(a,b)
    return Equation(a, b)

def SelectPivotElement(a, used_rows, used_columns):
    # This algorithm selects the first free element.
    # You'll need to improve it to pass the problem.
    # edge case where selected # is 0
    pivot_element = Position(0, 0)
    while used_rows[pivot_element.row]:
        pivot_element.row += 1
    while used_columns[pivot_element.column] or a[pivot_element.row][pivot_element.column] == 0:
        pivot_element.column += 1
    # print('Element Selected:', a[pivot_element.row][pivot_element.column] )
    return pivot_element

def SwapLines(a, b, used_rows, pivot_element):
    # swap to the top, using column and row as indicators
    # print('Before swap:',a,b,pivot_element.row,pivot_element.column)
    a[pivot_element.column], a[pivot_element.row] = a[pivot_element.row], a[pivot_element.column]
    b[pivot_element.column], b[pivot_element.row] = b[pivot_element.row], b[pivot_element.column]
    used_rows[pivot_element.column], used_rows[pivot_element.row] = used_rows[pivot_element.row], used_rows[pivot_element.column]
    pivot_element.row = pivot_element.column
    # print('After swap:',a,b,pivot_element.row,pivot_element.column)

def ProcessPivotElement(a, b, pivot_element):
    # Write your code here
    scale_factor = a[pivot_element.row][pivot_element.column]
    # print(pivot_element.row, pivot_element.column, scale_factor, a, b)
    if scale_factor != 1:
        for i in range(len(a[pivot_element.row])):
            a[pivot_element.row][i] /= scale_factor
        b[pivot_element.row] /= scale_factor
    # for all equations in the thing, if u aint 1, then u get the subtracc
    for i in range(len(a)):
        if i != pivot_element.row:
            # only do subtracting when elements exist in the same col as pivot
            if a[i][pivot_element.column] != 0:
                factor = a[i][pivot_element.column] if a[i][pivot_element.column] != 1 else None
                if factor:
                    for col_index in range(len(a[i])):
                        a[i][col_index] -= factor * a[pivot_element.row][col_index]
                    b[i] -= factor * b[pivot_element.row]
                else:
                    for col_index in range(len(a[i])):
                        a[i][col_index] -= a[pivot_element.row][col_index]
                    b[i] -= b[pivot_element.row]
    # print('After all ops:', a, b)

def MarkPivotElementUsed(pivot_element, used_rows, used_columns):
    used_rows[pivot_element.row] = True
    used_columns[pivot_element.column] = True

def SolveEquation(equation):
    a = equation.a
    b = equation.b
    size = len(a)

    used_columns = [False] * size
    used_rows = [False] * size
    for step in range(size):
        pivot_element = SelectPivotElement(a, used_rows, used_columns)
        SwapLines(a, b, used_rows, pivot_element)
        ProcessPivotElement(a, b, pivot_element)
        MarkPivotElementUsed(pivot_element, used_rows, used_columns)

    return b

def PrintColumn(column):
    size = len(column)
    for row in range(size):
        print("%.20lf" % column[row])

if __name__ == "__main__":
    equation = ReadEquation()
    solution = SolveEquation(equation)
    # SwapLines(equation.a, equation.b, )
    PrintColumn(solution)
    exit(0)
