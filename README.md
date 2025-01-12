# ZipHeader
A small code for parsing zip archive headers and extracting data from them directly. Everything is uploaded to a file for further analysis, headers are saved in byts, hex, ASCII, data is saved in several variants (hex, bit, base64)

Небольшой код для парсинга заголовков zip-архивов и распаковки данных из них напрямую. Все выгружается в файл для дальнейшего анализа, заголовки сохраянются в byts, hex, ASCII, данные сохраняются в нескольких вариантах (hex, bit, base64)

# Install library 
Use pip and python3:
Library: argparse, os, struct, zlib, base64.
For use: `python3 ZIPmain file_path output_file_path extract_to_path`
