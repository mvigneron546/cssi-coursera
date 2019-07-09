# python3
from sys import stdin

class Equation:
    def __init__(self, a, b):
        self.a = [ele[:] for ele in a]
        self.b = b[:]
        self.orig_b = b[:]
        self.orig_a = [ele[:] for ele in a]

class Position:
    def __init__(self, column, row):
        self.column = column
        self.row = row

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
    # print('Element Selected:', pivot_element.row, pivot_element.column, )
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
                # print(a,b)

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
    # print(len(param_list), integer)

    def generate_subsets(param_list):
        if len(param_list) == 1:
            return [[param_list[0]],[]]
        current_subset = generate_subsets(param_list[1:])
        new_subset = current_subset[:]
        returned_list = []
        for i in range(len(new_subset)):
            new_subset[i] = new_subset[i][:]
            new_subset[i].append(param_list[0])
        returned_list += current_subset
        returned_list += new_subset
        return returned_list

    returned_list = []
    subsets = generate_subsets(param_list)
    for subset in subsets:
        if len(subset) == integer:
            if list_active:
                for i in range(len(subset)):
                    subset[i] = subset[i][:]
                returned_list.append(subset)
            else:
                returned_list.append(subset)
    return returned_list

def generate_all_subsets(A,b):
    equations = []
    a_sets = combo(A[:], m, True)
    b_sets = combo(b[:], m)
    for i in range(len(a_sets)):
        equations.append(Equation(a_sets[i],b_sets[i]))
        # equations.append(Equation(a_sets[i], [ eq_const[tuple(a)] for a in a_sets[i]]))
    return equations

def check_solutions(m,A,b,solns):
    """ checks solutions for validity. returns True if valid, else False. """
    epsilon = 10 ** -3
    total = 0
    for equation_index in range(len(A)):
        for index in range(m):
            total += A[equation_index][index] * solns[index]
        if A[equation_index].count(1) == 1 and b[equation_index] == 0:
                if total < b[equation_index]:
                    return False
        elif total > b[equation_index] + epsilon:
            return False
        total = 0
    # print()
    return True

def possible_infinity(m,A,c):
    """
    Checks to see if there are any cases where there are no limits on variables.
    Returns True if the following occurs:
    - All coefficients for a specific column are 0.
    - The corresponding column in c > 0.
    False otherwise.
    """
    coefficient_present = False
    for row in range(len(orig_A)):
        for column in range(m):
            if orig_A[row][column] == 0:
                # print(row,column)
                for second_row in range(row,len(orig_A)):
                    # print(second_row, column, orig_A[second_row][column])
                    if orig_A[second_row][column] > 0:
                        coefficient_present = True
                        break
                if not coefficient_present and c[column] > 0:
                    return True
            # coefficient_present = False
    return False

def soln_rearrange(equation):
    """
    Creates a list in which the index corresponds to the column #.
    Uses equation.a and equation.b as the matrix and soln, respectively.
    """
    a = equation.a
    b = equation.b
    return_list = [0 for i in range(len(b))]
    for row in range(len(a)):
        # print(a[row])
        for column in range(len(a[0])):
            if a[row][column] == 1:
                # print(row,column)
                return_list[column] = b[row]
    equation.b = return_list
    return return_list

def solve_diet_problem(n, m, A, b, c):
    # Write your code here
    soln_set = [0 for num in range(m)]
    cur_eq = None
    rolling_total = None
    total = 0
    # case where pleasure factors are 0; no need to go any further
    if c.count(0) == len(c):
        return [0, soln_set]
    # if there are more foods than there are restrictions, there may be a possible infinity
    if m > n:
        if possible_infinity(m,A,c):
            return [1,soln_set]
    equations = generate_all_subsets(A,b)
    # print([(equation.a, equation.b) for equation in equations])
    # print()
    solutions = []
    # only put in viable solutions. If there aren't any, then the problem has no solution
    for equation in equations:
        # print()
        # print(equation.a, equation.b)
        solns = SolveEquation(equation)
        # print('Solution:', solns, equation.a, equation.b)
        # print()
        if solns:
            # rearrange the solution list so that it matches up with the rest of the matrix
            solns = soln_rearrange(equation)
            # print(solns)
            # print('After rearranging:',solns, equation.a)
            # print()
            if check_solutions(m,A,b,solns):
                solutions.append(solns)
                # print(solns, equation.orig_a, equation.orig_b)
                for i in range(m):
                    total += solns[i] * c[i]
                if rolling_total == None:
                    rolling_total = total
                    soln_set = solns
                    cur_eq = equation
                if total > rolling_total:
                    rolling_total = total
                    soln_set = solns
                    cur_eq = equation
                elif total == rolling_total and 10 ** 9 in cur_eq.orig_b:
                    rolling_total = total
                    soln_set = solns
                    cur_eq = equation
                total = 0
    if not solutions:
        return [-1, soln_set]
    for equation in equations:
        if equation.b == soln_set and 10 ** 9 in equation.orig_b:
            # print(equation.b, equation.orig_b)
            return [1, soln_set]
    return [0, soln_set]

n, m = list(map(int, stdin.readline().split()))
A = []
zero_list = [0 for i in range(m)]
for i in range(n):
  A += [list(map(int, stdin.readline().split()))]
b = list(map(int, stdin.readline().split()))
orig_A = A[:]
orig_B = b[:]
for i in range(m):
    A.append([0 for num in range(i)] + [1] + [0 for num in range(i+1,m)])
    b.append(0)
# A.append([0,1,0])
# b.append(0)
A.append([1 for i in range(m)])
b.append(10 ** 9)
# print(A,b)
# print()
eq_const = {tuple(A[i]):b[i] for i in range(len(A))}
# print(eq_const)
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
