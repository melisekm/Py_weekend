# Author: Martin Melisek
# Date: 31.7.2021
# Find all flight combinations for a selected route between airports A -> B, sorted by fianl price for the trip
# Results are printed to stdout
# Usage: python -m solution <CSV FILE> <ORIGIN_AIRPORT_CODE> <DESTINATION_AIRPORT_CODE> [--bags=<BAG_COUNT>] [--return]
# Example: python -m solution data.csv DHE NIZ --bags=2 --return

import sys

from solver import solve
from utils import parse_args, read_csv

if __name__ == "__main__":
    file_path, src, dst, bags, return_trip = parse_args(sys.argv)
    flights = read_csv(file_path)
    solution = solve(flights, src, dst, bags, return_trip)
    print(solution)
