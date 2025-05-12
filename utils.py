# Copyright (c) 2025 nggit

import os
import socket


def iter_files(path, extensions=('.gen.txt',)):
    if os.path.isfile(path):
        for ext in extensions:
            if path.endswith(ext.lower()):
                yield path
                break

        return

    with os.scandir(path) as entries:
        for entry in entries:
            yield from iter_files(entry.path, extensions)


def parse_file(path):
    with open(path, 'rb') as file:
        result = bytearray()

        for line in file:
            if line.startswith(b'#'):
                continue

            result.extend(line.rstrip(b'\r\n')
                          .decode('unicode_escape').encode('latin-1'))
            result.extend(b' ')

        return result[:-1]


def send_data(host, port, data=b'', max_retries=10):
    if max_retries <= 0:
        raise ValueError('max_retries is exceeded, or it cannot be negative')

    with socket.create_connection((host, port)) as sock:
        try:
            sock.sendall(data)

            while True:
                chunk = sock.recv(4096)
                if not chunk:
                    break

                yield chunk
        except OSError:
            print('send_data: retry:', max_retries)
            yield from send_data(
                host, port, data, max_retries=max_retries - 1
            )
