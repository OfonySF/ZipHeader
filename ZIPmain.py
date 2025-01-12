# main.py
# -*- coding: utf-8 -*-
# python ZIPmain.py path_to_zip_file path_to_output_file path_to_extract_directory
import os
import argparse
from hex_utils import file_to_hex
from local_file_header import find_and_print_local_file_headers
from central_directory import find_and_print_central_directory_headers
from eocd import find_and_print_eocd, handle_zip64_eocdl
from DifferLFHCDFH import extract_CentralDirectoryFileHeader_compression_method, extract_LocalFileHeader_compression_methods, extract_LocalFileHeader_uncompressed_size, extract_CentralDirectoryFileHeader_uncompressed_size
from data_utils import find_and_process_data
from spravka import print_local_file_header_info

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process a ZIP file and extract information.')
    parser.add_argument('file_path', type=str, help='Path to the ZIP file')
    parser.add_argument('output_file_path', type=str, help='Path to the output file')
    parser.add_argument('extract_to_path', type=str, help='Path to extract files to')

    # Parse arguments
    args = parser.parse_args()

    # Ensure the extraction directory exists
    os.makedirs(args.extract_to_path, exist_ok=True)

    # Actions on data
    print_local_file_header_info()
    content = file_to_hex(args.file_path, args.output_file_path)
    find_and_print_local_file_headers(content, args.output_file_path)
    find_and_print_central_directory_headers(content, args.output_file_path)
    find_and_print_eocd(content, args.output_file_path)

    # Actions on compression methods
    compression_methods_lfh = extract_LocalFileHeader_compression_methods(args.output_file_path)
    compression_methods_cdfh = extract_CentralDirectoryFileHeader_compression_method(args.output_file_path)

    # Arrays to store indices where compression method is not equal to 8
    lfh_indices_not_equal_8 = []
    cdfh_indices_not_equal_8 = []

    for index, method in enumerate(compression_methods_lfh, start=1):
        if method != "8":
            lfh_indices_not_equal_8.append(index)

    for index, method in enumerate(compression_methods_cdfh, start=1):
        if method != "8":
            cdfh_indices_not_equal_8.append(index)

    # Check if compression methods match at corresponding indices
    for index in set(lfh_indices_not_equal_8).intersection(cdfh_indices_not_equal_8):
        if compression_methods_lfh[index - 1] != compression_methods_cdfh[index - 1]:
            print(f"Несоответствие метода сжатия на индексе {index}: lfh = {compression_methods_lfh[index - 1]}, cdfh = {compression_methods_cdfh[index - 1]}")

    compression = []

    # Determine length for iteration
    max_length = max(len(compression_methods_lfh), len(compression_methods_cdfh))

    for i in range(max_length):
        # Get values from both arrays, use None if index is out of bounds
        lfh_value = compression_methods_lfh[i] if i < len(compression_methods_lfh) else None
        cdfh_value = compression_methods_cdfh[i] if i < len(compression_methods_cdfh) else None

        if lfh_value == cdfh_value:
            compression.append(lfh_value)
        else:
            compression.append(0)

    print("Объединенный массив compression:", compression)

    # Actions on uncompressed sizes
    uncompressed = []
    uncompressed_local = extract_LocalFileHeader_uncompressed_size(args.output_file_path)
    uncompressed_central = extract_CentralDirectoryFileHeader_uncompressed_size(args.output_file_path)
    for index, (size_local, size_central) in enumerate(zip(uncompressed_local, uncompressed_central), start=1):
        if size_local != size_central:
            print(f"Warning: Different uncompressed sizes at index {index}: LocalFileHeader size = {size_local}, CentralDirectoryFileHeader size = {size_central}")
            uncompressed.append(0)
        else:
            uncompressed.append(size_local)
    print("Объединенный массив uncompressed size:", uncompressed)

    # Start extraction process
    combined = list(zip(compression, uncompressed))
    find_and_process_data(args.output_file_path, combined, args.extract_to_path)

if __name__ == '__main__':
    main()
