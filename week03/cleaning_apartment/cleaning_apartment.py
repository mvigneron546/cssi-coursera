# python3

import pycosat
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

    # CNF for each vertex being part of the path
    # CNF: (x11 V x21 V ...) (x21 V x22 V ...) ...
    for vertex in range(1, n+1):
        vars = []
        for position in range(1, n+1):
            vertex_var = str(vertex) + str(position)
            var_map[vertex_var] = counter
            counter += 1
            vars.append(str(var_map[vertex_var]))
        list_formulas.append(' '.join(vars + ['0']))

    # add CNF for each vertex must occupy only one position
    # CNF: exactly_one_of([x11, x12, ...])
    for vertex in range(1, n+1):
        same_vertex_positions = [str(var_map[str(vertex) + str(position)]) for position in range(1, n+1)]
        list_formulas += exactly_one_of(same_vertex_positions)

    # add in CNF for no two vertices can occupy the same position
    # CNF: (-x11 V -x21 V ...) (-x12 V -x22 V ...) ...
    for position in range(1, n+1):
        same_position_vertices = [str(var_map[str(vertex) + str(position)]) for vertex in range(1, n+1)]
        list_formulas += exactly_one_of(same_position_vertices)

    # # add in CNF for selecting exactly one path of the m possible for each vertex
    # for vertex in range(1, n+1):
    #     vars = []
    #     for position in range(1, m+1):
    #         vertex_var = str(vertex) + str(position)
    #         var_map[vertex_var] = counter
    #         counter += 1
    #         vars.append(str(var_map[vertex_var]))
    #         list_formulas.append('-{} -{} 0'.format(var_map[vertex_var], var_map[adjacent_var]))

    # # CNF for there must be a vertex per position
    # for position in range(1, m+1):
    #     same_position_vertices = [str(var_map[str(vertex) + str(position)]) for vertex in range(1, n+1)]
    #     list_formulas.append(' '.join(same_position_vertices + ['0']))
    #     # list_formulas += exactly_one_of(same_position_vertices)
    #
    # # add CNF that no two vertices have the same color
    # for source, sink in edges:
    #     for i in range(1, m+1):
    #         source_var = str(source) + str(i)
    #         sink_var = str(sink) + str(i)
    #         list_formulas.append('-{} -{} 0'.format(var_map[source_var], var_map[sink_var]))

    # add CNF that all vertices in a possible path must be connected by an edge
    # CNF: (-xik V -xjk+1) if (k, k+1) not in E
    for vertex1, vertex2 in itertools.combinations([vertex for vertex in range(1,n+1)], 2):
        if [vertex1, vertex2] not in edges:
            for i in range(1, n):
                vertex_var = str(vertex1) + str(i)
                adjacent_var = str(vertex2) + str(i+1)
                list_formulas.append('-{} -{} 0'.format(var_map[vertex_var], var_map[adjacent_var]))

    list_formulas[0] = '{} {}'.format(len(list_formulas)-1, m * n) # all clauses are in list, and all vars are in the set
    print('\n'.join(list_formulas))
    print(var_map)
    print(pycosat.solve(pycosat_input(list_formulas)))

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
    return list_expressions


printEquisatisfiableSatFormula()
