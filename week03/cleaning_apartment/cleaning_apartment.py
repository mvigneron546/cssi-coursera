# python3

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
    vars = []

    # all nodes appear on path
    for vertex in range(1, n+1):
        for position in range(1, n+1):
            vertex_var = str(vertex) * 2 + str(position)
            var_map[vertex_var] = counter
            counter += 1
            vars.append(str(var_map[vertex_var]))
    list_formulas.append(' '.join(vars + ['0']))

    # add CNF for each vertex must occupy only one position; also takes into account that all vars need to occupy positions
    # CNF: exactly_one_of([xij]) where j = 1,2,3,...n
    for pos1, pos2 in itertools.combinations([pos for pos in range(1,n+1)], 2):
        for vertex in range(1, n+1):
            vertex_var = str(vertex) * 2 + str(pos1)
            # print(vertex_var)
            adjacent_var = str(vertex) * 2 + str(pos2)
            # print(adjacent_var)
            list_formulas.append('-{} -{} 0'.format(var_map[vertex_var], var_map[adjacent_var]))

    # for vertex in range(1, n+1):
    #     for position in range(1, n+1):
    #         vertex_var = str(vertex) * 2 + str(position)
    #         vars.append(str(var_map[vertex_var]))
    #     list_formulas += exactly_one_of(vars)

    # add in CNF for no two vertices can occupy the same position
    # CNF: exactly_one_of([xij]) where i = 1,2,3...n
    for position in range(1, n+1):
        same_position_vertices = [str(var_map[str(vertex) * 2 + str(position)]) for vertex in range(1, n+1)]
        list_formulas += exactly_one_of(same_position_vertices)

    # for vertex1 in range(1, n+1):
    #     for vertex2 in range(1, n+1):
    #         if [vertex1, vertex2] not in edges and [vertex2, vertex1] not in edges and vertex1 != vertex2:
    #             for i in range(1, n):
    #                 vertex_var = str(vertex1) * 2 + str(i)
    #                 adjacent_var = str(vertex2) * 2 + str(i+1)
    #                 list_formulas.append('-{} -{} 0'.format(var_map[vertex_var], var_map[adjacent_var]))

    # add CNF that all vertices in a possible path must be connected by an edge
    # CNF: (-xik V -xjk+1) if (k, k+1) not in E
    for vertex1, vertex2 in itertools.combinations([vertex for vertex in range(1,n+1)], 2):
        if [vertex1, vertex2] not in edges and [vertex2, vertex1] not in edges:
            for i in range(1, n):
                vertex_var = str(vertex1) * 2 + str(i)
                adjacent_var = str(vertex2) * 2 + str(i+1)
                list_formulas.append('-{} -{} 0'.format(var_map[vertex_var], var_map[adjacent_var]))
                # also add a CNF with positions swapped. potential SAT optimization here
                vertex_var = str(vertex1) * 2 + str(i+1)
                adjacent_var = str(vertex2) * 2 + str(i)
                list_formulas.append('-{} -{} 0'.format(var_map[vertex_var], var_map[adjacent_var]))

    list_formulas[0] = '{} {}'.format(len(list_formulas)-1, len(var_map)) # all clauses are in list, and all vars are in the set
    # if n == 30 and m == 80:
        # list_formulas = ['1 1', '1 0']
    print('\n'.join(list_formulas))
    # print(var_map, len(var_map))
    # sat_solve(list_formulas)
    # write_file(list_formulas)

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

def sat_solve(list_formulas):
    """uses pycosat to solve for a CNF. Used for testing purposes."""
    import pycosat
    solve = pycosat.solve(pycosat_input(list_formulas))
    if type(solve) == list:
        print(list(filter(lambda x: x > 0, solve)))
    else:
        print(solve)

def write_file(list_formulas):
    """writes output to a file."""
    f = open('output.cnf', 'w')
    f.write('\n'.join(list_formulas))
    f.close()

printEquisatisfiableSatFormula()
