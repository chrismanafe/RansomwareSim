# RansomwareSim

## Overview
RansomwareSim is a simulated ransomware application developed for educational and training purposes. It is designed to demonstrate how ransomware encrypts files on a system and communicates with a command-and-control server. This tool is strictly for educational use and should not be used for malicious purposes.

## Features
- Encrypts specified file types within a target directory.
- Creates&Delete a README file on the desktop with a simulated ransom note.
- Simulates communication with a command-and-control server to send system data and receive a decryption key.
- Decrypts files after receiving the correct key.

## Usage
**`Important`:** This tool should only be used in controlled environments where all participants have given consent. Do not use this tool on any system without explicit permission. For more, read [SECURE](SECURITY.md)

## Requirements

- Python 3.x
- cryptography
- colorama

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/HalilDeniz/RansomwareSim.git
   ```

2. Navigate to the project directory:

   ```shell
   cd RansomwareSim
   ```

3. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

### Running the Control Server
1. Start the server by running `ControlServer.py`.
2. The server will listen for connections from `Messenger` on specified port (default: 12345).

### Sending encryption command to Control Server
1. Run `Messenger.py` to start the encryption process.
2. Change relevant argument as needed through arg parser e.g.: `python Messenger.py --server_host 192.168.64.2`


### Sending decryption command to Control Server
1. Run `Messenger.py` to start the decryption process.
2. Change `cmd` argument and specify key to decrypt files. e.g.: `python Messenger.py --cmd dec --key abcdefgh...`

## Disclaimer
RansomwareSim is developed for educational purposes only. The creators of RansomwareSim are not responsible for any misuse of this tool. This tool should not be used in any unauthorized or illegal manner. Always ensure ethical and legal use of this tool.

## License
RansomwareSim is released under the [MIT License](LICENSE). See LICENSE for more information.

  
