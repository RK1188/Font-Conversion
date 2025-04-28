import struct
import sys
from pathlib import Path

def ttf_to_eot_with_template(template_eot_path, ttf_path, output_eot_path):
    template = Path(template_eot_path).read_bytes()
    eot_size, font_data_size = struct.unpack('<II', template[0:8])
    header_len = eot_size - font_data_size
    header = bytearray(template[:header_len])
    ttf_data = Path(ttf_path).read_bytes()
    new_font_size = len(ttf_data)
    new_eot_size = header_len + new_font_size
    header[0:4] = struct.pack('<I', new_eot_size)  
    header[4:8] = struct.pack('<I', new_font_size)
    output_data = header + ttf_data
    Path(output_eot_path).write_bytes(output_data)
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python ttf2eot.py template.eot input.ttf output.eot")
        sys.exit(1)
    _, tpl, ttf, out = sys.argv
    try:
        ttf_to_eot_with_template(tpl, ttf, out)
    except FileNotFoundError as e:
        print(f"File not found: {e.filename}")
    except Exception as exc:
        print(f"Error: {exc}")










# import struct
# import sys

# def ttf_to_eot(ttf_path, eot_path):
#     try:
#         # Read TTF file
#         with open(ttf_path, 'rb') as f:
#             ttf_data = f.read()

#         # Hardcoded placeholder values for EOT header fields
#         family_name = "PlaceholderFamily".encode('utf-16-le') + b'\x00\x00'
#         style_name = "Regular".encode('utf-16-le') + b'\x00\x00'
#         version_name = "Version 1.0".encode('utf-16-le') + b'\x00\x00'
#         full_name = "PlaceholderFamily Regular".encode('utf-16-le') + b'\x00\x00'

#         # Calculate lengths for name fields
#         family_name_size = len(family_name)
#         style_name_size = len(style_name)
#         version_name_size = len(version_name)
#         full_name_size = len(full_name)

#         # Construct EOT header
#         eot_header = bytearray()
#         eot_header += struct.pack('<I', 0)  # EOTSize (placeholder)
#         eot_header += struct.pack('<I', len(ttf_data))  # FontDataSize
#         eot_header += struct.pack('<I', 0x00020000)  # Version
#         eot_header += struct.pack('<I', 0x00000000)  # Flags (no compression)

#         # FontPANOSE (10 bytes, hardcoded to zeros)
#         eot_header += b'\x00' * 10

#         # Charset (ANSI_CHARSET)
#         eot_header += struct.pack('<B', 0x00)

#         # Italic, Weight, fsType, MagicNumber
#         eot_header += struct.pack('<B', 0x00)  # Italic (not italic)
#         eot_header += struct.pack('<H', 400)   # Weight (normal)
#         eot_header += struct.pack('<H', 0x0000)  # fsType
#         eot_header += struct.pack('<H', 0x504C)  # MagicNumber (fixed value)

#         # UnicodeRange (16 bytes, hardcoded to zeros)
#         eot_header += b'\x00' * 16

#         # CodePageRange (8 bytes, hardcoded to zeros)
#         eot_header += b'\x00' * 8

#         # CheckSumAdjustment (hardcoded to zero)
#         eot_header += struct.pack('<I', 0x00000000)

#         # Reserved fields (4 bytes, set to zero)
#         eot_header += b'\x00' * 4

#         # Padding (2 bytes)
#         eot_header += b'\x00\x00'

#         # FamilyNameSize and FamilyName
#         eot_header += struct.pack('<H', family_name_size)
#         eot_header += family_name

#         # StyleNameSize and StyleName
#         eot_header += struct.pack('<H', style_name_size)
#         eot_header += style_name

#         # VersionNameSize and VersionName
#         eot_header += struct.pack('<H', version_name_size)
#         eot_header += version_name

#         # FullNameSize and FullName
#         eot_header += struct.pack('<H', full_name_size)
#         eot_header += full_name

#         # Combine header and TTF data
#         eot_data = eot_header + ttf_data

#         # Update EOTSize with the total length
#         eot_size = len(eot_data)
#         eot_data[0:4] = struct.pack('<I', eot_size)

#         # Write EOT file
#         with open(eot_path, 'wb') as f:
#             f.write(eot_data)
#         print(f"Successfully converted {ttf_path} to {eot_path}")
#     except FileNotFoundError:
#         print(f"Error: File {ttf_path} not found.")
#     except Exception as e:
#         print(f"Error during conversion: {e}")

# if __name__ == "__main__":
#     if len(sys.argv) != 3:
#         print("Usage: python ttf2eot.py input.ttf output.eot")
#         sys.exit(1)
#     ttf_to_eot(sys.argv[1], sys.argv[2])