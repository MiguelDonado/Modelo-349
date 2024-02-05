import re

""" IN THE MODELO 349, THERE'RE FOUR TYPES OF SHEETS:
    0 - FRONT PAGE (ALWAYS)
    1 - RESUMEN PAGE (ALWAYS)
    2 - MAIN PAGE (ALWAYS)
    3 - RECTIFICATIVA PAGE (NOT ALWAYS) 
"""

# -----------------------------------------ZERO TYPE SHEET---------------------------------------------------------------------
date_zero_sheet = re.compile(r"\d{2}-\d{2}-\d{4}")

# -----------------------------------------FIRST TYPE SHEET---------------------------------------------------------------------
year_first_sheet = re.compile(r"^20\d{2}", flags=re.MULTILINE)
month_first_sheet = re.compile(r"(\d\w)\s?\n\d+\n\d+(\.|,).*?\n+")
total_first_sheet = re.compile(r"\s([0-9\.]+,\d\d)")

# -----------------------------------------SECOND TYPE SHEET---------------------------------------------------------------------
clave_and_amount_second_sheet = re.compile(r"\s([A-Z])\s([0-9\.]+,\d\d)")
# It returns something like this:
# [('E', '2.291,90'), ('E', '8.520,81'), ('E', '1.640,50'), ('E', '3.430,15'), ('E', '6.798,29'), ('E', '1.888,75'), ('E', '27.145,71'), ('E', '6.107,25')]

# -----------------------------------------THIRD TYPE SHEET---------------------------------------------------------------------
year_month_two_amounts_third_sheet = re.compile(
    r"^\d{4}\s\d{2}\s([0-9\.]+,\d\d)\s([0-9\.]+,\d\d)", flags=re.MULTILINE
)
# It returns something like this:
# ['2021 11 26.869,04 32.151,63', '2021 08 36.246,13 36.332,41', '2022 01 4.984,61 5.285,74']
