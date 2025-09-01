
# Shellcode-Via-Fibers

This is a Proof-of-Concept (PoC) project that demonstrates the execution of encrypted shellcode using **Windows Fibers**.

The primary goal of this project is to showcase a method for loading and executing shellcode that combines encryption and an uncommon execution flow (Fibers) to bypass some basic security detections.

---

## Technical Highlights

- **Dynamic Function Resolution**: Dynamically resolves necessary function addresses from `kernel32.dll` using `GetModuleHandleA` and `GetProcAddress`. This avoids leaving traces in the Import Address Table (IAT), making static analysis more difficult.
- **Shellcode Encryption**: Employs a simple **XOR encryption** to protect the shellcode from being identified by static scanning tools. The key is hardcoded in the program and used for decryption at runtime.
- **Execution via Fibers**:
    - **What are Fibers?**: Fibers are a lightweight execution unit, even more so than threads. A single thread can schedule multiple fibers. Unlike threads, the scheduling of fibers must be explicitly managed by the program.
    - **Why use Fibers?**:
        1.  **Stealth**: Compared to common techniques like `CreateThread` or `CreateRemoteThread`, using Fibers to execute shellcode is a less frequent approach and may evade some EDR/AV products that only monitor thread creation.
        2.  **Control Flow Obfuscation**: Converting the main thread to a fiber, then creating and switching to another fiber containing the shellcode, introduces a control flow switch that can be less intuitive for analysts to follow.
- **Console-less Execution**: Uses `#pragma comment(linker, "/SUBSYSTEM:WINDOWS /ENTRY:mainCRTStartup")` to set the program's entry point, allowing it to run in the background without a console window popping up.

## File Descriptions

- **`main.cpp`**: Contains the C++ loader code. It is responsible for decrypting the encrypted shellcode, allocating executable memory, and using Fibers to execute it.
- **`encrypt.py`**: A Python script designed to XOR encrypt a raw shellcode file (`shellcode.bin`) and output a C/C++ style byte array.

## How to Use

### 1. Generate Shellcode

First, you need to generate your raw shellcode using a tool like Metasploit's `msfvenom`.

For example, the following command generates shellcode that launches `calc.exe` on a 64-bit Windows system and saves it as `shellcode.bin`.

```bash
msfvenom -p windows/x64/exec CMD=calc.exe -f raw -o shellcode.bin
```

### 2. Encrypt the Shellcode

Next, run the `encrypt.py` script to encrypt the `shellcode.bin` file.

**Requirements**:
- Ensure `shellcode.bin` is in the same directory as `encrypt.py`.
- Python must be installed.

Run the script:
```bash
python encrypt.py
```

The script will read `shellcode.bin`, encrypt it with the hardcoded XOR key `0x5A`, and print the resulting C-style array to the console.

You will see output similar to the following:
```
[+] Encryption complete!
[i] Shellcode size: 276 bytes
[i] XOR Key: 0x5a

[*] Copy the following C array into your main.c file:

--------------------------------------------------
unsigned char encryptedShellcode[] = {
    0xa6, 0x12, 0xd9, 0xbe, 0xaa, 0xb2, 0x92, 0x5a, 0x5a, 0x5a, 0x1b, 0x0b, 0x1b, 0x0a, 0x08, 0x0b,
    ... (rest of the array)
};
--------------------------------------------------
```

### 3. Update the Loader Code

Copy the entire `unsigned char encryptedShellcode[]` array generated in the previous step. Open the `main.cpp` file and **replace** the existing `encryptedShellcode` array with the one you just copied.

### 4. Compile
Try to use Visual Studio 2022 to compile it whenever possible.

### 5. Execute

Run the compiled executable. If everything is configured correctly, your shellcode will be executed (e.g., the calculator will launch).

## Disclaimer

This project is intended for academic research and educational purposes only. Do not use this code on any system without proper authorization. The author is not responsible for any misuse or damage caused by this code.
