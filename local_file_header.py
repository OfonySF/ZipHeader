# local_file_header.py
# -*- coding: utf-8 -*-
import struct
from descriptor import check_and_process_descriptor
def find_and_print_local_file_headers(content, output_file_path):
    signature = 0x04034b50
    signature_bytes = signature.to_bytes(4, byteorder='little')
    position = 0
    structure_number = 0

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        while position != -1:
            position = content.find(signature_bytes, position)
            if position != -1:
                structure_number += 1
                output_file.write(f"<lfhst{structure_number}>\n")
                print(f"\nЗаголовок локального файла найден на позиции: {position}")

                header_format = '<IHHHHHIIIHH'
                header_size = struct.calcsize(header_format)

                if position + header_size > len(content):
                    print("Неполный заголовок локального файла найден, пропускаем.")
                    break

                header_data = content[position:position + header_size]
                unpacked_data = struct.unpack(header_format, header_data)

                output_file.write("LocalFileHeader:\n")
                output_file.write(
                    f"  Signature: {hex(unpacked_data[0])} (Это фиксированная подпись для заголовка локального файла, всегда 0x04034b50)\n")
                output_file.write(f"    Hex: {header_data[0:4].hex()} (Байты: {header_data[0:4]})\n")
                output_file.write(f"    Bits: {format(unpacked_data[0], '032b')}\n")

                output_file.write(
                    f"  Version to Extract: {unpacked_data[1]} (Минимальная версия, необходимая для извлечения файла)\n")
                output_file.write(f"    Hex: {header_data[4:6].hex()} (Байты: {header_data[4:6]})\n")
                output_file.write(f"    Bits: {format(unpacked_data[1], '016b')}\n")

                output_file.write(
                    f"  General Purpose Bit Flag: {unpacked_data[2]} (Флаги, указывающие на различные параметры, такие как шифрование или сжатие)\n")
                output_file.write(f"    Hex: {header_data[6:8].hex()} (Байты: {header_data[6:8]})\n")
                output_file.write(f"    Bits: {format(unpacked_data[2], '016b')}\n")

                output_file.write(
                    f"  Compression Method: {unpacked_data[3]} (Метод, используемый для сжатия файла, например, 0 для отсутствия сжатия, 8 для deflate)\n")
                output_file.write(f"    Hex: {header_data[8:10].hex()} (Байты: {header_data[8:10]})\n")
                output_file.write(f"    Bits: {format(unpacked_data[3], '016b')}\n")

                output_file.write(
                    f"  Modification Time: {unpacked_data[4]} (Время последнего изменения файла, сохраненного в формате MS-DOS)\n")
                output_file.write(f"    Hex: {header_data[10:12].hex()} (Байты: {header_data[10:12]})\n")
                output_file.write(f"    Bits: {format(unpacked_data[4], '016b')}\n")

                output_file.write(
                    f"  Modification Date: {unpacked_data[5]} (Дата последнего изменения файла, сохраненного в формате MS-DOS)\n")
                output_file.write(f"    Hex: {header_data[12:14].hex()} (Байты: {header_data[12:14]})\n")
                output_file.write(f"    Bits: {format(unpacked_data[5], '016b')}\n")

                output_file.write(
                    f"  CRC32: {hex(unpacked_data[6])} (Контрольная сумма CRC-32 данных несжатого файла для проверки целостности)\n")
                output_file.write(f"    Hex: {header_data[14:18].hex()} (Байты: {header_data[14:18]})\n")
                output_file.write(f"    Bits: {format(unpacked_data[6], '032b')}\n")

                output_file.write(f"  Compressed Size: {unpacked_data[7]} (Размер сжатого файла данных)\n")
                output_file.write(f"    Hex: {header_data[18:22].hex()} (Байты: {header_data[18:22]})\n")
                output_file.write(f"    Bits: {format(unpacked_data[7], '032b')}\n")

                output_file.write(f"  Uncompressed Size: {unpacked_data[8]} (Размер данных файла после распаковки)\n")
                output_file.write(f"    Hex: {header_data[22:26].hex()} (Байты: {header_data[22:26]})\n")
                output_file.write(f"    Bits: {format(unpacked_data[8], '032b')}\n")

                output_file.write(f"  Filename Length: {unpacked_data[9]} (Длина поля имени файла)\n")
                output_file.write(f"    Hex: {header_data[26:28].hex()} (Байты: {header_data[26:28]})\n")
                output_file.write(f"    Bits: {format(unpacked_data[9], '016b')}\n")

                output_file.write(
                    f"  Extra Field Length: {unpacked_data[10]} (Длина дополнительного поля, которое может содержать дополнительную метаинформацию)\n")
                output_file.write(f"    Hex: {header_data[28:30].hex()} (Байты: {header_data[28:30]})\n")
                output_file.write(f"    Bits: {format(unpacked_data[10], '016b')}\n")

                filename_start = position + header_size
                filename_end = filename_start + unpacked_data[9]
                filename = content[filename_start:filename_end].decode('utf-8', errors='replace')
                output_file.write(f"  Filename: {filename} (Имя файла, сохраненного в архиве)\n")
                output_file.write(
                    f"    Hex: {content[filename_start:filename_end].hex()} (Байты: {content[filename_start:filename_end]})\n")

                extra_field_start = filename_end
                extra_field_end = extra_field_start + unpacked_data[10]
                extra_field = content[extra_field_start:extra_field_end]
                output_file.write(
                    f"  Extra Field: {extra_field.hex()} (Дополнительные данные, связанные с файлом, формат зависит от приложения)\n")
                output_file.write(f"    Hex: {extra_field.hex()} (Байты: {extra_field})\n")

                output_file.write(f"<lfhen{structure_number}>\n\n\n")

                data_size = unpacked_data[7] if unpacked_data[3] != 0 else unpacked_data[8]
                data_start = extra_field_end
                data_end = data_start + data_size

                output_file.write(f"\n<dtst{structure_number}>\n")
                data_hex = content[data_start:data_end].hex()
                output_file.write(data_hex)
                output_file.write(f"\n<dten{structure_number}>\n\n\n")


                position = data_end
                if unpacked_data[2] & (1 << 3):
                    check_and_process_descriptor(content, position, header_size, unpacked_data, structure_number,
                                                     output_file)
        else:
                print("Больше заголовков локальных файлов не найдено.")
