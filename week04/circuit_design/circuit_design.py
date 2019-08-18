# python3

import itertools

n, m = map(int, input().split())
clauses = [ list(map(int, input().split())) for i in range(m) ]
# may need to add CNFs here
# print(n,m,clauses)

class Vertex:
    def __init__(self,u):
        self.index = u
        self.out_neighbors = [] # vertices that can be traversed in the forward direction (u -> v)
        self.in_neighbors = [] # vertices that can be traversed in the backward direction (t -> u)

# This solution tries all possible 2^n variable assignments.
# It is too slow to pass the problem.
# Implement a more efficient algorithm here.
def isSatisfiable():
    graph = construct_implication_graph(clauses)
    # print(graph)
    # print([(v.index, v.out_neighbors) for v in graph.values()])
    find_SCCs(graph)

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
        # graph[i] = []
        # graph[-i] = []
        graph[i] = Vertex(i)
        graph[-i] = Vertex(-i)
    for clause in clauses:
        u = clause[0]
        if len(clause) == 1:
            # graph.append([-clause[0], clause[0]])
            graph[-u].out_neighbors.append(u)
            graph[u].in_neighbors.append(-u)
            # graph[-u].append(u)
        elif len(clause) == 2:
            v = clause[1]
            # print(u,v)
            # graph.append([-clause[0], clause[1]])
            # graph.append([-clause[1], clause[0]])
            graph[-u].out_neighbors.append(v)
            graph[v].in_neighbors.append(-u)
            graph[-v].out_neighbors.append(u)
            graph[u].in_neighbors.append(-v)
    return graph

def find_SCCs(graph):
    """ uses Kosaraju's Algorithm to generate the SCCs. """
    explored = set()
    L = [] #list that stores traversals
    # visit each vertex via dfs
    for vertex in graph.keys():
        visit(graph, vertex, explored, L)
    print(L)
    # now assign values to root, forming SCCs
    for vertex in L:
        assign(vertex)


def visit(graph, u, explored, L):
    # print(explored, u, u not in explored)
    # print()
    if u not in explored:
        explored.add(u)
        L.insert(0, u)
        for v in graph[u].out_neighbors:
            # print(v, v not in explored, explored)
            visit(graph, v, explored, L)

def assign(vertex):
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
