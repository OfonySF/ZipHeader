# eocd.py
# -*- coding: utf-8 -*-
import struct

def find_and_print_eocd(content, output_file_path):
    signature = 0x06054b50
    signature_bytes = signature.to_bytes(4, byteorder='little')
    position = content.find(signature_bytes)

    if position != -1:
        with open(output_file_path, 'a', encoding='utf-8') as output_file:
            output_file.write("<eocdst>\n")
            print(f"\nEOCD found at position: {position}\n\n")

            eocd_format = '<IHHHHLLH'
            eocd_size = struct.calcsize(eocd_format)

            if position + eocd_size > len(content):
                print("Incomplete EOCD found, skipping.")
                return

            eocd_data = content[position:position + eocd_size]
            unpacked_data = struct.unpack(eocd_format, eocd_data)

            output_file.write("EOCD:\n")
            output_file.write(f"  Signature: {hex(unpacked_data[0])} (This is the fixed signature for EOCD, always 0x06054b50)\n")
            output_file.write(f"    Hex: {eocd_data[0:4].hex()} (Bytes: {eocd_data[0:4]})\n")

            output_file.write(f"  Disk Number: {unpacked_data[1]} (The disk number where this EOCD record is located)\n")
            output_file.write(f"    Hex: {eocd_data[4:6].hex()} (Bytes: {eocd_data[4:6]})\n")

            output_file.write(f"  Start Disk Number: {unpacked_data[2]} (The disk number where the central directory starts)\n")
            output_file.write(f"    Hex: {eocd_data[6:8].hex()} (Bytes: {eocd_data[6:8]})\n")

            output_file.write(f"  Number of Central Directory Records on this Disk: {unpacked_data[3]}\n")
            output_file.write(f"    Hex: {eocd_data[8:10].hex()} (Bytes: {eocd_data[8:10]})\n")

            output_file.write(f"  Total Number of Central Directory Records: {unpacked_data[4]}\n")
            output_file.write(f"    Hex: {eocd_data[10:12].hex()} (Bytes: {eocd_data[10:12]})\n")

            output_file.write(f"  Size of Central Directory: {unpacked_data[5]} (The size of the central directory in bytes)\n")
            output_file.write(f"    Hex: {eocd_data[12:16].hex()} (Bytes: {eocd_data[12:16]})\n")

            output_file.write(f"  Central Directory Offset: {unpacked_data[6]} (Offset of the start of the central directory)\n")
            output_file.write(f"    Hex: {eocd_data[16:20].hex()} (Bytes: {eocd_data[16:20]})\n")

            output_file.write(f"  Comment Length: {unpacked_data[7]} (The length of the comment field)\n")
            output_file.write(f"    Hex: {eocd_data[20:22].hex()} (Bytes: {eocd_data[20:22]})\n")

            comment_start = position + eocd_size
            comment_end = comment_start + unpacked_data[7]
            comment = content[comment_start:comment_end].decode('utf-8', errors='replace')
            output_file.write(f"  Comment: {comment} (The comment for the ZIP file)\n")
            output_file.write(f"    Hex: {content[comment_start:comment_end].hex()} (Bytes: {content[comment_start:comment_end]})\n")
            output_file.write("<eocden>\n\n\n")

            # Check for ZIP64 EOCD Locator
            if (unpacked_data[1] == 0xFFFF or unpacked_data[2] == 0xFFFF or
                unpacked_data[3] == 0xFFFF or unpacked_data[4] == 0xFFFF or
                unpacked_data[5] == 0xFFFFFFFF or unpacked_data[6] == 0xFFFFFFFF):
                print("ZIP64 End Of Central Directory Locator detected.")
                # Call the module or function to handle ZIP64 EOCD Locator
                handle_zip64_eocdl(content, position)
            else:
                print("ZIP64 End Of Central Directory Locator not detected.\n\n")

    else:
        print("EOCD signature not found.")


def handle_zip64_eocdl(content, position):
    # Define the format of the EOCD64 Locator
    eocd64_locator_format = '<IQLI'
    eocd64_locator_size = struct.calcsize(eocd64_locator_format)

    if position + eocd64_locator_size > len(content):
        print("Incomplete ZIP64 EOCD Locator found, skipping.")
        return

    # Extract EOCD64 Locator data from the content
    eocd64_locator_data = content[position:position + eocd64_locator_size]
    unpacked_data = struct.unpack(eocd64_locator_format, eocd64_locator_data)

    # Unpack the data
    signature, disk_number, eocd64_offset, total_disk_count = unpacked_data

    # Check the signature
    if signature != 0x07064b50:
        print("Invalid ZIP64 EOCD Locator signature.")
        return

    # Print information about the ZIP64 EOCD Locator
    print("ZIP64 EOCD Locator found:")
    print(f"  Signature: {hex(signature)}")
    print(f"  Disk Number: {disk_number}")
    print(f"  EOCD64 Offset: {eocd64_offset}")
    print(f"  Total Disk Count: {total_disk_count}")

    # Now handle the ZIP64 Extended Information
    # Assuming the ZIP64 EOCD is located at eocd64_offset
    zip64_eocd_format = '<QQLQ'
    zip64_eocd_size = struct.calcsize(zip64_eocd_format)

    if eocd64_offset + zip64_eocd_size > len(content):
        print("Incomplete ZIP64 EOCD found, skipping.")
        return

    zip64_eocd_data = content[eocd64_offset:eocd64_offset + zip64_eocd_size]
    unpacked_zip64_data = struct.unpack(zip64_eocd_format, zip64_eocd_data)

    # Unpack the ZIP64 EOCD data
    uncompressed_size, compressed_size, local_file_header_offset, disk_number = unpacked_zip64_data

    # Print the ZIP64 Extended Information
    print("ZIP64 Extended Information:")
    print(f"  Uncompressed Size: {uncompressed_size}")
    print(f"  Compressed Size: {compressed_size}")
    print(f"  Local File Header Offset: {local_file_header_offset}")
    print(f"  Disk Number: {disk_number}")




