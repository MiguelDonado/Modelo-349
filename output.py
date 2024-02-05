from openpyxl import Workbook


def write_to_xlsx(meses):
    """The argument is a list with 12 dictionaries. Each dictionary is a month.
    Example of variable meses:
    [{"Fecha presentacion": ["17-03-2022"],"Ejercicio": ["2022"],"Periodo": ["02"],  "Total": ["957170.96"],
    "Base Imponible Rectificada": 68099.78, "Base Imponible Declarada Anteriormente": 73769.78,
    "A": 915587.22, "E": 67.18, "I": 41516.56, "S": 0.0}, ... 12 times]
    Each dictionary will contain always the same keys. For instance, even though on the pdf doesn't appear
    sometimes the value of the "S", on the dictionary it will appear with the value 0.0.
    """

    wb = Workbook()
    ws = wb.active
    headers = list(meses[0].keys())
    # headers = ['Fecha presentacion', 'Ejercicio', 'Periodo', 'Total', 'Base Imponible Rectificada',
    # 'Base Imponible Decla...eriormente', 'A', 'E', 'I', 'S']
    ws.append(headers)
    for mes in meses:
        mes = list(mes.values())
        # mes = [['17-03-2022'], ['2022'], ['02'], ['957170.96'], 68099.78, 73769.78000000001, 915587.22, 67.18, 41516.56, 0.0]
        flat_row = []
        for item in mes:
            if isinstance(item, list):
                flat_row.extend(item)
            else:
                flat_row.append(item)
        # flat_row = ['17-03-2022', '2022', '02', '957170.96', 68099.78, 73769.78000000001, 915587.22, 67.18, 41516.56, 0.0]
        ws.append(flat_row)
    wb.save("Modelo 349.xlsx")
