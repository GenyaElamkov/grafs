import configparser

from collections import namedtuple

from src.read_csv import read_excel, get_data_csv
from src.show_graphics import building_graphics, sorted_table_csv


def setting(filename: str) -> None:
    read_excel(filename, file_name_out="data.csv")
    data = get_data_csv(filename="data.csv")

    Object_csv = namedtuple(
        "Object_csv", ["analiz_object", "sum_inst", "sum_out", "agent", "inn"]
    )
    config = configparser.ConfigParser()
    config.read("settings.ini", encoding="utf-8")

    object_csv = Object_csv(
        config["CSV_table"]["analiz_object"],
        config["CSV_table"]["sum_inst"],
        config["CSV_table"]["sum_out"],
        config["CSV_table"]["agent"],
        config["CSV_table"]["inn"],
    )
    data = sorted_table_csv(data, field_name=object_csv.sum_out)
    building_graphics(data, object_csv, filename_out_html="nx.html")
