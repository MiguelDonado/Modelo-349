# Model 349 Extractor

This Python project is designed to process PDF files of the Spanish tax form "Modelo 349", extract specific data from them, and output the results to an Excel file.

## Files

- **definitive.py**: This is the main script that orchestrates the entire process. It uses functions from other modules to read PDF files, extract data, and write the results to an Excel file.

- **intro_func.py**: This module contains utility functions for reading PDF files and preparing data structures.

- **logic.py**: This module contains logic for processing the data extracted from the PDF files.

- **output.py**: This module contains functions for writing the processed data to an Excel file.

- **support_regex.py**: This module contains support functions for regular expressions.

## Usage

To run the project, execute the `definitive.py` script. The script will process all PDF files in the current directory and write the results to an Excel file.

```sh
python definitive.py
```