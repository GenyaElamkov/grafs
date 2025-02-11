from collections import namedtuple
from pyvis.network import Network


def format_number(num: float) -> str:
    return f"{'{0:,}'.format(round(num)).replace(',', ' ')} ₽"


def format_description(agent: str, inn: str, num_text: str) -> str:
    """
    Функция для форматирования описания контрагента с указанием ИНН и суммы.

    Параметры:
    agent (str): наименование контрагента.
    inn (str): ИНН контрагента.
    num_text (str): текстовое представление суммы, связанной с контрагентом.

    Возвращает:
    str: отформатированное описание контрагента с указанием ИНН и суммы.
    """
    description = f"Контрагент: {agent}\nИНН: {inn}"
    return f"{description}\nСумма: {num_text}"


def sorted_table_csv(data: list[dict], field_name: str, reverse=False) -> list[dict]:
    """Сортировка данных по определенныму полю"""
    return sorted(
        data,
        key=lambda x: 0 if not x[field_name] else float(x[field_name]),
        reverse=reverse,
    )


def building_graphics(
    data: list[dict], object_csv: namedtuple, filename_out_html: str
) -> None:
    height = len(data) * 70  # Высота графика, Оптимально 70px для одного Node
    nt = Network(directed=True, height=height, filter_menu=True)
    # filter_menu - верхнее меню для фильров

    # Координаты для Node
    coordinate_y: int = height
    coordinate_one_Node = height / len(data)
    coordinate_x = 500

    id = 0
    for row in data:
        try:
            sum_admission = format_number(float(row[object_csv.sum_inst]))
        except ValueError:
            sum_admission = 0

        try:
            sum_write_off = format_number(float(row[object_csv.sum_out]))
        except ValueError:
            sum_write_off = 0

        id_key = row[object_csv.analiz_object]
        nt.add_node(id_key, label=id_key, group=1, font={"size": 30}, size=50)

        # Добавляем ноды — входящие суммы.
        coordinate_y -= coordinate_one_Node
        if sum_admission != 0:
            id += 1
            id_sum_admission = id
            nt.add_node(
                id,
                label=format_description(
                    row[object_csv.agent], row[object_csv.inn], sum_admission
                ),
                group=2,
                size=10,
                x=-coordinate_x,
                y=coordinate_y,
                physics=False,
            )
            nt.add_edge(id, id_key)

        # Добавляем ноды — исходящие суммы.
        if sum_write_off != 0:
            id += 2
            nt.add_node(
                id,
                label=format_description(
                    row[object_csv.agent], row[object_csv.inn], sum_write_off
                ),
                group=3,
                size=10,
                x=coordinate_x,
                y=coordinate_y,
                physics=False,
            )
            nt.add_edge(id_key, id)

    nt.repulsion(node_distance=200, spring_length=250)
    nt.set_edge_smooth("dynamic")
    nt.barnes_hut(overlap=1)

    # Показываем настройки внизу экрана.
    nt.show_buttons(filter_=["nodes", "edges"])
    nt.show(filename_out_html, notebook=False)


if __name__ == "__main__":
    import configparser
    from read_csv import get_data_csv

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
    data = sorted_table_csv(data, field_name=object_csv.sum_inst)
    building_graphics(data, object_csv, filename_out_html="nx.html")
    # print(type(format_number(num=24141247.83)))
