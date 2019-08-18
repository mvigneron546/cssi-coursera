# python3
from itertools import permutations
INF = 10 ** 9

class Graph:
    def __init__(self, graph):
        self.graph = graph
        self.best_weight = INF
        self.best_path = []

def read_data():
    n, m = map(int, input().split())
    graph = [[INF] * n for _ in range(n)]
    for _ in range(m):
        u, v, weight = map(int, input().split())
        u -= 1
        v -= 1
        graph[u][v] = graph[v][u] = weight
    # print(graph)
    return Graph(graph)

def print_answer(path_weight, path):
    print(path_weight)
    if path_weight == -1:
        return
    print(' '.join(map(str, path)))

def optimal_path(graph):
    # This solution tries all the possible sequences of stops.
    # It is too slow to pass the problem.
    # Implement a more efficient algorithm here.
    n = len(graph.graph)
    best_ans = INF
    best_path = []

    find_optimal_path(graph, 0, 0, set(), 0, [])
    # for p in permutations(range(n)):
    #     cur_sum = 0
    #     for i in range(1, n):
    #         if graph[p[i - 1]][p[i]] == INF:
    #             break
    #         cur_sum += graph[p[i - 1]][p[i]]
    #     else:
    #         if graph[p[-1]][p[0]] == INF:
    #             continue
    #         cur_sum += graph[p[-1]][p[0]]
    #         if cur_sum < best_ans:
    #             best_ans = cur_sum
    #             best_path = list(p)
    #
    if graph.best_weight == INF:
        return (-1, [])
    return (graph.best_weight, [x + 1 for x in graph.best_path])

def find_optimal_path(graph, from_vertex, to_vertex, explored, cur_weight, cur_path):
    """ solves TSPs using the branch and bound technique. Unfortunately still too slow. """
    if from_vertex != to_vertex:
        cur_weight += graph.graph[from_vertex][to_vertex]
    explored.add(to_vertex)
    cur_path.append(to_vertex)
    # print(from_vertex, to_vertex, explored)
    # if the rest of the graph has been explored and a path exists to the initial vertex, compute the rest of soln
    if len(explored) == len(graph.graph) and graph.graph[to_vertex][0] != INF:
        cur_weight += graph.graph[to_vertex][0]
        if cur_weight < graph.best_weight:
            graph.best_weight = cur_weight
            graph.best_path = cur_path
            return
    # prune the branch if it already exceeds the current best solution
    if cur_weight > graph.best_weight:
        return
    # otherwise explore all unexplored vertices; keep the vertex positions for bookkeeping
    weights_list = [i for i in range(len(graph.graph)) if i not in explored]
    # print(graph.graph[to_vertex], weights_list, cur_weight, cur_path)
    # print(graph.best_weight)
    for unexplored_vertex in weights_list:
        # print(to_vertex, unexplored_vertex, explored.copy(), cur_weight, cur_path[:])
        find_optimal_path(graph, to_vertex, unexplored_vertex, explored.copy(), cur_weight, cur_path[:])

if __name__ == '__main__':
    print_answer(*optimal_path(read_data()))
