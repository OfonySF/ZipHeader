import struct

def check_and_process_descriptor(content, position, header_size, unpacked_data, structure_number, output_file):
    # Calculate data descriptor
    data_size = unpacked_data[7] if unpacked_data[3] != 0 else unpacked_data[8]
    data_start = position + header_size
    data_end = data_start + data_size

    # Check for the presence of the 0x08074b50 signature
    descriptor_signature = 0x08074b50
    descriptor_position = content.find(descriptor_signature.to_bytes(4, byteorder='little'), data_end)
    if descriptor_position != -1:
        data_end = descriptor_position + 4  # Move to the end of the descriptor signature
    else:
        print("Descriptor signature not found, proceeding to read data descriptors.")

    # Read data descriptor
    descriptor_format = '<III'
    descriptor_size = struct.calcsize(descriptor_format)
    descriptor_data = content[data_end:data_end + descriptor_size]

    if len(descriptor_data) < descriptor_size:
        raise ValueError(f"Expected {descriptor_size} bytes for descriptor, but got {len(descriptor_data)}")

    crc32, compressed_size, uncompressed_size = struct.unpack(descriptor_format, descriptor_data)

    output_file.write(f"\n<dtdst{structure_number}>\n")
    output_file.write(f"  Data Descriptor:\n")
    output_file.write(f"    CRC-32: {crc32}\n")
    output_file.write(f"    Compressed Size: {compressed_size}\n")
    output_file.write(f"    Uncompressed Size: {uncompressed_size}\n")
    output_file.write(f"\n<dtden{structure_number}>\n")

    # Update position to the end of the data descriptor
    new_position = data_end + descriptor_size

    # Prepare to read the first bit after the data descriptor
    if new_position < len(content):
        next_byte = content[new_position]
        print(f"First byte after data descriptor: {next_byte}")

    return new_position
