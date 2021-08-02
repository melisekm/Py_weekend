# Author: Martin Melisek
# Date: 31.7.2021
# Find all flight combinations for a selected route between airports A -> B, sorted by final price for the trip
# Results are printed to stdout
# Usage: python -m solution <CSV FILE> <ORIGIN_AIRPORT_CODE> <DESTINATION_AIRPORT_CODE> [--bags=<BAG_COUNT>] [--return]
# Example: python -m solution data.csv DHE NIZ --bags=2 --return

from solver import solve
from utils import parse_args, read_csv

if __name__ == "__main__":
    csv_file, src, dst, bags, return_trip = parse_args()
    flights = read_csv(csv_file)
    solution = solve(flights, src, dst, bags, return_trip)
    print(solution)
