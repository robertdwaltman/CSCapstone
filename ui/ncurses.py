import curses

class NCurses(object):
    """docstring for NCurses"""
    def __init__(self):
        # Create a curses object
        self.stdscr = curses.initscr()

        # create border and add string
        self.stdscr.border(0)
        self.stdscr.addstr(12, 25, "cs419 - Group 5 (Press any key to exit UI)")
        self.stdscr.refresh()

        # Wait for user input and then quit
        self.stdscr.getch()
        curses.endwin()

if __name__ == '__main__':
    cur = NCurses()
