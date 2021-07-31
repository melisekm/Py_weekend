import csv

allowed_columns = [
    'flight_no', 'origin', 'destination', 'departure',
    'arrival', 'base_price', 'bag_price', 'bags_allowed'
]


def read_csv(path):
    with open(path, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        if csv_reader.fieldnames != allowed_columns:
            raise ValueError("CSV file contains illegal collumns.")
        res = []
        for row in csv_reader:
            row["base_price"] = float(row["base_price"])
            row["bag_price"] = float(row["bag_price"])
            row["bags_allowed"] = int(row["bags_allowed"])
            res.append(row)
    return res
