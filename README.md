# ZipHeader
A small code for parsing zip archive headers and extracting data from them directly. Everything is uploaded to a file for further analysis, headers are saved in byts, hex, ASCII, data is saved in several variants (hex, bit, base64)

Небольшой код для парсинга заголовков zip-архивов и распаковки данных из них напрямую. Все выгружается в файл для дальнейшего анализа, заголовки сохраянются в byts, hex, ASCII, данные сохраняются в нескольких вариантах (hex, bit, base64)

# Code explorer
*All signatures with corresponding headers are combined into blocks to facilitate further work*

First, the LFH signature is searched for and all headers are extracted.
After that, blocks of compressed data are extracted until the CD signature is encountered (in case of additional blocks, they are also processed)
At the end, the EOD data block is extracted (in addition, ZIP64 EOCD)
Then the cycle continues until the end, to be in the provided ZIP file
Finally, the data is saved in a separate folder in different formats, for further work (values ​​from LFH and CD are used for data decompression)

# Install library 
Use pip and python3:
Library: argparse, os, struct, zlib, base64.
For use: `python3 ZIPmain file_path output_file_path extract_to_path`
