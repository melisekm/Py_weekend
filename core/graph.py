from collections import defaultdict

from utils import get_time_delta, MIN_LAYOVER_HRS, MAX_LAYOVER_HRS, LAYOVER_OK


class Graph:
    """
    Represents airports as nodes and edges as flights between two airports.
    Directed oriented multigraph.
    """

    def __init__(self, bags_count, src, dst):
        """
        Inicializes internal graph data structures
        @param bags_count: Number of requested bags
        @param src: origin airport code
        @param dst: destination aiport code
        """
        self.nodes = {}
        self.paths = []
        self.bags_count = bags_count
        self.orig_src = src
        self.orig_dst = dst

    def create_graph(self, flights):
        """
        Creates nodes and edges in the graph
        @param flights: list of flights(edges) between airports
        """
        for flight in flights:
            # create both nodes if they do not exist yet
            if flight["origin"] not in self.nodes:
                self.nodes[flight["origin"]] = Node(flight["origin"])
            if flight["destination"] not in self.nodes:
                self.nodes[flight["destination"]] = Node(flight["destination"])

            self.nodes[flight["origin"]].add_edge(flight, self.nodes[flight["destination"]])

    def search(self, src, dst, visited, path, flight_info, return_trip, layover_enabled):
        """
        Recursive Depth First Search through the graph to obtain all combinations of flights from A to B.
        Populates self graph attribute paths with all combinations.
        @param src: currently visited Node
        @param dst: final Node
        @param visited: boolean defaultdict of visited nodes
        @param path: list of flights in currently constructed path
        @param flight_info: info about latest added path
        @param return_trip: if during currrent recursive iteration we search for return trip from the destination
        @param layover_enabled: if we care about layover interval time.
        We do not, if we have just arrived to the final destination and we are on a return trip.
        """
        visited[src] = True
        if flight_info:
            path.append(flight_info)  # add flight info to the temporary path list
        if src == dst:  # we arrived in destination
            if return_trip:
                # perform return trip search with same temp path, but without layover.
                self.search(self.nodes[self.orig_dst], self.nodes[self.orig_src],
                            defaultdict(lambda: False), path[:-1], flight_info, False, False)
            else:
                self.paths.append(path[:])  # include current temp path in the final result
        else:
            for edge in src.edges:  # search all neighbouring nodes, which are in the layover interval
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

        if flight_info:  # recursion is unwinding, because we checked all adjacent edges
            path.pop()
        visited[src] = False


class Node:
    """
    Represents airport as a node in the graph
    """

    def __init__(self, name):
        """
        Initialize internal list of edges
        @param name: code of the airport
        """
        self.edges = []  # adjacency list
        self.name = name

    def add_edge(self, data, dst):
        """
        Create and add edge to the list of edges
        """
        self.edges.append(Edge(data, self, dst))

    def __str__(self):
        return self.name


class Edge:
    """
    Represents one flight between two airports(nodes) as an edge.
    """

    def __init__(self, flight_info_input, src, dst):
        self.flight_info = flight_info_input
        self.src = src
        self.dst = dst

    def __str__(self):
        return f"{self.src} -> {self.dst}"
