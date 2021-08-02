import datetime
import json
import sys
from collections import defaultdict

from graph import Graph
from utils import get_time_delta, print_arg_error


def solve(flights, src, dst, bags_count, return_trip):
    """
    Creates graph and initializes search for all combinations
    @param flights: list of dicts of flights
    @param src: origin airport code
    @param dst: destination aiport code
    @param bags_count: Number of requested bags
    @param return_trip: Is it a return flight
    @return: json-compatible structured list of trips sorted by price.
    """
    graph = Graph(bags_count, src, dst)
    graph.create_graph(flights)

    if src not in graph.nodes:
        print_arg_error("Error: ORIGIN airport code was not found in input CSV file.")
        sys.exit(1)
    if dst not in graph.nodes:
        print_arg_error("Error: DESTINATION airport code was not found in input CSV file.")
        sys.exit(1)

    return find_all_paths(graph, src, dst, return_trip)


def calc_travel_time(path):
    """
    Calculates final travelling time including layover.
    @param path: list of flights taken
    @return: formatted time - str
    """
    sum_seconds = 0
    prev = None  # holds information about latest flight, used to calculate layover time
    for flight in path:
        if prev:
            # get time between previous arrival and next departure
            sum_seconds += get_time_delta(flight["departure"], prev, sec=True, reversed=True)
        # get time between departure and arrival
        sum_seconds += get_time_delta(flight["arrival"], flight["departure"], sec=True, reversed=True)
        prev = flight["arrival"]
    return str(datetime.timedelta(seconds=sum_seconds))


def find_all_paths(graph, src, dst, return_trip):
    """
    Utility function to initialize DFS (Depth first search) from src node to dst node.
    After the run is finished flight description is appended to each path found
    and result is formatted to json compatible format.
    @param graph: oriented multigraph which hold flights
    @param src: origin airport code
    @param dst: destination aiport code
    @param return_trip: Is it a return flight
    @return list of paths containing list of flights and information about the path
    """

    # defaultdict represents visited nodes, those which were not yet visited are implictly False
    # empty list of current path
    # no info about current flight because there was not any node searched
    graph.search(graph.nodes[src], graph.nodes[dst], defaultdict(lambda: False), [], None, return_trip, True)

    res = []
    for path in graph.paths:
        path_obj = {
            "flights": path,
            # if one of the flights has max allowed 1 bag we can take only 1 bag with us on the whole trip.
            # obtains flight with minimum amount of bags_allowed and returns its value
            "bags_allowed": int(min(path, key=lambda x: x["bags_allowed"])["bags_allowed"]),
            "bags_count": graph.bags_count,
            "destination": dst,
            "origin": src,
            "total_price": sum(
                map(lambda x: x["base_price"] + x["bag_price"] * graph.bags_count, path)
            ),
            "travel_time": calc_travel_time(path)
        }
        res.append(path_obj)

    return json.dumps(sorted(res, key=lambda x: x["total_price"]))
