import re
import itertools
from support_regex import (
    date_zero_sheet,
    year_first_sheet,
    month_first_sheet,
    total_first_sheet,
    clave_and_amount_second_sheet,
    year_month_two_amounts_third_sheet,
)

""" KEYWORDS TO KNOW IN WHICH TYPE OF PAGE WE ARE
    0 - PRESENTACIÓN REALIZADA
    1 - RECAPITULATIVA
    2 - RELACIÓN DE OPERACIONES
    3 - DECLARADA ANTERIORMENTE
"""


def extract_data_based_on_type_page(text_page):
    """Given the text of a page, through conditional statements, we detect in which type of page we are.
    The keywords that i use in the conditional statements exists only in one type of page.
    Once i know in which type of page i am, i extract the data that i need from that page and return it in a dictionary.
    """
    if "Presentación realizada" in text_page:
        row = {}
        date = date_zero_sheet.search(text_page).group(
            0
        )  # group(0) returns the whole match
        # Ex. date = '17-03-2022'
        row["Fecha presentacion"] = [date]
    elif "recapitulativa" in text_page:
        row = {}
        year = year_first_sheet.search(text_page).group(0)
        month = month_first_sheet.search(text_page).group(1)
        # group(1) returns the first capture group
        total = total_first_sheet.search(text_page).group(1)
        total = float(total.replace("\n", "").replace(".", "").replace(",", "."))
        # Ex. year = '2022', month = '02', total = '957170.96'
        row["Ejercicio"] = [year]
        row["Periodo"] = [month]
        row["Total"] = [total]
    elif "Relación de operaciones" in text_page:
        row = {}
        clave_and_amount = clave_and_amount_second_sheet.findall(text_page)
        """clave_and_amount is a list of tuples. It finds all the matches of the regex in the text_page.
        Ex. [('A', '419.430,81'), ('A', '3.222,77'), ('A', '6.384,00'), ('A', '1.258,40'), 
        ('A', '2.932,00'), ('A', '232.113,31'), ('A', '54.239,07'), ('A', '4.426,50')]
        The findall() method returns a list of all matches of the regular expression in the string. 
        If the regular expression has groups, findall() returns a list of tuples 
        where each tuple contains the groups of one match."""
        row["Clave_amount"] = [clave_and_amount]
    elif "declarada anteriormente" in text_page:
        row = {}
        year_month_two_amounts = year_month_two_amounts_third_sheet.findall(text_page)
        # Ex. year_month_two_amounts = [('26.869,04', '32.151,63'), ('36.246,13', '36.332,41')]
        row["Base Imponible Rectificada"] = [
            amount[0] for amount in year_month_two_amounts
        ]
        # Ex. row["Base Imponible Rectificada"] = ['26.869,04', '36.246,13', '4.984,61']
        row["Base Imponible Declarada Anteriormente"] = [
            amount[1] for amount in year_month_two_amounts
        ]
        # Ex. row["Base Imponible Declarada Anteriormente"] = ['32.151,63', '36.332,41', '5.285,74']
    else:
        return None
    return row


def clean_clave_and_amount(clave_and_amount):
    # Primarily it clean, put in the desired format the value of the row["Clave_amount"].
    # Clave_and_amount is a list of lists of tuples. Ex. [[(),(),...],...] -> [[(A, 0,00),(E, 0,00),...],...]
    # First we flat the data structure, to obtain only a list of tuples.
    # Then we add the keys all the keys, just in case that anyone doesn't appear on the PDF,
    # to make sure that in the future when writing to xlsx, all the rows will have the same headers.
    desired_clave_amount = [item for sublist in clave_and_amount for item in sublist]
    desired_clave_amount.append(("E", "0,00"))
    desired_clave_amount.append(("A", "0,00"))
    desired_clave_amount.append(("S", "0,00"))
    desired_clave_amount.append(("I", "0,00"))
    desired_clave_amount = [
        (i[0], float(i[1].replace(".", "").replace(",", ".")))
        for i in desired_clave_amount
    ]
    desired_clave_amount.sort(key=lambda x: x[0])
    desired_clave_amount = [
        (k, sum(i[1] for i in g))
        for k, g in itertools.groupby(desired_clave_amount, key=lambda x: x[0])
    ]
    desired_clave_amount = {k: v for k, v in desired_clave_amount}
    # Example desired_clave_amount = {'A': 2.291, 'E': 8.520, 'I': 1.640, 'S': 3.430}
    return desired_clave_amount


def clean_bases_third_page(bases_list):
    # Ex. bases_list = ['26.869,04', '36.246,13', '4.984,61']
    # If the list is empty, it returns 0.0
    final_bases = float(
        sum([float(num.replace(".", "").replace(",", ".")) for num in bases_list])
    )
    # Ex. final_bases = 6799.78
    return final_bases


def put_in_desired_format_dict(row):
    """Ex. row = {'Fecha presentacion': ['17-03-2022'], 'Ejercicio': ['2022'], 'Periodo': ['02'], 'Total': ['957170.96'],
    'Clave_amount': {'A': 2.291, 'E': 8.520, 'I': 1.640, 'S': 3.430}, 'Base Imponible Rectificada': 68099.78,
    'Base Imponible Declarada Anteriormente': 73769.78}"""
    new_row = row.copy()  # Create a copy of the row
    clave_amount = new_row.pop(
        "Clave_amount"
    )  # Remove the 'Clave_amount' key and get its value
    for key, value in clave_amount.items():
        new_row[key] = (
            value  # Add the keys and values from 'Clave_amount' to the new row
        )
    # Ex. new_row = {'Fecha presentacion': ['17-03-2022'], 'Ejercicio': ['2022'], 'Periodo': ['02'], 'Total': ['957170.96'],
    # 'Base Imponible Rectificada': 68099.78, 'Base Imponible Declarada Anteriormente': 73769.78, 'A': 2.291, 'E': 8.520,
    # 'I': 1.640, 'S': 3.430}
    return new_row
