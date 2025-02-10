from collections import namedtuple
from pyvis.network import Network


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

    id_counter = 0
    for row in data:
        try:
            sum_admission = round(float(row[object_csv.sum_inst]), 2)
        except ValueError:
            sum_admission = 0

        try:
            sum_write_off = round(float(row[object_csv.sum_out]), 2)
        except ValueError:
            sum_write_off = 0

        id_key = row[object_csv.analiz_object]
        nt.add_node(id_key, label=id_key, group=1, font={"size": 30}, size=50)

        # Добавляем ноды — входящие суммы.
        description = f"ИНН: {row[object_csv.inn]}\nКонтрагент: {row[object_csv.agent]}"
        coordinate_y -= coordinate_one_Node
        if sum_admission != 0:
            id_counter += 1
            nt.add_node(
                id_counter,
                label=f"Сумма: {sum_admission}\n{description}",
                group=2,
                size=10,
                x=coordinate_x,
                y=coordinate_y,
                physics=False,
            )
            nt.add_edge(id_counter, id_key)

        # Добавляем ноды — исходящие суммы.
        if sum_write_off != 0:
            id_counter += 3
            nt.add_node(
                id_counter,
                label=f"Сумма: {sum_write_off}\n{description}",
                group=3,
                size=10,
                x=-coordinate_x,
                y=coordinate_y,
                physics=False,
            )
            nt.add_edge(id_key, id_counter)

    nt.repulsion(node_distance=200, spring_length=250)
    nt.set_edge_smooth("dynamic")
    # nt.toggle_physics(False)
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
    building_graphics(data, object_csv, filename_out_html="nx.html")
