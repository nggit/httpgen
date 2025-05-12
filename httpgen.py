#!/usr/bin/env python
# Copyright (c) 2025 nggit

import sys

from utils import iter_files, parse_file, send_data


def main(host, port=80, path='data'):
    for filepath in iter_files(path):
        data = parse_file(filepath)

        print('-->', filepath)
        print(str(data)[:256], '[...]' if len(data) > 256 else '')
        print('<--')

        try:
            for chunk in send_data(host, port, data):
                print(chunk.decode(), end='')

            print('⏎')
        except (ConnectionError, OSError) as exc:
            return f'Failed to connect to {host} port {port}: {str(exc)}'


if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:]))
