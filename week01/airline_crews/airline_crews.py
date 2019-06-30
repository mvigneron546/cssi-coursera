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

def max_flow(graph, from_, to):
    """ Uses Edmonds-Karp algorithm to compute maxflow """
    flow = 0
    # your code goes here
    path = edge_BFS(graph, from_, to)
    # generate first path
    while path:
        # take maxflow of the remaining flows
        maxflow = min([graph.edges[edge].capacity - graph.edges[edge].flow for edge in path])
        for edge in path:
            graph.add_flow(edge, maxflow)
        flow += maxflow
        path = edge_BFS(graph, from_, to)
    # residual would be seeking backward edges that have a positive capacity
    # find mincut after pathing, set flow to cur_flow + mincut, set backward edges to edge.flow - mincut (just use add_flow to accomplish this)
    return flow

def edge_BFS(graph, start, target):
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

class MaxMatching:
    def read_data(self):
        n, m = map(int, input().split())
        self.graph = FlowGraph(n + m + 2) # account for all vertices, including ones at start and end
        adj_matrix = [list(map(int, input().split())) for i in range(n)]
        # populate FlowGraph with edges
        for i in range(len(adj_matrix)):
            if 1 in adj_matrix[i]:
                # connect start_ndoe to airline flights, capacity 1 as in bipartite matching
                flight_node = i + 1
                self.graph.add_edge(0, flight_node, 1)
                # add crews, connect with airplan crews and end_node
                for j in range(len(adj_matrix[i])):
                    if adj_matrix[i][j] == 1:
                        crew_node = len(adj_matrix) + 1 + j
                        self.graph.add_edge(flight_node, crew_node, 1)
        # connect all crews to the end_node
        for j in range(len(adj_matrix[0])):
            crew_node = len(adj_matrix) + 1 + j
            self.graph.add_edge(crew_node, n + m + 1, 1)
        # print([(edge.u, edge.v) for edge in self.graph.edges if edge.u == 101 or edge.v == 101])
        return adj_matrix

    def write_response(self, matching):
        line = [str(-1 if x == -1 else x + 1) for x in matching]
        print(' '.join(line))

    def find_matching(self, adj_matrix):
        # Replace this code with an algorithm that finds the maximum
        # matching correctly in all cases.
        n = len(adj_matrix)
        m = len(adj_matrix[0])
        max_flow(self.graph, 0, n + m + 1)
        # print([(edge.u, edge.v, edge.flow) for edge in self.graph.edges if edge.v != n+m+1]) # if edge.flow == 1 and edge.u != 0 and edge.v != n + m + 1]))
        # print(self.graph.graph)
        matching = [-1] * n
        for edge in self.graph.edges:
            # if edge.v == 101:
            #     print('Edge:', edge.u, edge.v)
            if edge.flow == 1 and edge.u != 0 and edge.v != n + m + 1:
                # flights are flight-1; crews are index-len(flights)-1
                # print('Edge combo:', 'Former Start:', edge.u, 'Start:', edge.u-1, 'Former End:', edge.v, 'End:', edge.v - n - 1)
                matching[edge.u - 1] = edge.v - n - 1
        return matching

    def solve(self):
        adj_matrix = self.read_data()
        # print(adj_matrix)
        # print([(edge.u, edge.v) for edge in self.graph.edges])
        matching = self.find_matching(adj_matrix)
        self.write_response(matching)

if __name__ == '__main__':
    max_matching = MaxMatching()
    max_matching.solve()
