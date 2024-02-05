from intro_func import get_pdf_files, read_pdf, create_row_dictionary
from logic import (
    extract_data_based_on_type_page,
    put_in_desired_format_dict,
    clean_bases_third_page,
    clean_clave_and_amount,
)
from output import write_to_xlsx


def main():
    pdf_files = get_pdf_files()
    rows = []
    if len(pdf_files) > 1:
        for file in pdf_files:
            row = create_row_dictionary()
            text_file = read_pdf(file)
            for page in text_file:
                provisional_row = extract_data_based_on_type_page(page)
                if provisional_row:
                    for key, value in provisional_row.items():
                        row[key].extend(value)
                        """It extends the value of the provisional_row 
                        to the value of the row as it is."""
                provisional_row = None
            rows.append(prepare_to_append(row))
            row = None
    elif len(pdf_files) == 1:
        text_file = read_pdf(pdf_files[0])
        row = create_row_dictionary()
        for page in text_file:
            provisional_row = extract_data_based_on_type_page(page)
            if (
                list(provisional_row.keys())[0] == "Fecha presentacion"
                and row["Ejercicio"]
            ):
                rows.append(prepare_to_append(row))
                row = None
                row = create_row_dictionary()
            for key, value in provisional_row.items():
                row[key].extend(value)
                """It extends the value of the provisional_row 
                    to the value of the row as it is."""
            provisional_row = None
        rows.append(prepare_to_append(row))
    write_to_xlsx(rows)


def prepare_to_append(row):
    row["Clave_amount"] = clean_clave_and_amount(row["Clave_amount"])
    """At first row["Clave_amount"] is a list of lists of tuples.
    After, row["Clave_amount"] is a dictionary that contains as values
    the total amount for each key {'A': 2.291, 'E': 8.520, 'I': 1.640, 'S': 3.430}."""
    row["Base Imponible Rectificada"] = clean_bases_third_page(
        row["Base Imponible Rectificada"]
    )
    """At first row["Base Imponible Rectificada"] is a list of numbers stored as strings.
    After, row["Base Imponible Rectificada"] is a float (sum of all the numbers in the list)."""
    row["Base Imponible Declarada Anteriormente"] = clean_bases_third_page(
        row["Base Imponible Declarada Anteriormente"]
    )
    """At first row["Base Imponible Declarada Anteriormente"] is a list of numbers stored as strings.
    After, row["Base Imponible Declarada Anteriormente"] is a float (sum of all the numbers in the list)."""
    return put_in_desired_format_dict(row)


if __name__ == "__main__":
    main()
