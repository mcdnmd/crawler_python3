"""@package startup
Documentation for startup module.

This is a main module to prepare environment and launch crawler conveyor
"""

from modules.Crawler import Crawler
from modules.TerminalParser import TerminalParser
from modules.StateHandler import StateHandler


def main():
    """
    start crawling utility
    """
    launcher = TerminalParser()
    args = launcher.get_terminal_arguments()
    if args.filters:
        args.filters = launcher.parse_filters(args.filters)

    stateHandler = StateHandler(args.folder)
    swap_state = stateHandler.load_crawler_state()

    if swap_state['downloadRequired']:
        crawler = stateHandler.get_crawler_from_dump()
    else:
        crawler = Crawler(args.url, args.folder, args.depth, args.max_threads,
                          args.filters, StateHandler(args.folder))
    crawler.run()


if __name__ == '__main__':
    main()
