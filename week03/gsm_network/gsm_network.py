# python3

# import pycosat
import itertools

n, m = map(int, input().split())
edges = [ list(map(int, input().split())) for i in range(m) ]

# This solution prints a simple satisfiable formula
# and passes about half of the tests.
# Change this function to solve the problem.
def printEquisatisfiableSatFormula():
    list_formulas = [''] # first index will contain length
    var_map = {} # dict that will map all vars to the natural numbers.
    counter = 1
    # add in CNF for selecting exactly one color of the three possible for each vertex
    for vertex in range(1, n+1):
        vars = []
        for i in range(1,4):
            vertex_var = str(vertex) + str(i)
            var_map[vertex_var] = counter
            counter += 1
            vars.append(str(var_map[vertex_var]))
        list_formulas += exactly_one_of(vars)
    # add CNF that no two vertices have the same color
    for source, sink in edges:
        for i in range(1,4):
            source_var = str(source) + str(i)
            sink_var = str(sink) + str(i)
            list_formulas.append('-{} -{} 0'.format(var_map[source_var], var_map[sink_var]))
    list_formulas[0] = '{} {}'.format(len(list_formulas)-1, 3 * n) # all clauses are in list, and all vars are in the set
    print('\n'.join(list_formulas))
    # print(pycosat.solve(pycosat_input(list_formulas)))
    # print("3 2")
    # print("1 2 0")
    # print("-1 -2 0")
    # print("1 -2 0")

def exactly_one_of(iterable):
    """returns exactly one of iterable in CNF form as a list of strings."""
    new_iterable = []
    new_iterable.append(' '.join(iterable + ['0']))
    for var1, var2 in itertools.combinations(iterable, 2):
        new_iterable.append('-{} -{} 0'.format(var1, var2))
    return new_iterable

def pycosat_input(list_formulas):
    """ turns an array into pycosat input. """
    list_expressions = []
    list_expressions = [[int(i) for i in (formula[:-2].split(' '))] for formula in list_formulas[1:]]
    print(list_expressions)
    return list_expressions


printEquisatisfiableSatFormula()
