import csv
import sys
from datetime import datetime

MIN_LAYOVER_HRS = 1
MAX_LAYOVER_HRS = 6
LAYOVER_OK = 1  # explicit value so we dont calculate non existent layover


def parse_args(argv):
    """
    Parses program arguments from list of command line arguments.
    @param argv: list of arguments
    @return: tuple of parsed arguments ->
        file path of CSV file: str,
        origin airport code: str,
        destination airport code: str,
        maximum allowed bags: int,
        true/false if the program should include return trip: boolean
    @raise ValueError: if value of argument --bags was negative
    @raise TypeError: if value of argument --bags was invalid
    """
    bags = 0
    return_trip = False
    try:
        file_path, src, dst = argv[1], argv[2], argv[3]  # required args
        for argument in argv[4:]:
            if "--bags=" in argument:
                bags = int(argument.split("=")[1])  # structure of argument is --bags=X where X is positive integer
                if bags < 0:
                    raise ValueError("Entered value for argument '--bags' is negative.")
            elif argument == "--return":
                return_trip = True
    except ValueError as e:
        print_arg_error("Error: Missing positive integer number for parameter --bags", e)
        sys.exit(-1)
    except IndexError as e:
        print_arg_error("Error: Missing required arguments", e)
        sys.exit(-2)
    return file_path, src, dst, bags, return_trip


def print_arg_error(description, exception_msg=None):
    """
    prints formatted error description
    @param description: message about raised exception - str
    @param exception_msg: details - information gathered by interpreter - str. Default: None
    """
    print(description, file=sys.stderr)
    if exception_msg:
        print("Details:\n", exception_msg, file=sys.stderr)


def read_csv(path):
    """
    Reads csv file and changes base_price, bag_price and bags_allowed columns to corresponding data types
    @param path: path to the csv file
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
        with open(path, "r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            if csv_reader.fieldnames != allowed_columns:
                raise ValueError("CSV file contains illegal collumns.")
            res = []
            for row in csv_reader:
                row["base_price"] = float(row["base_price"])  # we do this to simplify manipulating with those fields
                row["bag_price"] = float(row["bag_price"])  # in later stages of solution
                row["bags_allowed"] = int(row["bags_allowed"])  # see core.solver.find_all_paths
                res.append(row)
    except ValueError as e:
        print_arg_error("Error: CSV file error", e)
        sys.exit(-3)
    except FileNotFoundError as e:
        print_arg_error("Error: CSV file does not exist.", e)
        sys.exit(-4)
    except TypeError as e:
        print_arg_error("Error: Corrupted CSV file", e)
        sys.exit(-5)
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
