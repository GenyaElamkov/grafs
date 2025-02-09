from collections import namedtuple

from src.read_csv import read_excel, get_data_csv
from src.show_graphics import building_graphics


def setting(filename: str) -> None:
    read_excel(filename, file_name_out='data.csv')
    data = get_data_csv(filename="data.csv")

    Object_csv = namedtuple(
        "Object_csv", ["analiz_object", "sum_inst", "sum_out", "agent", "inn"]
    )
    object_csv = Object_csv(
        "Анализиреумое ООО",
        "Сумма по полю Поступление",
        "Сумма по полю Списание",
        "Контрагент",
        "ИНН",
    )
    building_graphics(data, object_csv, filename_out_html='nx.html')
