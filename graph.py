# -*- coding: utf-8 -*-
# Authorin: Sandra Sánchez
# Project: Modulprojekt PRO II
# Datum: 21.08.2022


import networkx as nx
from matplotlib import pyplot as plt
from networkx.drawing.nx_pydot import graphviz_layout


class Graph:
    """
    Class that passes in a tuple with a BKTree.tree structure
    and draws a graphic from it.
    """

    def __init__(self, tree: tuple):
        self.tree = tree
        self.tuples = self.create_tuples()
        self.triples = self.create_triples()
        self.labels = self.get_edge_labels()

    def create_triples(self) -> list[tuple]:
        """
        Pass in a nested tuple with a bk-tree structure and adapt build
        a list of tuples of 3 format, where node_1, node_2 and their edit distance is
        represented. The resulting list of tuples will be then used by networkx
        to draw a graph visualization of the bk-tree structure.
        :return: list of triples.
        """
        self.triples = []
        node_1 = self.tree[0]
        nested_element = self.tree[1]
        for distance in nested_element:
            node_2 = nested_element[distance][0]
            triple = node_1, node_2, distance
            self.triples.append(triple)
            new_tuple = nested_element[distance]
            if new_tuple[1]:
                graph_tuple = Graph(new_tuple)
                self.triples = self.triples + graph_tuple.create_triples()
        return self.triples

    def create_tuples(self) -> list[tuple]:
        """
        Pass in a nested tuple with a bk-tree structure and build a list of tuples
        representing all edges. The list will be used to build the networkx graphic.
        :return: list of triples.
        """
        self.tuples = []
        node_1 = self.tree[0]
        nested_element = self.tree[1]
        for distance in nested_element:
            node_2 = nested_element[distance][0]
            _tuple = node_1, node_2
            self.tuples.append(_tuple)
            new_tuple = nested_element[distance]
            if new_tuple[1]:
                graph_tuple = Graph(new_tuple)
                self.tuples = self.tuples + graph_tuple.create_tuples()
        return self.tuples

    def get_edge_labels(self) -> dict:
        """
        Pass in the list of triples and get only the label information
        for every edge.
        :return: self.labels
        """
        self.labels = {}
        for triple in self.triples:
            node_1 = triple[0]
            node_2 = triple[1]
            label = triple[2]
            if (node_1, node_2) not in self.labels:
                self.labels[node_1, node_2] = label
        return self.labels

    def visualize_graph(self):
        """
        Generate directed graph, adding edges from self.tuples and
        calculating hierarchical positions from the 'dot' graphviz_layout.
        Add labels from self.labels, plot the graphic with matplotlib and save it.
        """
        tree_graph = nx.DiGraph()
        tree_graph.add_edges_from(self.tuples)
        # This layout draws the directed graph in a hierarchical way
        positions = graphviz_layout(tree_graph, prog='dot')
        nx.draw_networkx(tree_graph, pos=positions, node_size=1500, arrows=True)
        nx.draw_networkx_edge_labels(tree_graph, pos=positions, edge_labels=self.get_edge_labels())
        plt.savefig("bk_tree.png")
        plt.show()
