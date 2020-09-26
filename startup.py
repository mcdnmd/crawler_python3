"""@package startup
Documentation for startup module.

This is a main module to prepare environment and launch crawler conveyor
"""

ERROR_PYTHON_VERSION = 3

import sys

if sys.version_info < (3, 8):
    print('Use python >= 3.8', file=sys.stderr)
    sys.exit(ERROR_PYTHON_VERSION)

from modules.Crawler import Crawler
from modules.TerminalParser import TerminalParser
from modules.SafeStates import StateHandler


def main():
    """
    start crawling utility
    """
    launcher = TerminalParser()
    args = launcher.get_terminal_arguments()

    stateHandler = StateHandler(args.folder)
    swop_state = stateHandler.load_crawler_state()

    if swop_state is not None and swop_state['needSwop'] is True:
        crawler = stateHandler.get_crawler_from_dump()
    else:
        crawler = Crawler(args.url,
                          args.folder,
                          args.depth,
                          args.max_threads,
                          StateHandler(args.folder))
    crawler.run()


if __name__ == '__main__':
    main()
