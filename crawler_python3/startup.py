ERROR_PYTHON_VERSION = 3

import sys

if sys.version_info < (3, 7):
    print('Use python >= 3.7', file=sys.stderr)
    sys.exit(ERROR_PYTHON_VERSION)

from modules import crawler

MAX_DEPTH = 5
VISITED = set()


def main(argv):
    global MAX_DEPTH
    if len(argv) == 3:
        try:
            link = str(argv[0])
            directory = str(argv[1])
            MAX_DEPTH = int(argv[2])
        except ValueError as e:
            return sys.exit(e)
    elif len(argv) == 1 and argv[0] == "-h":
        print('To launch crawler use: startup.py '
              '<start_url> <dir_to_upload> <depth>')
        sys.exit()
    c = crawler.Crawler(link, directory)
    c.run()


if __name__ == '__main__':
    main(sys.argv[1:])
