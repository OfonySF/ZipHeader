# hex_utils.py
# -*- coding: utf-8 -*-
def file_to_hex(file_path, output_file_path):
    with open(file_path, 'rb') as file:
        content = file.read()

        # Convert content to hex
        hex_content = content.hex()
        formatted_hex = ' '.join(hex_content[i:i + 2] for i in range(0, len(hex_content), 2))
        print("\n\n\n\nHexadecimal format:")
        print(formatted_hex)

        # Convert content to binary
        binary_content = ' '.join(format(byte, '08b') for byte in content)
        print("\nBinary format:")
        print(binary_content)

        return content

