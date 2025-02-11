import openpyxl
import csv


def read_excel(filename_path: str, file_name_out: str) -> None:
    wb = openpyxl.load_workbook(filename_path)
    sh = wb.active
    with open(file_name_out, "w", encoding="utf-8", newline="") as file:
        data = csv.writer(file)
        for r in sh.rows:
            data.writerow([cell.value for cell in r])


def get_data_csv(filename: str) -> list[dict]:
    with open(filename, "r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)
