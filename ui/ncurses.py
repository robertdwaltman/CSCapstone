import curses

class NCurses(object):
    """docstring for NCurses"""
    def __init__(self):
        # Create a curses object
        self.menu_options = {
            "main":   ["List Table Contents", "Drop Table"],


        }
        self.stdscr = curses.initscr()
        self.stdscr.keypad(1)

        # create border and add string
        self.stdscr.border(0)
        self.queryBox = curses.newwin(10, 50, 12, 0)
        self.queryBox.border(0)
        self.stdscr.addstr(11, 25, "cs419 - Group 5", curses.A_STANDOUT)


        # Wait for user input and then quit
        self.print_main_menu()
        #self.stdscr.getch()
        curses.endwin()

    def clear_screen(self):
        self.stdscr.clear()
        self.stdscr.border(0)


    def menu_cycle(self, menu_listing, index):
        self.clear_screen()
        ypos = 10
        for i, item in enumerate(menu_listing):
            if i == index:
                self.stdscr.addstr(ypos, 25, item, curses.A_STANDOUT )
            else:
                self.stdscr.addstr(ypos, 25, item)
            ypos += 2



    def print_main_menu(self):
        self.clear_screen()
        continue_loop = True
        counter = 0
        options = ["List Table Contents", "Drop Table"]
        self.menu_cycle(options, 0)
        while continue_loop:
            b = self.stdscr.getch()
            if b == curses.KEY_DOWN:
                if counter >= len(options)-1:
                    counter = 0
                else:
                    counter += 1
                self.menu_cycle(options, counter)
            elif b == curses.KEY_UP:
                if counter <= 0:
                    counter = len(options) -1
                else:
                    counter -= 1
                self.menu_cycle(options, counter)
            elif b == curses.KEY_RIGHT or b == curses.KEY_ENTER:
                if counter == 0:
                    self.print_table_names()
                elif counter == 1:
                    self.drop_table_menu()
                continue_loop = False
            elif b == 27:
                continue_loop = False

                #curses.endwin()


    def print_table_names(self):
        self.clear_screen()
        temp_table_names = ["stuff", "more stuff", "extra stuff"]
        continue_loop = True
        counter = 0
        self.menu_cycle(temp_table_names, 0)
        while continue_loop:
            b = self.stdscr.getch()
            if b == curses.KEY_DOWN:
                if counter >= len(temp_table_names)-1:
                    counter = 0
                else:
                    counter += 1
                self.menu_cycle(temp_table_names, counter)
            elif b == curses.KEY_UP:
                if counter <= 0:
                    counter = len(temp_table_names) -1
                else:
                    counter -= 1
                self.menu_cycle(temp_table_names, counter)
            elif b == curses.KEY_RIGHT or b == curses.KEY_ENTER:
                if counter == 0:
                    self.print_table_names()
                elif counter == 1:
                    self.drop_table_menu()
                continue_loop = False
            elif b == curses.KEY_LEFT:
                continue_loop = False
                self.print_main_menu()

            elif b == 27:
                continue_loop = False

        c = self.stdscr.getch()

    def print_table_contents(self, results_per_page, table_name):
        pass

    def drop_table_menu(self):
        self.clear_screen()
        self.stdscr.addstr(10, 15, "Drop Tables names")

    def print_sql_menu(self):
        pass

    def get_user_query(self):
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
        curses.endwin()

    def query_db(self):
        pass

    def print_sql_results(self, results_per_page):
        pass



if __name__ == '__main__':
    cur = NCurses()
