from advent.advent_tools import PuzzleSetup, Timer
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os


class Map:
    def __init__(self, mapstr):
        lines = [list(line) for line in mapstr.split("\n") if line != ""]

        self._map = np.array(lines, dtype=str)
        self.m, self.n = self._map.shape
        for i in range(self.m):
            for j in range(self.n):
                if self[i][j] == "S":
                    self.start = (i, j)
                    self[i][j] = "a"
                if self[i][j] == "E":
                    self.end = (i, j)
                    self[i][j] = "z"

        arr = [[ord(c) - 97 for c in self[i]] for i in range(self.m)]
        self._arr = np.array(arr, dtype=int)

        plot_dir = "plots"
        if not os.path.exists(plot_dir):
            os.makedirs(plot_dir)
        self.graph = nx.DiGraph()
        self.pos = {}
        self.pruned = False

    def __getitem__(self, idx):
        return self._map[idx]

    def neighbours(self, i, j):
        nbrs = set()
        if i > 0:
            nbrs.add((i - 1, j))
        if i < self.m - 1:
            nbrs.add((i + 1, j))
        if j > 0:
            nbrs.add((i, j - 1))
        if j < self.n - 1:
            nbrs.add((i, j + 1))
        return nbrs

    def partition(self):
        self.levels = [[] for i in range(26)]
        done = np.zeros(self._arr.shape, dtype=bool)
        regions = np.zeros((self.m, self.n, 2), dtype=int)

        def find_levels(i, j, k):
            cnt = len(self.levels[k])
            if done[i, j]:
                return
            elif self._arr[i, j] == k:
                done[i, j] = True
                regions[i, j, :] = [k, len(self.levels[k]) - 1]
                self.levels[k][-1].add((i, j))
                for (ii, jj) in self.neighbours(i, j):
                    if not done[ii, jj]:
                        find_levels(ii, jj, k)

        for k, level in enumerate(self.levels):
            for i in range(self.m):
                for j in range(self.n):
                    if self._arr[i, j] == k and not done[i, j]:
                        node = (k, len(level))
                        level.append(set())
                        find_levels(i, j, k)
                        self.graph.add_node(node)
                        x = np.mean([xy[1] for xy in level[-1]])
                        y = np.mean([xy[0] for xy in level[-1]])
                        self.pos[node] = (x, y)

        for k, level in enumerate(self.levels):
            for region in level:
                for (i, j) in region:
                    r = tuple(regions[i, j, :])
                    for (ii, jj) in self.neighbours(i, j):
                        if self._arr[ii, jj] < k or self._arr[ii, jj] == k + 1:
                            self.graph.add_edge(r, tuple(regions[ii, jj, :]))
        assert np.all(done)

    def prune_graph(self):
        self.pruned = True
        outnodes = [n1 for (n1, n2) in self.graph.out_edges]
        innodes = [n2 for (n1, n2) in self.graph.out_edges]
        for (n1, n2) in self.graph.copy().out_edges:
            if n1[0] == 25 or (n1[0] == 24 and n2[0] != 25):
                self.graph.remove_edge(n1, n2)
        for node in self.graph.copy().nodes:
            if node[0] != 25 and node not in outnodes:
                self.graph.remove_node(node)
        for node in self.graph.copy().nodes:
            if node[0] != 0 and node not in innodes:
                self.graph.remove_node(node)
        for node in self.graph.copy().nodes:
            if node[0] != 25 and self.graph.degree[node] <= 1:
                self.graph.remove_node(node)

    def view(self, dtype=str):
        if dtype == str:
            if setup.verbose:
                print("\n".join(["".join(m) for m in self._map]))
        elif dtype == int:
            if setup.verbose:
                print(self._arr)
        elif dtype == nx.DiGraph:
            fig, axes = plt.subplots()
            axes.set_title("Pruned region graph" if self.pruned else "All regions")
            nx.draw(self.graph, self.pos, with_labels=True, ax=axes)
            plt.savefig(f"plots/{'pruned' if self.pruned else 'initial'}_graph.png")
            plt.close()
        else:
            raise TypeError(f"dtype {dtype} not recognised")


class RouteFinder:
    def __init__(self, map, start=None, end=None):
        self.map = map
        self.start = start or self.map.start
        self.end = end or self.map.end
        self.m = self.map.m
        self.n = self.map.n
        self._region_routes = None
        self._in_nodes = None
        self._out_nodes = None

    @property
    def region_routes(self):
        if self._region_routes is None:
            region_list = list(
                nx.all_simple_paths(self.map.graph, source=(0, 0), target=(25, 0))
            )
            self._region_routes = [
                [self.map.levels[k][l] for (k, l) in region] for region in region_list
            ]
        return self._region_routes

    def determine_gateways(self):
        self._in_nodes = [[set() for region in route] for route in self.region_routes]
        self._out_nodes = [[set() for region in route] for route in self.region_routes]
        for r, route in enumerate(self.region_routes):
            self._in_nodes[r][0].add(self.map.start)
            self._out_nodes[r][-1].add(self.map.end)
            for k, region in enumerate(route[:-1]):
                for (i, j) in region:
                    for (ii, jj) in self.map.neighbours(i, j).intersection(route[k+1]):
                        self._out_nodes[r][k].add((i, j))
                        self._in_nodes[r][k+1].add((ii, jj))

    @property
    def in_nodes(self):
        if self._in_nodes is None:
            self.determine_gateways()
        return self._in_nodes

    @property
    def out_nodes(self):
        if self._in_nodes is None:
            self.determine_gateways()
        return self._out_nodes

    def region_graph(self, rou, reg):
        route = self.region_routes[rou]
        region = route[reg]
        I = set(self.in_nodes[rou][reg])
        O = set(self.out_nodes[rou][reg])

        Gr = nx.Graph()
        cmap = []
        pos = {}
        for (i, j) in region:
            Gr.add_node((i, j))
            pos[(i, j)] = (j, i)
            if (i, j) in I.union(O):
                Gr.add_edge((i, j), (i, j))
                colour = "purple"
            elif (i, j) in I:
                colour = "green"
            elif (i, j) in O:
                colour = "red"
            else:
                colour = "lightblue"
            cmap.append(colour)

            # Add adjacent nodes from the next region along
            if reg < len(route) - 1:
                for (ii, jj) in self.map.neighbours(i, j):
                    if (ii, jj) in set(self.in_nodes[rou][reg+1]).difference(set(Gr.nodes)):
                        Gr.add_node((ii, jj))
                        Gr.add_edge((i, j), (ii, jj))
                        pos[(ii, jj)] = (jj, ii)
                        cmap.append("yellow")

        # Connect all adjacent nodes in the graph
        for (i, j) in region:
            for (ii, jj) in region.difference({(i, j)}):
                if (abs(i - ii) + abs(j - jj) == 1):
                    Gr.add_edge((i, j), (ii, jj))

        # Plot the local graph
        fig, axes = plt.subplots()
        axes.set_title(f"Local graph for region {reg}")
        nx.draw(Gr, pos=pos, node_color=cmap, node_size=4, ax=axes)
        plt.savefig(f"plots/local_graph__route{rou}_reg{reg}.png")
        plt.close()
        return Gr

    def shortest_local_paths(self, rou, reg):
        paths = set()
        Gr = self.region_graph(rou, reg)
        T = {self.map.end} if reg == len(self.in_nodes[rou]) - 1 else self.in_nodes[rou][reg + 1]
        for source in self.in_nodes[rou][reg]:
            for target in T:
                paths.add(tuple(nx.shortest_path(Gr, source=source, target=target)))
        return paths

    def shortest_path(self):
        options = []
        for rou, route in enumerate(self.region_routes):
            paths = [self.shortest_local_paths(rou, reg) for reg, region in enumerate(route)]
            candidates = []
            for reg, path in enumerate(paths):
                candidates_ = set(candidates)

                # Keep only the shortest path between each start node and each end node
                for p1 in candidates:
                    for p2 in candidates:
                        if p1 != p2 and (p1[0], p1[-1]) == (p2[0], p2[-1]) and \
                            len(p1) >= len(p2) and {p1, p2}.issubset(candidates_):
                            candidates_.remove(p1)
                if setup.verbose:
                    print(f"Number of paths after trimming: {len(candidates_)}")
                    print(f"Route {rou}, region {reg} has {len(path)} possible paths")

                candidates = []
                for r, p1 in enumerate(path):
                    if reg == 0:
                        candidates.append(p1)
                    for p2 in candidates_:
                        if p2[-1] == p1[0]:
                            new = p2[:-1]
                            new += p1
                            candidates.append(new)
                if setup.verbose:
                    print(f"Current number of paths: {len(candidates)}")
            options += candidates

        minlen = np.inf
        choice = None
        for path in options:
            l = len(path) - 1
            if l < minlen:
                minlen = l
                choice = path
            if setup.verbose:
                print("\n" + "->".join([f"{i},{j}" for (i, j) in path]) + f" (length={l})")

        return minlen


setup = PuzzleSetup(__file__)
with open(setup.input_file, "r") as f:
    m = Map(f.read())

if setup.verbose:
    print("Map:")
    m.view(dtype=str)
    print("Map as levels:")
    m.view(dtype=int)

m.partition()
if setup.verbose:
    for k, level in enumerate(m.levels):
        print(f"There are {len(level)} regions at level {k}")
m.view(dtype=nx.DiGraph)
m.prune_graph()
m.view(dtype=nx.DiGraph)

rf = RouteFinder(m)
if setup.verbose:
    print(f"Number of routes through the regions: {len(rf.region_routes)}")
minlen = rf.shortest_path()
print(f"Part 1: {minlen}")

for i in range(m.m):
    for j in range(m.n):
        if m[i][j] == "a":
            start = (i, j)
            rf = RouteFinder(m, start=start)
            minlen = min(rf.shortest_path(), minlen)
print(f"Part 2: {minlen}")
