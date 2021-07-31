from collections import defaultdict

from utils import get_time_delta, MIN_LAYOVER_HRS, MAX_LAYOVER_HRS, LAYOVER_OK


class Graph:
    def __init__(self, bags_count, src, dst):
        self.nodes = {}
        self.paths = []
        self.bags_count = bags_count
        self.orig_src = src
        self.orig_dst = dst

    def create_graph(self, flights):
        for flight in flights:
            if flight["origin"] not in self.nodes:
                self.nodes[flight["origin"]] = Node(flight["origin"])
            if flight["destination"] not in self.nodes:
                self.nodes[flight["destination"]] = Node(flight["destination"])

            self.nodes[flight["origin"]].add_edge(flight, self.nodes[flight["destination"]])

    def print_graph(self):
        for node_src, node in self.nodes.items():
            print("SRC: ", node_src)
            for edge in node.edges:
                print(f"{edge.flight_info['origin']} -> {edge.flight_info['destination']}")

    def search(self, src, dst, visited, path, flight_info, return_trip, layover_enabled):
        visited[src] = True
        if flight_info:
            path.append(flight_info)
        if src == dst:
            if return_trip:
                self.search(self.nodes[self.orig_dst], self.nodes[self.orig_src],
                            defaultdict(lambda: False), path[:-1], flight_info, False, False)
            else:
                self.paths.append(path[:])
        else:
            for edge in src.edges:
                if flight_info:
                    layover_time_hrs = get_time_delta(flight_info["arrival"], edge.flight_info["departure"], hrs=True)
                else:
                    layover_time_hrs = LAYOVER_OK

                if not layover_enabled:
                    is_layover_time_in_interval = layover_time_hrs > 0
                else:
                    if layover_time_hrs > MAX_LAYOVER_HRS:  # FIXME treba sa uistit ze je zoznam sortnuty/sortnut ho
                        break  # az 40% performance increase
                    is_layover_time_in_interval = MIN_LAYOVER_HRS <= layover_time_hrs <= MAX_LAYOVER_HRS

                are_all_bags_allowed = edge.flight_info["bags_allowed"] >= self.bags_count
                if are_all_bags_allowed and is_layover_time_in_interval and not visited[edge.dst]:
                    self.search(edge.dst, dst, visited, path, edge.flight_info, return_trip, True)

        if flight_info:
            path.pop()
        visited[src] = False


class Node:
    def __init__(self, name):
        self.edges = []
        self.name = name

    def add_edge(self, data, dst):
        self.edges.append(Edge(data, self, dst))

    def __str__(self):
        return self.name


class Edge:
    def __init__(self, flight_info_input, src, dst):
        self.flight_info = flight_info_input
        self.src = src
        self.dst = dst

    def __str__(self):
        return f"{self.src} -> {self.dst}"
