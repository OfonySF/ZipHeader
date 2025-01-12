import struct

def find_and_print_central_directory_headers(content, output_file_path):
    # Signature for Central Directory File Header
    signature = 0x02014b50
    signature_bytes = signature.to_bytes(4, byteorder='little')
    position = 0
    structure_number = 0

    with open(output_file_path, 'a', encoding='utf-8') as output_file:
        while position != -1:
            position = content.find(signature_bytes, position)
            if position != -1:
                structure_number += 1
                output_file.write(f"<cdfhst{structure_number}>\n")
                print(f"\nCentralDirectoryFileHeader found at position: {position}")

                # Define the structure format for unpacking
                header_format = '<IHHHHHHIIIHHHHHII'
                header_size = struct.calcsize(header_format)

                if position + header_size > len(content):
                    print("Incomplete Central Directory Header found, skipping.")
                    break

                # Extract the header fields
                header_data = content[position:position + header_size]
                unpacked_data = struct.unpack(header_format, header_data)

                # Write the header fields with explanations and hex examples to the file
                output_file.write("CentralDirectoryFileHeader:\n")
                output_file.write(f"  Signature: {hex(unpacked_data[0])} (This is the fixed signature for a Central Directory File Header, always 0x02014b50)\n")
                output_file.write(f"    Hex: {header_data[0:4].hex()} (Bytes: {header_data[0:4]})\n")

                output_file.write(f"  Version Made By: {unpacked_data[1]} (The version of the software that created the file)\n")
                output_file.write(f"    Hex: {header_data[4:6].hex()} (Bytes: {header_data[4:6]})\n")

                output_file.write(f"  Version to Extract: {unpacked_data[2]} (The minimum version needed to extract the file)\n")
                output_file.write(f"    Hex: {header_data[6:8].hex()} (Bytes: {header_data[6:8]})\n")

                output_file.write(f"  General Purpose Bit Flag: {unpacked_data[3]} (Flags that indicate various options, such as encryption or compression)\n")
                output_file.write(f"    Hex: {header_data[8:10].hex()} (Bytes: {header_data[8:10]})\n")

                output_file.write(f"  Compression Method: {unpacked_data[4]} (The method used to compress the file, e.g., 0 for no compression, 8 for deflate)\n")
                output_file.write(f"    Hex: {header_data[10:12].hex()} (Bytes: {header_data[10:12]})\n")

                output_file.write(f"  Modification Time: {unpacked_data[5]} (The last modification time of the file, stored in MS-DOS format)\n")
                output_file.write(f"    Hex: {header_data[12:14].hex()} (Bytes: {header_data[12:14]})\n")

                output_file.write(f"  Modification Date: {unpacked_data[6]} (The last modification date of the file, stored in MS-DOS format)\n")
                output_file.write(f"    Hex: {header_data[14:16].hex()} (Bytes: {header_data[14:16]})\n")

                output_file.write(f"  CRC32: {hex(unpacked_data[7])} (The CRC-32 checksum of the uncompressed file data for integrity verification)\n")
                output_file.write(f"    Hex: {header_data[16:20].hex()} (Bytes: {header_data[16:20]})\n")

                output_file.write(f"  Compressed Size: {unpacked_data[8]} (The size of the compressed file data)\n")
                output_file.write(f"    Hex: {header_data[20:24].hex()} (Bytes: {header_data[20:24]})\n")

                output_file.write(f"  Uncompressed Size: {unpacked_data[9]} (The size of the file data after decompression)\n")
                output_file.write(f"    Hex: {header_data[24:28].hex()} (Bytes: {header_data[24:28]})\n")

                output_file.write(f"  Filename Length: {unpacked_data[10]} (The length of the filename field)\n")
                output_file.write(f"    Hex: {header_data[28:30].hex()} (Bytes: {header_data[28:30]})\n")

                output_file.write(f"  Extra Field Length: {unpacked_data[11]} (The length of the extra field, which may contain additional metadata)\n")
                output_file.write(f"    Hex: {header_data[30:32].hex()} (Bytes: {header_data[30:32]})\n")

                output_file.write(f"  File Comment Length: {unpacked_data[12]} (The length of the file comment field)\n")
                output_file.write(f"    Hex: {header_data[32:34].hex()} (Bytes: {header_data[32:34]})\n")

                output_file.write(f"  Disk Number: {unpacked_data[13]} (The disk number where the file starts)\n")
                output_file.write(f"    Hex: {header_data[34:36].hex()} (Bytes: {header_data[34:36]})\n")

                output_file.write(f"  Internal File Attributes: {unpacked_data[14]} (Attributes that are specific to the file system)\n")
                output_file.write(f"    Hex: {header_data[36:38].hex()} (Bytes: {header_data[36:38]})\n")

                output_file.write(f"  External File Attributes: {unpacked_data[15]} (Attributes that are specific to the file system)\n")
                output_file.write(f"    Hex: {header_data[38:42].hex()} (Bytes: {header_data[38:42]})\n")

                # Check if the unpacked data has the expected number of elements
                if len(unpacked_data) > 16:
                    output_file.write(f"  Local File Header Offset: {unpacked_data[16]} (Offset of the local file header)\n")
                    output_file.write(f"    Hex: {header_data[42:46].hex()} (Bytes: {header_data[42:46]})\n")
                else:
                    output_file.write("  Local File Header Offset: Not available\n")

                # Extract and write the filename, extra field, and file comment if they exist
                filename_start = position + header_size
                filename_end = filename_start + unpacked_data[10]
                filename = content[filename_start:filename_end].decode('utf-8', errors='replace')
                output_file.write(f"  Filename: {filename} (The name of the file stored in the archive)\n")
                output_file.write(f"    Hex: {content[filename_start:filename_end].hex()} (Bytes: {content[filename_start:filename_end]})\n")

                extra_field_start = filename_end
                extra_field_end = extra_field_start + unpacked_data[11]
                extra_field = content[extra_field_start:extra_field_end]
                output_file.write(f"  Extra Field: {extra_field.hex()} (Additional data related to the file, format depends on the application)\n")
                output_file.write(f"    Hex: {extra_field.hex()} (Bytes: {extra_field})\n")

                file_comment_start = extra_field_end
                file_comment_end = file_comment_start + unpacked_data[12]
                file_comment = content[file_comment_start:file_comment_end].decode('utf-8', errors='replace')
                output_file.write(f"  File Comment: {file_comment} (Comment related to the file)\n")
                output_file.write(f"    Hex: {content[file_comment_start:file_comment_end].hex()} (Bytes: {content[file_comment_start:file_comment_end]})\n")

                output_file.write(f"<cdfhen{structure_number}>\n\n\n")

                position = file_comment_end
            else:
                print("No more CentralDirectoryFileHeader found.")
