#!/usr/bin/env python3

from label_compare.label import Labelling

def main():
    d = Labelling.from_csv_in_seconds("./examples/example.csv")
    print(d.labels)

if __name__ == "__main__":
    main()
