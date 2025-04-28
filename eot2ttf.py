import struct
import sys
from pathlib import Path

def eot_to_ttf(eot_path, ttf_path):
    try:
        eot_data = Path(eot_path).read_bytes()
        if len(eot_data) < 66:
            raise ValueError("EOT file is too small to contain a valid header")
        eot_size, font_data_size, version, flags = struct.unpack('<IIII', eot_data[0:16])
        if eot_size != len(eot_data):
            raise ValueError(f"EOT size mismatch: header says {eot_size}, file is {len(eot_data)}")
        if font_data_size > eot_size:
            raise ValueError(f"Font data size {font_data_size} exceeds EOT size {eot_size}")
        supported_versions = (0x00010000, 0x00020000, 0x00020001)
        if version not in supported_versions:
            raise ValueError(f"Unsupported EOT version {hex(version)}")
        if flags != 0:
            raise ValueError("Flags indicate compression or other features not supported by this script")
        fixed_header_size = 54 
        offset = fixed_header_size
        if len(eot_data) < offset + 8:
            raise ValueError("EOT file too small to contain name size fields")
        family_name_size = struct.unpack('<H', eot_data[offset:offset+2])[0]
        offset += 2
        style_name_size = struct.unpack('<H', eot_data[offset:offset+2])[0]
        offset += 2
        version_name_size = struct.unpack('<H', eot_data[offset:offset+2])[0]
        offset += 2
        full_name_size = struct.unpack('<H', eot_data[offset:offset+2])[0]
        offset += 2
        root_string_size = 0
        if version == 0x00020001:
            if len(eot_data) < offset + 2:
                raise ValueError("EOT file too small to contain RootString size")
            root_string_size = struct.unpack('<H', eot_data[offset:offset+2])[0]
            offset += 2
        header_size = (fixed_header_size +
                       2 + family_name_size +  
                       2 + style_name_size +  
                       2 + version_name_size + 
                       2 + full_name_size +   
                       (2 + root_string_size if version == 0x00020001 else 0)) 
        expected_header_size = eot_size - font_data_size
        if header_size != expected_header_size:
            header_size = expected_header_size
        if header_size < 66:
            raise ValueError(f"Header size {header_size} is too small for a valid EOT header")
        if header_size > eot_size:
            raise ValueError(f"Header size {header_size} exceeds EOT size {eot_size}")
        if header_size + font_data_size > eot_size:
            raise ValueError(f"Header size {header_size} plus font data size {font_data_size} "
                             f"exceeds EOT size {eot_size}")
        ttf_data = eot_data[header_size:header_size + font_data_size]
        if len(ttf_data) != font_data_size:
            raise ValueError(f"Extracted TTF data size {len(ttf_data)} does not match "
                             f"expected {font_data_size}")
        if len(ttf_data) < 12:
            raise ValueError("Extracted TTF data is too small to be a valid font")
        Path(ttf_path).write_bytes(ttf_data)

    except FileNotFoundError:
        print(f"Error: File {eot_path} not found.")
        sys.exit(1)
    except struct.error as e:
        print(f"Error: Invalid EOT header structure: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error during conversion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python eot2ttf.py input.eot output.ttf")
        sys.exit(1)
    eot_to_ttf(sys.argv[1], sys.argv[2])






# import struct
# import sys
# from pathlib import Path

# def eot_to_ttf(eot_path, ttf_path):
#     try:
#         # Read EOT file
#         eot_data = Path(eot_path).read_bytes()

#         # Parse EOT header
#         if len(eot_data) < 66:
#             raise ValueError("EOT file is too small to contain a valid header")
#         eot_size, font_data_size, version, flags = struct.unpack('<IIII', eot_data[0:16])

#         # Debugging: Print version, flags, and sizes
#         print(f"EOT Version: {hex(version)}")
#         print(f"Flags: {hex(flags)}")
#         print(f"EOT Size: {eot_size}, Font Data Size: {font_data_size}")

#         # Validate sizes
#         if eot_size != len(eot_data):
#             raise ValueError(f"EOT size mismatch: header says {eot_size}, file is {len(eot_data)}")
#         if font_data_size > eot_size:
#             raise ValueError(f"Font data size {font_data_size} exceeds EOT size {eot_size}")

#         # Support version 0x00020001 alongside 0x00010000 and 0x00020000
#         supported_versions = (0x00010000, 0x00020000, 0x00020001)
#         if version not in supported_versions:
#             raise ValueError(f"Unsupported EOT version {hex(version)}")

#         # Check flags (warn if compression or other features are present)
#         if flags != 0:
#             raise ValueError("Flags indicate compression or other features not supported by this script")

#         # Calculate header size dynamically
#         # Fixed portion of header (up to naming fields) for version 0x00020000/0x00020001
#         fixed_header_size = 54  # Up to FullNameSize field
#         if len(eot_data) < fixed_header_size + 12:  # Enough for name size fields
#             raise ValueError("EOT file too small to contain naming fields")

#         # Parse name field sizes (each is a 2-byte unsigned short)
#         offset = fixed_header_size
#         family_name_size = struct.unpack('<H', eot_data[offset:offset+2])[0]
#         offset += 2
#         style_name_size = struct.unpack('<H', eot_data[offset:offset+2])[0]
#         offset += 2
#         version_name_size = struct.unpack('<H', eot_data[offset:offset+2])[0]
#         offset += 2
#         full_name_size = struct.unpack('<H', eot_data[offset:offset+2])[0]
#         offset += 2

#         # Calculate total header size
#         header_size = (fixed_header_size +
#                        2 + family_name_size +  # FamilyNameSize + FamilyName
#                        2 + style_name_size +   # StyleNameSize + StyleName
#                        2 + version_name_size + # VersionNameSize + VersionName
#                        2 + full_name_size)     # FullNameSize + FullName

#         # Validate header size
#         if header_size > eot_size:
#             raise ValueError(f"Calculated header size {header_size} exceeds EOT size {eot_size}")
#         if header_size + font_data_size > eot_size:
#             raise ValueError(f"Header size {header_size} plus font data size {font_data_size} exceeds EOT size {eot_size}")

#         # Extract TTF data
#         ttf_data = eot_data[header_size:header_size + font_data_size]

#         # Validate TTF data
#         if len(ttf_data) != font_data_size:
#             raise ValueError(f"Extracted TTF data size {len(ttf_data)} does not match expected {font_data_size}")
#         if len(ttf_data) < 12:  # Minimum size for a valid TTF header
#             raise ValueError("Extracted TTF data is too small to be a valid font")

#         # Write TTF file
#         Path(ttf_path).write_bytes(ttf_data)
#         print(f"Successfully converted {eot_path} to {ttf_path}")

#     except FileNotFoundError:
#         print(f"Error: File {eot_path} not found.")
#         sys.exit(1)
#     except struct.error as e:
#         print(f"Error: Invalid EOT header structure: {e}")
#         sys.exit(1)
#     except ValueError as e:
#         print(f"Error: {e}")
#         sys.exit(1)
#     except Exception as e:
#         print(f"Unexpected error during conversion: {e}")
#         sys.exit(1)

# if __name__ == "__main__":
#     if len(sys.argv) != 3:
#         print("Usage: python eot2ttf.py input.eot output.ttf")
#         sys.exit(1)
#     eot_to_ttf(sys.argv[1], sys.argv[2])
    
    
    
    

# import struct
# import sys

# def eot_to_ttf(eot_path, ttf_path):
#     try:
#         # Read EOT file
#         with open(eot_path, 'rb') as f:
#             eot_data = f.read()

#         # Parse EOT header
#         eot_size = struct.unpack('<I', eot_data[0:4])[0]
#         font_data_size = struct.unpack('<I', eot_data[4:8])[0]
#         version = struct.unpack('<I', eot_data[8:12])[0]
#         flags = struct.unpack('<I', eot_data[12:16])[0]

#         # Check version and flags (basic validation)
#         if version not in (0x00010000, 0x00020000):
#             raise ValueError("Unsupported EOT version")
#         if flags != 0:
#             print("Warning: Flags indicate compression or other features not handled here")

#         # Assume header size (simplified; adjust based on actual EOT spec)
#         header_size = 66  # Minimal header size for version 0x00020000 without names

#         # Extract TTF data
#         ttf_data = eot_data[header_size:header_size + font_data_size]

#         # Write TTF file
#         with open(ttf_path, 'wb') as f:
#             f.write(ttf_data)
#         print(f"Successfully converted {eot_path} to {ttf_path}")
#     except FileNotFoundError:
#         print(f"Error: File {eot_path} not found.")
#     except Exception as e:
#         print(f"Error during conversion: {e}")

# if __name__ == "__main__":
#     if len(sys.argv) != 3:
#         print("Usage: python eot2ttf.py input.eot output.ttf")
#         sys.exit(1)
#     eot_to_ttf(sys.argv[1], sys.argv[2])