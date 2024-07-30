import base64
import os
import subprocess
import tempfile
import sys

def encode_elf_to_base64(file_path):
    """
    Encodes the ELF file to base64.

    :param file_path: Path to the ELF file
    :return: Base64 encoded data
    """
    try:
        with open(file_path, 'rb') as f:
            return base64.b64encode(f.read())
    except Exception as e:
        print(f"Error encoding file: {e}")
        sys.exit(1)

def decode_base64_to_file(encoded_data, file_path):
    """
    Decodes base64 data to a file.

    :param encoded_data: Base64 encoded data
    :param file_path: Path to save the decoded file
    """
    try:
        with open(file_path, 'wb') as f:
            f.write(base64.b64decode(encoded_data))
    except Exception as e:
        print(f"Error decoding file: {e}")
        sys.exit(1)

def execute_elf_from_memory(encoded_data):
    """
    Executes an ELF file from memory.

    :param encoded_data: Base64 encoded ELF data
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file_path = tmp_file.name
            decode_base64_to_file(encoded_data, tmp_file_path)
            os.chmod(tmp_file_path, 0o755)  # Ensure the file is executable
            subprocess.run([tmp_file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing file: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path_to_elf_file>")
        sys.exit(1)

    elf_file_path = sys.argv[1]
    if not os.path.isfile(elf_file_path):
        print(f"Error: File '{elf_file_path}' not found.")
        sys.exit(1)

    encoded_data = encode_elf_to_base64(elf_file_path)
    execute_elf_from_memory(encoded_data)
