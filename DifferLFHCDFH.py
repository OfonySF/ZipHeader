import re
def extract_CentralDirectoryFileHeader_compression_method(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    compression_method = []
    inside_field = False
    for line in lines:
        if line.startswith('<cdfhst'):
            inside_field = True
        elif line.startswith('<cdfhen'):
            inside_field = False

        if inside_field and 'Compression Method' in line:
            # Extract the compression method value
            method_value = line.split(':')[1].strip().split(' ')[0]
            compression_method.append(method_value)

    return compression_method

def extract_LocalFileHeader_compression_methods(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    compression_methods = []
    inside_field = False
    for line in lines:
        if line.startswith('<lfhst'):
            inside_field = True
        elif line.startswith('<lfhen'):
            inside_field = False

        if inside_field and 'Compression Method' in line:
            # Extract the compression method value
            method_value = line.split(':')[1].strip().split(' ')[0]
            compression_methods.append(method_value)

    return compression_methods


def extract_CentralDirectoryFileHeader_uncompressed_size(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    uncompressed_sizes = []
    in_field = False

    for line in lines:
        # Используем регулярные выражения для поиска тегов с индексами
        if re.search(r'<cdfhst\d+>', line):
            in_field = True
        elif re.search(r'<cdfhen\d+>', line):
            in_field = False

        if in_field and 'Uncompressed Size:' in line:
            # Извлекаем значение после 'Uncompressed Size:'
            parts = line.split('Uncompressed Size:')
            if len(parts) > 1:
                size_str = parts[1].strip().split('(')[0]  # Получаем первую часть до символа '('
                try:
                    size = int(size_str)
                    uncompressed_sizes.append(size)
                except ValueError:
                    print(f"Could not convert {size_str} to an integer.")

    return uncompressed_sizes


def extract_LocalFileHeader_uncompressed_size(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    uncompressed_sizes = []
    in_field = False

    for line in lines:
        # Используем регулярные выражения для поиска тегов с индексами
        if re.search(r'<lfhst\d+>', line):
            in_field = True
        elif re.search(r'<lfhen\d+>', line):
            in_field = False

        if in_field and 'Uncompressed Size:' in line:
            # Извлекаем значение после 'Uncompressed Size:'
            parts = line.split('Uncompressed Size:')
            if len(parts) > 1:
                size_str = parts[1].strip().split('(')[0]  # Получаем первую часть до символа '('
                try:
                    size = int(size_str)
                    uncompressed_sizes.append(size)
                except ValueError:
                    print(f"Could not convert {size_str} to an integer.")

    return uncompressed_sizes