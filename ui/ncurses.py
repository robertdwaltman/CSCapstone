import curses

class NCurses(object):
    """docstring for NCurses"""
    def __init__(self):
        # Create a curses object
        self.stdscr = curses.initscr()

        # create border and add string
        self.stdscr.border(0)
        self.queryBox = curses.newwin(10, 50, 12, 0)
        self.queryBox.border(0)
        self.stdscr.addstr(11, 25, "cs419 - Group 5")
        self.queryBox.addstr(1, 5, "Enter your query below:")
        self.stdscr.refresh()
        inputString = self.queryBox.getstr(3, 25)
        self.queryBox.addstr(5, 5, "You entered: %s" % inputString)
        self.queryBox.addstr(6, 5, "(Press any key to exit UI)")
        self.queryBox.refresh()

        # Wait for user input and then quit
        self.stdscr.getch()
        curses.endwin()

if __name__ == '__main__':
    cur = NCurses()
