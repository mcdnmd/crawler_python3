"""@package startup
Documentation for startup module.

This is a main module to prepare environment and launch crawler conveyor
"""
import logging
import sys

from modules.Crawler import Crawler
from modules.TerminalParser import TerminalParser
from modules.StateHandler import StateHandler


def main():
    """
    start crawling utility
    """
    logging.getLogger().setLevel(logging.INFO)

    launcher = TerminalParser()
    args = launcher.get_terminal_arguments()
    if args.filters:
        args.filters = launcher.parse_filters(args.filters)

    crawler = choose_script(args.folder,
                            args.update_all,
                            args.url,
                            args.depth,
                            args.max_threads,
                            args.filters)
    crawler.run()


def choose_script(folder, update_all, url, depth, max_threads, filters):
    stateHandler = StateHandler(folder)
    swap_state = stateHandler.load_crawler_state()

    if update_all:
        if swap_state['wasDownloaded']:
            crawler = stateHandler.get_crawler_from_dump()
            crawler.update(swap_state["downloadedTime"])
        else:
            print(f'ERROR: {folder} is empty')
            return
    elif swap_state['downloadRequired']:
        crawler = stateHandler.get_crawler_from_dump()
    else:
        crawler = Crawler(url, folder, depth, max_threads,
                          filters, StateHandler(folder))
    return crawler

if __name__ == '__main__':
    main()
