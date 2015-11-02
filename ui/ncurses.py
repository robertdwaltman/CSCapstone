import curses
import sys
import os.path


module_path = os.path.abspath(os.path.join(sys.path[0], os.pardir))
sys.path.append(module_path)
from pgdb.pgdb import PgHandler

class NCurses(object):
    """docstring for NCurses"""
    def __init__(self):
        # Create a curses object
        self.stdscr = curses.initscr()
        self.stdscr.border(0)

        # Turn off keyboard echos
        curses.noecho()

        #Turn on arrow keys
        self.stdscr.keypad(1)

        # Get height and width of window
        self.win_height, self.win_width = self.stdscr.getmaxyx()

        # DB handler
        self.db = PgHandler()

        # Print main menu
        self.print_main_menu()
        #self.stdscr.getch()
        curses.endwin()

    # This function clears the screen and rebuilds the border
    def clear_screen(self):
        self.stdscr.clear()
        self.stdscr.border(0)
        self.stdscr.refresh()

    # This function builds the menu and spaces it out evenly
    # and highlights the first option in the list
    def menu_cycle(self, menu_listing, index):
        self.clear_screen()
        ypos = int(self.win_height)/2 - 5
        xpos = int(self.win_width)/2  - 20
        for i, item in enumerate(menu_listing):
            if i == index:
                self.stdscr.addstr(ypos, xpos, item, curses.A_STANDOUT )
            else:
                self.stdscr.addstr(ypos, xpos, item)
            ypos += 2
        self.stdscr.refresh()

    def print_main_menu(self):
        self.clear_screen()
        continue_loop = True
        counter = 0
        options = ["List Table Contents", "Submit SQL Query"]

        # Print menu
        self.menu_cycle(options, 0)

        # Listen for keyboard input. Quit when ESC key is hit
        while continue_loop:
            b = self.stdscr.getch()

            # If a down arrow is entered, highlight the next option in the list (or go to top if at the end of list)
            if b == curses.KEY_DOWN:
                if counter >= len(options)-1:
                    counter = 0
                else:
                    counter += 1
                self.menu_cycle(options, counter)
            # If up arrow is entered, highlight the previous option (or go to the end if at top)
            elif b == curses.KEY_UP:
                if counter <= 0:
                    counter = len(options) - 1
                else:
                    counter -= 1
                self.menu_cycle(options, counter)

            # Right arrow key or enter goes to the next menu
            elif b == curses.KEY_RIGHT or b == curses.KEY_ENTER:
                if counter == 0:
                    self.print_table_names()
                elif counter == 1:
                    self.get_user_query()
                continue_loop = False
            # ESC ascii code is 27. Quit the loop if this is entered
            elif b == 27:
                continue_loop = False

    def print_table_names(self):
        self.clear_screen()
        db_table_results = self.db.list_tables()
        table_names = []
        for item in db_table_results:
            table_names.append(item[0])


        continue_loop = True
        counter = 0
        self.menu_cycle(table_names, 0)
        while continue_loop:
            b = self.stdscr.getch()
            if b == curses.KEY_DOWN:
                if counter >= len(table_names)-1:
                    counter = 0
                else:
                    counter += 1
                self.menu_cycle(table_names, counter)
            elif b == curses.KEY_UP:
                if counter <= 0:
                    counter = len(table_names) -1
                else:
                    counter -= 1
                self.menu_cycle(table_names, counter)
            elif b == curses.KEY_RIGHT or b == curses.KEY_ENTER:
                self.print_table_contents(10, table_names[counter])
                continue_loop = False
            elif b == curses.KEY_LEFT:
                continue_loop = False
                self.print_main_menu()
            elif b == 27:
                continue_loop = False

    def print_table_contents(self, results_per_page, table_name):
        self.clear_screen()
        self.stdscr.addstr((3),(15), "%s" % table_name, curses.A_BOLD | curses.A_UNDERLINE)
        for x in range(0,results_per_page):
            #temp_string = "Place holder for printing %s results for table %s" %(str(results_per_page),table_name)
            temp_string = "%s table item %d" %(table_name,(x+1))
            self.stdscr.addstr((x + 5),(15), temp_string)
        continue_loop = True
        while continue_loop:
            b = self.stdscr.getch()
            if b == curses.KEY_LEFT:
                continue_loop = False
                self.print_table_names()
            elif b == 27:
                continue_loop = False
                curses.endwin()


    def drop_table_menu(self):
        self.clear_screen()
        self.stdscr.addstr(10, 15, "Drop Tables names")

    def get_user_query(self):
        self.clear_screen()
        curses.echo()
        self.queryBox = curses.newwin(10, 50, 12, 0)
        self.queryBox.border(0)
        self.stdscr.addstr(11, 25, "cs419 - Group 5", curses.A_STANDOUT)
        self.queryBox.addstr(1, 5, "Enter your query below:")
        self.stdscr.refresh()
        inputString = self.queryBox.getstr(3, 25)
        self.queryBox.addstr(5, 5, "You entered: %s" % inputString)
        self.queryBox.addstr(6, 5, "(Press any key to exit UI)")
        self.queryBox.refresh()

        # Wait for user input and then quit
        self.stdscr.getch()
        #curses.endwin()

    def query_db(self):
        pass

    def print_sql_results(self, results_per_page):
        pass

if __name__ == '__main__':
    #print os.path.dirname()
    cur = NCurses()
