# -*- coding: utf-8 -*-
import zlib
import base64
import os

def process_data(data, is_compressed, uncompressed_size, index, output_dir):
    if not is_compressed:
        # Если сжатие не применяется, данные уже в нужном формате
        uncompressed_data = data
    else:
        # Данные сжаты методом deflate
        try:
            uncompressed_data = zlib.decompress(data, -zlib.MAX_WBITS, uncompressed_size)
        except zlib.error as e:
            print(f"\nDecompression error: {e}\n")
            return

    # Выгружаем данные в различных форматах
    with open(os.path.join(output_dir, f"Data{index}.txt"), 'w') as file:
        # Битовый формат
        bit_format = ''.join(format(byte, '08b') for byte in uncompressed_data)
        file.write(f"<bitst{index}>\n{bit_format}\n<biten{index}>\n\n\n")

        # Hex формат
        hex_format = uncompressed_data.hex()
        file.write(f"<hexst{index}>\n{hex_format}\n<hexen{index}>\n\n\n")

        # Base64 формат
        base64_format = base64.b64encode(uncompressed_data).decode('utf-8')
        file.write(f"<base64st{index}>\n{base64_format}\n<base64en{index}>\n\n\n")
    print("Данные внутри zip выгружены")
    # Сохраняем данные в битовом формате в отдельный файл без расширения
    with open(os.path.join(output_dir, f"Data{index}"), 'wb') as file:
        file.write(uncompressed_data)
    print("Данные внутри zip выгружены в отдельный файл")

def find_and_process_data(file_path, compression_info, output_dir):
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
    except IOError:
        print("Failed to open file.")
        return

    deflate = False
    index = 1
    while True:
        # Формируем теги для поиска данных
        start_tag = f"<dtst{index}>".encode()
        end_tag = f"<dten{index}>".encode()

        # Ищем позиции начала и конца данных
        start_pos = content.find(start_tag)
        end_pos = content.find(end_tag)

        # Если не найдено, выходим из цикла
        if start_pos == -1 or end_pos == -1:
            break

        # Извлекаем данные между тегами
        start_pos += len(start_tag)
        hex_data = content[start_pos:end_pos]

        try:
            # Декодируем данные из hex в байты
            data = bytes.fromhex(hex_data.decode())
        except ValueError:
            print(f"Failed to decode hex data between {start_tag.decode()} and {end_tag.decode()}\n")
            index += 1
            continue

        # Вывод данных в консоль
        print(f"Data between {start_tag.decode()} and {end_tag.decode()}:\n {data}\n")

        # Получаем метод сжатия и размер данных для текущего индекса
        if index - 1 < len(compression_info):
            method, size = compression_info[index - 1]
            if method == '8':
                print('Compression Method is deflate\n\n')
                deflate = True
                process_data(data, deflate, size, index, output_dir)
            else:
                print('Compression Method is not deflate (доработка)\n\n')
                deflate = False
                process_data(data, deflate, size, index, output_dir)
        else:
            print(f"No compression info available for index {index}\n")

        # Переходим к следующему индексу
        deflate = False
        index += 1






