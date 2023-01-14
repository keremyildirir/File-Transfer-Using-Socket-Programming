import socket
import tqdm
import os
import argparse
from cryptography.fernet import Fernet


SEPARATOR = "<SEPARATOR>"

BUFFER_SIZE = 1024 * 4


def send_file(filename, host, port):
    # get the file size
    filesize = os.path.getsize(filename)
    # create the client socket
    s = socket.socket()
    print(f"[+] Connecting to {host}:{port}")
    s.connect((host, port))
    print("[+] Connected.")

    # create key from the value at filekey
    with open("filekey.key", "rb") as filekey:
        key = filekey.read()

    # create fernet key for symetric encryption
    fernet = Fernet(key)

    s.send(f"{filename}{SEPARATOR}{filesize}".encode())

    # start sending the file
    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        while True:
            # read the bytes from the file
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                break
            #update progress bar
            progress.update(len(bytes_read))
            bytes_read = fernet.encrypt(bytes_read)
            s.sendall(bytes_read)

    # close the socket
    s.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="File Transfer")
    parser.add_argument("file", help="File name to send")
    args = parser.parse_args()
    filename = args.file
    host = "3.83.178.221"
    port = 11467
    send_file(filename, host, port)