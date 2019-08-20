# python3

import itertools
import sys
import threading

# This code is used to avoid stack overflow issues
sys.setrecursionlimit(10**6) # max depth of recursion
threading.stack_size(2**26)  # new thread will get stack of such size

n, m = map(int, input().split())
clauses = [ list(map(int, input().split())) for i in range(m) ]
# may need to add CNFs here
# print(n,m,clauses)

class Vertex:
    def __init__(self,u):
        self.index = u
        self.value = -1 # the value the vertex becomes in the CNF when satisfied
        self.out_neighbors = [] # vertices that can be traversed in the forward direction (u -> v)
        self.in_neighbors = [] # vertices that can be traversed in the backward direction (t -> u)
        self.scc = set() # will hold the set of the strongly connected components this vertex is part of
        self.root = False # will determine if this is the root of the SCC
        # tarjan-specific variables
        self.lowlink = -1 # smallest discovered vertex reachable from this one
        self.discovered = -1 # when it was discovered
        self.on_stack = False

def isSatisfiable():
    graph = construct_implication_graph(clauses)
    # print(graph)
    # print([(v.index, v.out_neighbors, v.in_neighbors) for v in graph.values()])
    roots = find_SCCs(graph, tarjans)
    # roots = find_SCCs(graph, kosaraju)[::-1]
    # print(roots, {root: graph[root].scc for root in roots})
    for vertex in roots:
        if -vertex in graph[vertex].scc:
            return None
        # also check that components and their inverses aren't in the scc
        for literal in graph[vertex].scc:
            if -literal in graph[vertex].scc:
                return None
    # as roots contains the reverse topological order of the sccs, just go backwards and fill solns
    result = [None] * n
    for scc_root in roots:
        # print(graph[scc_root].scc)
        for literal in graph[scc_root].scc:
            if graph[literal].value == -1:
                graph[literal].value = 1
                # print(literal)
                result[abs(literal) - 1] = literal
                # print(result)
                graph[-literal].value = 0
    # print(result)
    return result

def construct_implication_graph(clauses):
    """
    constructs implication graph in the form of u -> v for clauses.
    returns a dict of vertices in the form {index : Vertex(index)}
    see Vertex object for further info
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

def find_SCCs(graph, function):
    """ uses either Kosaraju's or Tarjan's to find SCCs. """
    return function(graph)

def kosaraju(graph):
    """ uses Kosaraju's Algorithm to generate the SCCs. returns a list of vertex roots of the SCCs. potentially bugged as it didn't pass. """
    L = [] #list that stores traversals
    explored = set()
    # visit each vertex via dfs
    for vertex in graph.keys():
        visit(vertex, graph, explored, L)
    # print(L)
    # now assign values to root, forming SCCs
    assigned = set()
    roots = [] # stores roots of SCCs in topological order
    for vertex in L:
        assign(vertex, vertex, graph, assigned, roots)

    # scc_roots_graph = { vertex : graph[vertex] for vertex in graph.keys() if graph[vertex].root }
    # print({vertex : graph[vertex].scc for vertex in scc_roots_graph.keys()}, {vertex : graph[vertex].out_neighbors for vertex in graph.keys()})
    # print(roots)
    return roots

def tarjans(graph):
    """ uses Tarjan's Algorithm to generate the SCCs. returns a list of roots in reverse topological order. """
    index = 0
    stack = []
    roots = []
    for vertex in graph.keys():
        if graph[vertex].discovered == -1:
            strongconnect(graph[vertex], stack, index, graph, roots)
            # print(stack, roots)
    return roots

def strongconnect(vertex, stack, index, graph, roots):
    """ Helper for Tarjan's. Generates the SCCs. vertex input is the Vertex object. """
    vertex.discovered = index
    vertex.lowlink = index
    index += 1
    stack.append(vertex)
    vertex.on_stack = True

    # dfs
    for out_vertex_index in vertex.out_neighbors:
        if graph[out_vertex_index].discovered == -1:
            # not visited; recurse
            strongconnect(graph[out_vertex_index], stack, index, graph, roots)
            vertex.lowlink = min(vertex.lowlink, graph[out_vertex_index].lowlink)
        elif graph[out_vertex_index].on_stack:
            # the vertex is on the stack; back edge case
            # the out_vertex is the root
            vertex.lowlink = min(vertex.lowlink, graph[out_vertex_index].discovered)

    # generate the SCC if conditions are correct
    if vertex.discovered == vertex.lowlink:
        # print(vertex.index)
        # print(vertex.index, [v.index for v in stack])
        # popped_vertex = False
        while len(stack) != 0:
            v = stack.pop(-1)
            vertex.scc.add(v.index)
            v.on_stack = False
            # pop the stack only up and including the current root
            if v == vertex:
                break
        # while vertex != v
        roots.append(vertex.index)

def visit(u, graph, explored, L):
    """
    visits all vertices via dfs
    prepends them to a list L (to keep v from appearing from u) for further processing
    """
    # print(explored, u, u not in explored)
    # print()
    if u not in explored:
        explored.add(u)
        L.insert(0, u)
        for v in graph[u].out_neighbors:
            # print(v, v not in explored, explored)
            visit(v, graph, explored, L)

def assign(u, root, graph, assigned, roots):
    """ assigns all vertices to a SCC via dfs """
    if u not in assigned:
        graph[root].scc.add(u)
        assigned.add(u)
        if u == root:
            graph[u].root = True
            roots.append(u)
        for v in graph[u].in_neighbors:
            assign(v, root, graph, assigned, roots)

def main():
    result = isSatisfiable()
    if result is None:
        print("UNSATISFIABLE")
    else:
        print("SATISFIABLE");
        # print(" ".join(str(-i-1 if result[i] else i+1) for i in range(n)))
        print(" ".join([str(i) for i in result]))

threading.Thread(target=main).start()
