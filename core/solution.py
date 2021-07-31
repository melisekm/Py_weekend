from sys import argv, exit

from arg_parser import parse_args, print_arg_error
from read_csv import read_csv
from solver import solve

if __name__ == "__main__":
    try:
        file_path, src, dst, bags, return_trip = parse_args(argv)
    except ValueError as e:
        print_arg_error("Error: Missing integer number for parameter --bags", e)
        exit(-1)
    except IndexError as e:
        print_arg_error("Error: Missing required arguments", e)
        exit(-2)

    try:
        flights = read_csv(file_path)
    except ValueError as e:
        print_arg_error(e)
        exit(-3)
    except FileNotFoundError as e:
        print_arg_error("Error: CSV file does not exist.", e)
        exit(-4)
    except TypeError as e:
        print_arg_error("Error: Corrupted CSV file", e)
        exit(-5)

    solution = solve(flights, src, dst, bags, return_trip)
    if solution == -1:
        print_arg_error("Error: ORIGIN airport code was not found in input CSV file.")
        exit(-6)
    elif solution == -2:
        print_arg_error("Error: DESINATION airport code was not found in input CSV file.")
        exit(-7)
    else:
        print(solution)