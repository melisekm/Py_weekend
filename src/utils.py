import argparse
import csv
import sys
from datetime import datetime

MIN_LAYOVER_HRS = 1
MAX_LAYOVER_HRS = 6
LAYOVER_OK = 1  # explicit value so we dont calculate non existent layover


def parse_args():
    """
    Parses program arguments from command line arguments.
    @return: tuple of parsed arguments.
        file handle to csv file: TextIOWrapper.
        origin airport code: str.
        destination airport code: str.
        maximum allowed bags: int.
        true/false if the program should include return trip: boolean.
    """

    def non_negative_int(x):
        i = int(x)
        if i < 0:
            raise ValueError('Negative values are not allowed')
        return i

    program_description = "Find all flight combinations for a selected route between airports A -> B, " \
                          "sorted by final price for the trip"
    epilog = "example: python -m solution data.csv DHE NIZ --bags=2 --return"

    arg_parser = argparse.ArgumentParser(description=program_description, epilog=epilog)
    arg_parser.add_argument("csv_file", help="File path of input CSV file", type=argparse.FileType())
    arg_parser.add_argument("origin", help="Origin airport code")
    arg_parser.add_argument("destination", help="Destination airport code")
    arg_parser.add_argument("--bags", default=0, help="Number of requested bags", type=non_negative_int)
    arg_parser.add_argument("--return", action="store_true", default=False, help="Is it a return flight?",
                            dest="return_trip")

    args = arg_parser.parse_args()
    if args.origin == args.destination:
        print_arg_error("Error: origin and destination airport can not be the same.")
        sys.exit(1)

    return args.csv_file, args.origin, args.destination, args.bags, args.return_trip


def print_arg_error(description, exception_msg=None):
    """
    prints formatted error description
    @param description: message about raised exception - str
    @param exception_msg: details - information gathered by interpreter - str. Default: None
    """
    print(description, file=sys.stderr)
    if exception_msg:
        print("Details:\n", exception_msg, file=sys.stderr)


def read_csv(csv_file):
    """
    Reads csv file and changes base_price, bag_price and bags_allowed columns to corresponding data types
    Sorts the resulting list by departure time, if it was not sorted before
    @param csv_file: handle to opened csv file: _io.TextIOWrapper
    @return: list of dictionaries with keys as columns and values as fields - each dictionary is one flight
    @raise ValueError: if csv file contains illegal collumns
    @raise FileNotFoundError: if csv file does not exist.
    @raise TypeError: if one of the changed columns contains illegal value
    """
    # csv file has to contain these columns
    allowed_columns = [
        'flight_no', 'origin', 'destination', 'departure',
        'arrival', 'base_price', 'bag_price', 'bags_allowed'
    ]
    try:
        csv_reader = csv.DictReader(csv_file)
        if csv_reader.fieldnames != allowed_columns:
            raise ValueError("CSV file contains illegal collumns.")
        res = []
        for row in csv_reader:
            row["base_price"] = float(row["base_price"])  # we do this to simplify manipulating with those fields
            row["bag_price"] = float(row["bag_price"])  # in later stages of solution
            row["bags_allowed"] = int(row["bags_allowed"])  # see solver.find_all_paths
            res.append(row)
    except ValueError as e:
        print_arg_error("Error: CSV file error", e)
        sys.exit(1)
    except TypeError as e:
        print_arg_error("Error: Corrupted CSV file", e)
        sys.exit(1)

    csv_file.close()

    # checks if list of flights is sorted based on departure, if not sorts it
    # later on, it helps us to prune search space
    # so we can eliminate flights with very high layover and skip them immediately
    if not all(res[i]["departure"] <= res[i + 1]["departure"] for i in range(len(res) - 1)):
        res.sort(key=lambda x: x["departure"])

    return res


def get_time_delta(arrival, departure, hrs=False, sec=False, reversed=False):
    """
    Calculates time between two dates
    @param arrival: date in format of %Y-%m-%dT%H:%M:%S - str
    @param departure: same as arrival
    @param hrs: if the returned result should be in hours - boolean. Default: False
    @param sec: if the returned result should be in seconds - boolean. Default: False
    @param reversed: swaps the arrival and departure arguments - boolean. Default: False
    @return: time difference between two dates, with no args return type is datetime.timedelta.
    If hrs or sec is set returns integer
    """
    arrival = datetime.strptime(arrival, "%Y-%m-%dT%H:%M:%S")
    departure = datetime.strptime(departure, "%Y-%m-%dT%H:%M:%S")
    time_delta = arrival - departure if reversed else departure - arrival
    if hrs:
        return time_delta.total_seconds() / 3600
    if sec:
        return time_delta.total_seconds()
    return time_delta
