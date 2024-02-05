import os
from PyPDF2 import PdfReader


def get_pdf_files():
    # Get all the pdf files in the current directory
    pdf_files = [f for f in os.listdir(".") if f.endswith(".pdf")]
    return pdf_files


def read_pdf(file):
    # create a pdf file object
    pdfFileObj = open(file, "rb")

    # create a pdf reader object
    pdf_reader = PdfReader(pdfFileObj)

    # extract text from each page
    text_pages = [page.extract_text() for page in pdf_reader.pages]
    pdfFileObj.close()
    return text_pages
    # text_pages is a list. Each element of the list is a string with the text of each page.


def create_row_dictionary():
    row = {
        "Fecha presentacion": [],
        "Ejercicio": [],
        "Periodo": [],
        "Total": [],
        "Clave_amount": [],
        "Base Imponible Rectificada": [],
        "Base Imponible Declarada Anteriormente": [],
    }
    return row
