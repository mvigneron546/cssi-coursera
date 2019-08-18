# python3

import itertools

n, m = map(int, input().split())
clauses = [ list(map(int, input().split())) for i in range(m) ]
# may need to add CNFs here
# print(n,m,clauses)

# This solution tries all possible 2^n variable assignments.
# It is too slow to pass the problem.
# Implement a more efficient algorithm here.
def isSatisfiable():
    graph = construct_implication_graph(clauses)
    print(graph)

    for mask in range(1<<n):
        result = [ (mask >> i) & 1 for i in range(n) ]
        # print(mask, result)
        formulaIsSatisfied = True
        for clause in clauses:
            clauseIsSatisfied = False
            if result[abs(clause[0]) - 1] == (clause[0] < 0):
                clauseIsSatisfied = True
            if result[abs(clause[1]) - 1] == (clause[1] < 0):
                clauseIsSatisfied = True
            if not clauseIsSatisfied:
                formulaIsSatisfied = False
                break
        if formulaIsSatisfied:
            return result
    return None

def construct_implication_graph(clauses):
    """
    constructs implication graph in the form of u -> v for clauses.
    returns a list of sublists where sublist [u,v] == u -> v
    """
    graph = {} # u -> v stored as [u,v]
    for i in range(1,n+1):
        graph[i] = []
        graph[-i] = []
    for clause in clauses:
        u = clause[0]
        if len(clause) == 1:
            # graph.append([-clause[0], clause[0]])
            graph[-u].append(u)
        elif len(clause) == 2:
            v = clause[1]
            print(u,v)
            # graph.append([-clause[0], clause[1]])
            # graph.append([-clause[1], clause[0]])
            graph[-u].append(v)
            graph[-v].append(u)
    return graph

def find_SCCs(graph):
    pass

# def dfs(graph, vertex, explored=None):
#     if not explored:
#         explored = set()
#     if vertex not in explored:
#         explored.add(vertex)
#         for v in graph[vertex]:
#             dfs(graph, v, explored)




result = isSatisfiable()
if result is None:
    print("UNSATISFIABLE")
else:
    print("SATISFIABLE");
    print(" ".join(str(-i-1 if result[i] else i+1) for i in range(n)))
