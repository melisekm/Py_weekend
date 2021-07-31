from sys import stderr


def parse_args(argv):
    file_path, src, dst = argv[1], argv[2], argv[3]
    bags = 0
    return_trip = False
    for argument in argv[4:]:
        if "--bags" in argument:
            bags = int(argument.split("=")[1])
        elif argument == "--return":
            return_trip = True
    return file_path, src, dst, bags, return_trip


def print_arg_error(description, exception_msg=None):
    print(description, file=stderr)
    if exception_msg:
        print("Details:\n", exception_msg)
