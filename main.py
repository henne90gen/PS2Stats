#!/bin/python3
from classes import *
import spreadsheet_writer as sw

metrics = [Metrics.KDR, Metrics.IvI_Score, Metrics.IvI_Accuracy, Metrics.IvI_HSR, Metrics.IvI_KDR, Metrics.IvI_KPM]


def main():
    # members = ["halospud", "Swooshed", "Bilowan", "Bilowan"]
    # my_squad = Squad(members)
    # data = my_squad.get_data(metrics)
    outfit = Outfit("h")
    data = outfit.get_data(metrics)
    for data_point in data:
        print(data_point)
    sw.write(data, "Squad Statistics")


if __name__ == "__main__":
    main()
