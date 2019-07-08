# python3
from sys import stdin

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
        # print(pivot_element.row, pivot_element.column)
        pivot_element.column += 1
        if pivot_element.column >= len(used_columns):
            return Position(-1,-1)
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
        if pivot_element.row == -1 and pivot_element.column == -1:
            return None
        # SwapLines(a, b, used_rows, pivot_element)
        ProcessPivotElement(a, b, pivot_element)
        MarkPivotElementUsed(pivot_element, used_rows, used_columns)
    return b

def combo(param_list, integer, list_active=False):
    """
    finds all possible combinations of sets of len integer; performs deepcopy if needed
    Note: copies are modified
    """
    if list_active:
        param_list = param_list[:]
    temp_list = []
    return_list = []
    if integer < 1:
        raise ValueError('Invalid value!')
    if integer == 1 and list_active:
        return [[param[:]] for param in param_list]
    elif integer == 1:
        return [[param] for param in param_list]
    while integer <= len(param_list):
        temp_list = param_list[:integer - 1]
        if list_active:
            temp_list = [temp[:] for temp in temp_list]
        # print(temp_list)
        length = len(param_list)
        element = integer - 1
        while element < length:
            if list_active:
                temp_list.append(param_list[element][:])
                # print(temp_list)
                return_list.append(temp_list)
                temp_list = [param[:] for param in param_list[:integer-1]]
            else:
                temp_list.append(param_list[element])
                # print(temp_list)
                return_list.append(temp_list)
                temp_list = param_list[:integer-1]
            element += 1
        param_list.pop(0)
    return return_list

def generate_all_subsets(A,b):
    equations = []
    # print(A,b,m)
    a_sets = combo(A[:], m, True)
    b_sets = combo(b[:], m)
    # print(b)
    for i in range(len(a_sets)):
        # print('System:', a_sets[i], b_sets[i])
        equations.append(Equation(a_sets[i],b_sets[i]))
    # print(equations)
    return equations

def check_solutions(m,A,b,equation,solns):
    """ checks solutions for validity. returns 1 if valid, 0 if not, and -1 if infinite. """
    total = 0
    for equation_index in range(len(A)):
        for index in range(m):
            total += A[equation_index][index] * solns[index]
        # print(b, equation_index)
        if total > b[equation_index]:
            return False
        total = 0
    if 10 ** 9 in equation.b:
        return -1
    return True

def possible_infinity(n,m,A,b,c):
    """
    Checks to see if there are any cases where there are no limits on variables.
    Returns True if the following occurs:
    - All coefficients for a specific column are 0.
    - The corresponding column in c > 0.
    False otherwise.
    """
    coefficient_present = False
    for row in range(len(A)):
        for column in range(m):
            if A[row][column] == 0:
                for second_row in range(row+1,n):
                    if A[second_row][column] > 0:
                        coefficient_present = True
                        break
                if not coefficient_present and c[column] > 0:
                    return True
    return False

def solve_diet_problem(n, m, A, b, c):
    # Write your code here
    soln_set = [0 * m]
    # print(b)
    # if there are more foods than there are restrictions, there may be a possible infinity
    if m > n:
        if possible_infinity(n,m,A,b,c):
            return [1,soln_set]
    equations = generate_all_subsets(A,b)
    solutions = []
    # only put in viable solutions. If there aren't any, then the problem has no solution
    for equation in equations:
        # print([(eq.a, eq.b) for eq in equations])
        solns = SolveEquation(equation)
        # print('Solution:', solns)
        if solns:
            possible_negatives = [True if num >= 0 else False for num in solns]
            if False not in possible_negatives:
                indicator = check_solutions(m,A,b,equation,solns)
                if indicator == 1:
                    solutions.append(solns)
                elif indicator == -1:
                    return [1, soln_set]
    # print(solutions)
    if not solutions:
        return [-1, soln_set]
    # now try all possible combos of solutions that pass through all inequalities. If a metric in c is negative, use 0 instead.
    rolling_total = 0
    total = 0
    # print(A,b)
    # if the "true length", meaning the length without the 10^9 inequality is added in, then fulfill this cond
    if len(A)-1 == 1 and len(b)-1 == 1:
        # print('f')
        if c[0] > 0:
            rolling_total = solutions[0] * c[0]
            soln_set = solutions[0]
        return [0, soln_set]
    for solution in solutions:
        # print(solution)
        for i in range(m):
            # if other options in that inequality exist, use them
            if c[i] < 0 and len(A[0]) > 1:
                solution[i] = 0
            total += solution[i] * c[i]
        # for negatives that have no choice
        if total > rolling_total or (len(A[0]) == 1 and rolling_total == 0):
            rolling_total = total
            soln_set = solution
        total = 0
    return [0, soln_set]

n, m = list(map(int, stdin.readline().split()))
A = []
for i in range(n):
  A += [list(map(int, stdin.readline().split()))]
A.append([1 for i in range(m)])
b = list(map(int, stdin.readline().split()))
b.append(10 ** 9)
c = list(map(int, stdin.readline().split()))
# print(A,b,c)

anst, ansx = solve_diet_problem(n, m, A, b, c)

if anst == -1:
  print("No solution")
if anst == 0:
  print("Bounded solution")
  print(' '.join(list(map(lambda x : '%.18f' % x, ansx))))
if anst == 1:
  print("Infinity")
