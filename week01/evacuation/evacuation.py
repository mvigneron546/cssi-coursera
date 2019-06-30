# python3

from heapq import heappop, heappush

class Edge:

    def __init__(self, u, v, capacity):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0

# This class implements a bit unusual scheme for storing edges of the graph,
# in order to retrieve the backward edge for a given edge quickly.
class FlowGraph:

    def __init__(self, n):
        # List of all - forward and backward - edges
        self.edges = []
        # These adjacency lists store only indices of edges in the edges list
        self.graph = [[] for _ in range(n)]

    def add_edge(self, from_, to, capacity):
        # Note that we first append a forward edge and then a backward edge,
        # so all forward edges are stored at even indices (starting from 0),
        # whereas backward edges are stored at odd indices.
        forward_edge = Edge(from_, to, capacity)
        backward_edge = Edge(to, from_, 0)
        # print(from_, to)
        self.graph[from_].append(len(self.edges))
        self.edges.append(forward_edge)
        self.graph[to].append(len(self.edges))
        self.edges.append(backward_edge)

    def size(self):
        return len(self.graph)

    def get_ids(self, from_):
        return self.graph[from_]

    def get_edge(self, id):
        return self.edges[id]

    def add_flow(self, id, flow):
        # To get a backward edge for a true forward edge (i.e id is even), we should get id + 1
        # due to the described above scheme. On the other hand, when we have to get a "backward"
        # edge for a backward edge (i.e. get a forward edge for backward - id is odd), id - 1
        # should be taken.
        #
        # It turns out that id ^ 1 works for both cases. Think this through!
        self.edges[id].flow += flow
        self.edges[id ^ 1].flow -= flow


def read_data():
    vertex_count, edge_count = map(int, input().split())
    graph = FlowGraph(vertex_count)
    for _ in range(edge_count):
        u, v, capacity = map(int, input().split())
        graph.add_edge(u - 1, v - 1, capacity)
    return graph


def max_flow(graph, from_, to):
    """ Uses Edmonds-Karp algorithm to compute maxflow """
    flow = 0
    # your code goes here
    path = edge_BFS(from_, to)
    # generate first path
    while path:
        # take maxflow of the remaining flows
        maxflow = min([graph.edges[edge].capacity - graph.edges[edge].flow for edge in path])
        for edge in path:
            graph.add_flow(edge, maxflow)
        flow += maxflow
        path = edge_BFS(from_, to)
    # residual would be seeking backward edges that have a positive capacity
    # find mincut after pathing, set flow to cur_flow + mincut, set backward edges to edge.flow - mincut (just use add_flow to accomplish this)
    return flow

# def BFS(start, target):
#     '''
#     uses BFS to find the smallest sequence of steps to the target.
#     returns a list of steps.
#     '''
#     explored = set()
#     frontier = []
#     heappush(frontier, (0, start, [start]))
#     # search ops; len(curr_path) - 1 is the traversal_cost
#     while len(frontier) != 0:
#         current_node = heappop(frontier)
#         # print('Current Node:',current_node)
#         if current_node[1] == target:
#             return current_node[2]
#         elif current_node[1] not in explored:
#             explored.add(current_node[1])
#             neighbors = get_neighbors(current_node[1])
#             for neighbor in neighbors:
#                 # if the neighbor isn't in explored and the remaining capacity != 0, add it to the pqueue
#                 remaining_capacity = graph.edges[neighbor].capacity - graph.edges[neighbor].flow
#                 destination = graph.edges[neighbor].v
#                 # print('Capacity:',remaining_capacity)
#                 if destination not in explored and remaining_capacity > 0:
#                     # taking destination node, as starting node is the one you're on
#                     curr_path = current_node[2][:]
#                     curr_path.append(destination)
#                     node = (len(curr_path) - 1, destination, curr_path)
#                     heappush(frontier,node)
#         # print('Frontier:',frontier)
#         # print('explored:', explored)
#     return [] # no path exists

def edge_BFS(start, target):
    '''
    uses BFS to find the smallest sequence of edges taken to the target.
    returns a list of the edge indices.
    '''
    explored = set()
    frontier = []
    heappush(frontier, (0, start, []))
    # search ops; len(curr_path) - 1 is the traversal_cost
    while len(frontier) != 0:
        current_node = heappop(frontier)
        if current_node[1] == target:
            return current_node[2]
        elif current_node[1] not in explored:
            explored.add(current_node[1])
            # neighbors = get_neighbors(current_node[1])
            neighbors = graph.graph[current_node[1]]
            for neighbor in neighbors:
                destination = graph.edges[neighbor].v
                if neighbor % 2 == 0:
                    remaining_capacity = graph.edges[neighbor].capacity - graph.edges[neighbor].flow
                    if destination not in explored and remaining_capacity > 0:
                        # taking destination node, as starting node is the one you're on
                        curr_path = current_node[2][:]
                        # append index of the edge as it appears in graph.edges
                        curr_path.append(neighbor)
                        node = (len(curr_path) - 1, destination, curr_path)
                        heappush(frontier,node)
                elif neighbor % 2 == 1:
                    # only care about backwards edge when cancellations can be made (ie. the backwards node's flow == capacity)
                    if abs(graph.edges[neighbor].flow) == graph.edges[neighbor^1].capacity and destination not in explored:
                        # taking destination node, as starting node is the one you're on
                        curr_path = current_node[2][:]
                        # append index of the edge as it appears in graph.edges
                        curr_path.append(neighbor)
                        node = (len(curr_path) - 1, destination, curr_path)
                        heappush(frontier,node)
    return [] # no path exists


if __name__ == '__main__':
    graph = read_data()
    # print(graph.graph)
    # print([(edge.u,edge.v) for edge in graph.edges])
    # print(edge_BFS(0, len(graph.graph)-1))
    print(max_flow(graph, 0, graph.size() - 1))
