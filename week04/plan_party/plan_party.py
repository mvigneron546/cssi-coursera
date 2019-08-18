#uses python3

import sys
import threading

# This code is used to avoid stack overflow issues
sys.setrecursionlimit(10**6) # max depth of recursion
threading.stack_size(2**26)  # new thread will get stack of such size


class Vertex:
    def __init__(self, weight):
        self.weight = weight
        self.children = []
        self.optimal_weight = -1

def ReadTree():
    size = int(input())
    tree = [Vertex(w) for w in map(int, input().split())]
    for i in range(1, size):
        a, b = list(map(int, input().split()))
        tree[a - 1].children.append(b - 1)
        tree[b - 1].children.append(a - 1)
    return tree

def dfs(tree, vertex, parent):
    print(parent, vertex, tree[vertex].children)
    for child in tree[vertex].children:
        if child != parent:
            dfs(tree, child, vertex)

    # This is a template function for processing a tree using depth-first search.
    # Write your code here.
    # You may need to add more parameters to this function for child processing.
    if len(tree[vertex].children) == 1:
        if tree[vertex].children[0] == parent:
            tree[vertex].optimal_weight = tree[vertex].weight
            return
    for child in tree[vertex].children:
        if child != parent:
            tree[vertex].optimal_weight += tree[child].optimal_weight
    #     return vertex.weight


def MaxWeightIndependentTreeSubset(tree, vertex, parent):
    size = len(tree)
    if size == 0:
        return 0
    dfs(tree, 0, -1)
    # You must decide what to return.
    return tree[0].optimal_weight
    # if not tree[vertex].children:
    #     return tree[vertex].weight
    # # compute for current vertex and grandchildren
    # first_weight = tree[vertex].weight
    # for child in tree[vertex].children:
    #     if child != parent:
    #         for grand_child in tree[child].children:
    #             if grand_child != vertex:
    #                 first_weight += MaxWeightIndependentTreeSubset(tree, grand_child, child)
    # # compute for children only
    # second_weight = 0
    # for child in tree[vertex].children:
    #     if child != vertex:
    #         second_weight += MaxWeightIndependentTreeSubset(tree, child, vertex)
    # return max(first_weight, second_weight)


def main():
    tree = ReadTree()
    # print(tree)
    weight = MaxWeightIndependentTreeSubset(tree, 0, -1)
    print([v.children for v in tree])
    print([v.optimal_weight for v in tree])
    print(weight)


# This is to avoid stack overflow issues
# main()
threading.Thread(target=main).start()
