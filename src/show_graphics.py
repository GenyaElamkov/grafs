from collections import namedtuple
from pyvis.network import Network


def building_graphics(
    data: list[dict], object_csv: namedtuple, filename_out_html: str
) -> None:
    nt = Network(directed=True, height=1000, filter_menu=True)
    # filter_menu - верхнее меню для фильров

    counter = 0
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

        description = f"ИНН: {row[object_csv.inn]}\nКонтрагент: {row[object_csv.agent]}"
        if sum_admission != 0:
            counter += 1
            nt.add_node(
                counter,
                label=f"Сумма: {sum_admission}\n{description}",
                group=2,
                size=10,
            )
            nt.add_edge(counter, id_key)

        if sum_write_off != 0:
            counter += 3
            nt.add_node(
                counter,
                label=f"Сумма: {sum_write_off}\n{description}",
                group=3,
                size=10,
            )
            nt.add_edge(id_key, counter)

    nt.repulsion(node_distance=200, spring_length=250)
    nt.set_edge_smooth("dynamic")
    # nt.toggle_physics(False)
    nt.barnes_hut(overlap=1)
    nt.show_buttons(filter_=["nodes", "edges"])
    nt.show(filename_out_html, notebook=False)


if __name__ == "__main__":
    from read_csv import get_data_csv

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
    building_graphics(data, object_csv, filename_out_html="nx.html")
