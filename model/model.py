import copy
import random

from database.DAO import DAO
import networkx as nx
from geopy.distance import distance


class Model:
    def __init__(self):
        self._best_len = None
        self._best_sol = None
        self._providers = DAO.get_all_providers()
        self._graph = None
        self._nodes = None

    def build_graph(self, provider, d):
        self._nodes = DAO.get_locations(provider)
        self._graph = nx.Graph()
        self._graph.add_nodes_from(self._nodes)
        for u in self._graph.nodes:
            for v in self._graph.nodes:
                if u != v:
                    dist = distance((u.Latitude, u.Longitude), (v.Latitude, v.Longitude))
                    if dist <= d:
                        self._graph.add_edge(u, v, weight=dist)

    def get_graph_details(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def get_nodes_neighbors(self):
        neighbors_tuple = [(n, len(self._graph[n])) for n in self._graph.nodes]
        neighbors_tuple.sort(key=lambda tup: tup[1], reverse=True)
        result = [n for n in neighbors_tuple if n[1] == neighbors_tuple[0][1]]  # aggiungo solo quelli che hanno
        # lo stesso numero di vicini del primo
        return result

    def get_percorso(self, target, s):
        sources = self.get_nodes_neighbors()
        source = sources[random.randint(0, len(sources) - 1)][0]
        if not nx.has_path(self._graph, source, target):
            return [], source
        self._best_sol = []
        self._best_len = 0
        parziale = [source]
        self.ricorsione(parziale, s, target)
        return self._best_sol, source

    def ricorsione(self, parziale, s, target):
        if parziale[-1] == target:  # esco quando sono arrivato al target
            if len(parziale) > self.best_len:
                self._best_sol = copy.deepcopy(parziale)
                self._best_len = len(parziale)
            return
        for v in self._graph.neighbors(parziale[-1]):
            if v not in parziale and s not in v.Location:
                parziale.append(v)
                self.ricorsione(parziale, s, v)
                parziale.pop()

    @property
    def best_len(self):
        return self._best_len

    @property
    def best_sol(self):
        return self._best_sol

    @property
    def providers(self):
        return self._providers

    @property
    def graph(self):
        return self._graph


