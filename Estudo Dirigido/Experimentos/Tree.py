#!/usr/bin/env python3
class Tree:

    def __init__(self, depth):
        self.depth = depth
        #nós de branch: [1, ..., 2^depth - 1]
        self.nodes = [i for i in range(1, (1 << depth))]
        # nós folha: [2^depth, ..., 2^(depth + 1) - 1]
        self.leaves = [i for i in range((1 << depth), (1 << (depth + 1)))]

    def get_depth(self):
        return self.depth

    def left(self, node):
        return 2 * node

    def right(self, node):
        return 2 * node + 1

    def get_nodes(self):
        return self.nodes

    def get_leaves(self):
        return self.leaves
    
    def get_parent(self, node):
        return node // 2
