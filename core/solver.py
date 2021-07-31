import datetime
import json
from collections import defaultdict

from graph import Graph
from utils import get_time_delta


def solve(flights, src, dst, bags_count, return_trip):
    graph = Graph(bags_count, src, dst)
    graph.create_graph(flights)

    if src not in graph.nodes:
        return -1
    if dst not in graph.nodes:
        return -2

    return find_all_paths(graph, src, dst, return_trip)


def calc_travel_time(path):
    sum_seconds = 0
    prev = None
    for flight in path:
        if prev:
            sum_seconds += get_time_delta(flight["departure"], prev, sec=True, reversed=True)
        sum_seconds += get_time_delta(flight["arrival"], flight["departure"], sec=True, reversed=True)
        prev = flight["arrival"]
    return str(datetime.timedelta(seconds=sum_seconds))


def find_all_paths(graph, src, dst, return_trip):
    graph.search(graph.nodes[src], graph.nodes[dst], defaultdict(lambda: False), [], None, return_trip, True)

    res = []
    for path in graph.paths:
        path_obj = {
            "flights": path,
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
