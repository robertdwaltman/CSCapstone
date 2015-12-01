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
        # Hide Cursor
        curses.curs_set(0)

        #Turn on arrow keys
        self.stdscr.keypad(1)

        # Get height and width of window
        self.win_height, self.win_width = self.stdscr.getmaxyx()

        # DB handler
        self.db = PgHandler()

        # Print main menu
        self.print_intro()
        curses.endwin()

    # This function clears the screen and rebuilds the border
    def clear_screen(self):
        self.stdscr.clear()
        self.stdscr.border(0)
        self.stdscr.refresh()

    # This function builds the menu and spaces it out evenly
    # and highlights the first option in the list
    def menu_cycle1(self, menu_listing, index):
        self.clear_screen()

        # Get screen size and calculate the distance
        # from the edge of the screen
        ypos = int(self.win_height)/2 - 5
        xpos = int(self.win_width)/2 - 20

        # Iterate over the list of menu items.
        # Highlight the selected index/item
        for i, item in enumerate(menu_listing):
            if i == index:
                self.stdscr.addstr(ypos, xpos, item, curses.A_STANDOUT )
            else:
                self.stdscr.addstr(ypos, xpos, item)
            ypos += 2
        ypos += 5
        xpos = xpos - 6
        self.stdscr.addstr(ypos, xpos, "Press enter to select menu option or escape to quit.")
        self.stdscr.refresh()
		
    def menu_cycle2(self, menu_listing, index):
        self.clear_screen()

	    # Get screen size and calculate the distance
	    # from the edge of the screen
        ypos = int(self.win_height)/2 - 5
        xpos = int(self.win_width)/2 - 20

	    # Iterate over the list of menu items.
	    # Highlight the selected index/item
        for i, item in enumerate(menu_listing):
            if i == index:
                self.stdscr.addstr(ypos, xpos, item, curses.A_STANDOUT )
            else:
                self.stdscr.addstr(ypos, xpos, item)
            ypos += 2
        ypos += 3
        xpos -= 10
        self.stdscr.addstr(ypos, xpos, "Press enter to select table or escape to go back to menu select.")
        self.stdscr.refresh()

    def print_intro(self):
        self.clear_screen()
        height = self.win_height/2
        width = self.win_width/2
        introBox = curses.newwin(15, 50, height-6, width-25)
        introBox.border(0)
        introBox.addstr(1, 14, "cs419 - Group 5", curses.A_BOLD | curses.A_UNDERLINE)
        introBox.addstr(4, 14, "Jon Derderian")
        introBox.addstr(5, 14, "Ashok Nayar")
        introBox.addstr(6, 14, "Robert Waltman")
        introBox.addstr(8, 4, "Press enter to continue or escape to quit.", curses.A_STANDOUT)

        introBox.refresh()
        continue_loop = True
        while continue_loop:
            b = self.stdscr.getch()
            if b == curses.KEY_RIGHT or b == 10:
                continue_loop = False
                self.print_main_menu()
            elif b == 27:
                continue_loop = False
                curses.endwin()

    def print_main_menu(self):
        self.clear_screen()
        continue_loop = True
        counter = 0
        options = ["List Table Contents", "Submit SQL Query"]
        groupIdBox = curses.newwin(20, 5, 1, 1)
        groupIdBox.border(0)
        groupIdBox.refresh()
        self.stdscr.refresh()
        # Print menu
        self.menu_cycle1(options, 0)

        # Listen for keyboard input. Quit when ESC key is hit
        while continue_loop:
            b = self.stdscr.getch()

            # If a down arrow is entered, highlight the next option in the list (or go to top if at the end of list)
            if b == curses.KEY_DOWN:
                if counter >= len(options)-1:
                    counter = 0
                else:
                    counter += 1
                self.menu_cycle1(options, counter)
            # If up arrow is entered, highlight the previous option (or go to the end if at top)
            elif b == curses.KEY_UP:
                if counter <= 0:
                    counter = len(options) - 1
                else:
                    counter -= 1
                self.menu_cycle1(options, counter)

            # Right arrow key or enter goes to the next menu
            elif b == curses.KEY_RIGHT or b == 10:
                if counter == 0:
                    self.print_table_names()
                elif counter == 1:
                    self.get_user_query()
                continue_loop = False
            # ESC ascii code is 27. Quit the loop if this is entered
            elif b == 27:
                continue_loop = False
                #clears window then closes program, as it took multiple ESC presses to quit program
                curses.endwin()
                sys.exit(0)
            groupIdBox.refresh()

    def print_table_names(self):
        self.clear_screen()
        # Get the table names form DB
        self.db.get_all_tables()
        # Get the first set of names
        table_names = self.db.get_next_table_names()
        continue_loop = True
        counter = 0

        # Print the menu and select the first table name
        self.menu_cycle2(table_names, 0)
        while continue_loop:
            b = self.stdscr.getch()
            if b == curses.KEY_DOWN:
                if counter >= len(table_names)-1:
                    counter = 0
                else:
                    counter += 1
                self.menu_cycle2(table_names, counter)
            elif b == curses.KEY_UP:
                if counter <= 0:
                    counter = len(table_names) -1
                else:
                    counter -= 1
                self.menu_cycle2(table_names, counter)
            elif b == curses.KEY_RIGHT:
                table_names = self.db.get_next_table_names()
                self.menu_cycle(table_names, 0)
            elif b == curses.KEY_LEFT:
                table_names = self.db.get_prev_table_names()
                self.menu_cycle2(table_names, 0)
            elif b == 10:
                self.print_table_contents(10, table_names[counter])
            elif b == 27:
                continue_loop = False
                self.print_main_menu()

    def print_table_contents(self, results_per_page, table_name):
        self.clear_screen()
        #title_string = "%s" %(table_name)
        #self.stdscr.addstr(2, 15, title_string, curses.A_BOLD | curses.A_UNDERLINE)
        #self.stdscr.refresh()

        self.db.get_table_results(table_name)
        current_results = self.db.get_next_results()

        continue_loop = True
        selection_index = 1
        if not current_results:
            self.stdscr.addstr(1, 2, "This table is empty! Press any key to return to the previous menu.")
            self.stdscr.getch()
            self.print_table_names()
            continue_loop = False
        self.print_sql_results(current_results, 1)
        while continue_loop:
            b = self.stdscr.getch()
            if b == curses.KEY_LEFT:
                current_results = self.db.get_prev_results()
                selection_index = 1
                self.print_sql_results(current_results, selection_index)
            elif b == curses.KEY_RIGHT:
                current_results = self.db.get_next_results()
                selection_index = 1
                self.print_sql_results(current_results, selection_index)
            elif b == curses.KEY_UP:
                if current_results:
                    selection_index -=1
                    if selection_index < 1:
                        selection_index = len(current_results)
                    self.print_sql_results(current_results, selection_index)
            elif b == curses.KEY_DOWN:
                if current_results:
                    selection_index += 1
                    if selection_index > len(current_results):
                        selection_index = 1
                    self.print_sql_results(current_results, selection_index)
            elif b == 10:
                self.print_row_details(current_results[selection_index-1])
            elif b == 27:
                continue_loop = False
                #self.print_sql_results(current_results, 1)
                self.print_table_names()

    def print_row_details(self, row):
        self.clear_screen()
        curses.curs_set(0)
        columns = self.db.get_returned_columns()
        resultsBox = curses.newwin(self.win_height-2, self.win_width-2, 1, 1)
        #resultsBox.border(0)
        x = 1
        for index, item in enumerate(row):
            detail_str = "%s : %s" %(columns[index], item)
            position = resultsBox.getyx()
            x = position[0] + 1
            resultsBox.addstr(x, 2, detail_str)
            x += 1
        #currently, left arrow returns to table, one previous page, right arrow returns to table forward one page
        #up arrow returns to same page but moves the highlighted row up one, and down arrow moves the highlighted row down one
        resultsBox.addstr(19, 15, "Press any arrow key to go back to table.")
        resultsBox.addstr(20, 15, "Press escape to go back to table selection.")
        resultsBox.refresh()

    def drop_table_menu(self):
        self.clear_screen()
        self.stdscr.addstr(10, 15, "Drop Tables names")

    def get_user_query(self):
        self.clear_screen()
        curses.echo()
        curses.curs_set(1)
        current_results = None
        selection_index = 0
        errors = False
        self.queryBox = curses.newwin(self.win_height/4, self.win_width-2,(self.win_height - self.win_height/4)-1,1 )
        self.queryBox.border(0)

        self.stdscr.addstr(10, 15, "Enter your query below.")
        self.stdscr.addstr(11, 15, "Enter 'q' by itself to go back to the previous screen.")
        #self.queryBox.addstr(1, 5, "Enter your query below. Enter 'q' by itself to go back to the previous screen:")
        self.stdscr.refresh()
        inputString = self.queryBox.getstr(3, 25)
        if inputString == 'q':
            curses.curs_set(0)
            curses.noecho()
            self.print_main_menu()
            return
        status = self.db.run_query(inputString)
        if status:
            current_results = self.db.get_next_results()
            self.print_sql_results(current_results, 1)
        else:
            errors = True
            error_list = []
            error_list.append("          There was a problem with your query: " + self.db.get_error())
            self.print_error(error_list)
        # Wait for user input and then quit
        continue_loop = True
        while continue_loop:
            b = self.stdscr.getch()
            if b == curses.KEY_RIGHT:
                if not errors:
                    current_results = self.db.get_next_results()
                    self.print_sql_results(current_results, 1)
            elif b == curses.KEY_LEFT:
                if not errors:
                    current_results = self.db.get_prev_results()
                    self.print_sql_results(current_results, 1)
            elif b == curses.KEY_UP:
                if not errors:
                    if current_results:
                        selection_index -= 1
                        if selection_index < 0:
                            selection_index = len(current_results)
                        self.print_sql_results(current_results, selection_index)
            elif b == curses.KEY_DOWN:
                if not errors:
                    if current_results:
                        selection_index += 1
                        if selection_index > len(current_results):
                            selection_index = 1
                        self.print_sql_results(current_results, selection_index)
            elif b == 10:
                if not errors:
                    if current_results:
                        self.print_row_details(current_results[selection_index-1])
            elif b == 27:
                self.get_user_query()
                continue_loop = False

    def query_db(self):
        pass

    def print_error(self, errors):
        self.clear_screen()
        curses.curs_set(0)

        resultsBox = curses.newwin(self.win_height-2, self.win_width-2, 1, 1)
        if errors:
            col_width = 10  # padding
            x = 1
            for row in errors:
                if type(row) is tuple:
                    temp_string = "".join(str(word).ljust(col_width) for word in row)
                    resultsBox.addstr(x, 10, "".join(str(word).ljust(col_width) for word in row))
                else:
                    col_width = 10 +2
                    temp_string = "".join(str(word).ljust(col_width) for word in errors)
                    resultsBox.addstr(x, 10, "".join(str(word).ljust(col_width) for word in errors))
                x += 1
                resultsBox.refresh()
                self.stdscr.refresh()

    def print_sql_results(self, returned_results, selection_index):
        self.clear_screen()
        curses.curs_set(0)
        results = returned_results[:]
        resultsBox = curses.newwin(self.win_height-2, self.win_width-2, 1, 1)
        resultsBox.border(0)
        column_names = self.db.get_returned_columns()
        if column_names:
            results.insert(0, column_names)
        #based solutions from link, http://stackoverflow.com/questions/9989334/create-nice-column-output-in-python
        if results:
            col_width = 11  # padding
            x = 1
            for index, row in enumerate(results):
                if type(row) is tuple:
                    temp_string = "".join(str(word).ljust(col_width) for word in row)
                    if index == selection_index:
                        resultsBox.addstr(x, 2, "".join(str(word)[0:9].ljust(col_width) for word in row[0:6]), curses.A_STANDOUT)
                    else:
                        resultsBox.addstr(x, 2, "".join(str(word)[0:9].ljust(col_width) for word in row[0:6]))
                else:
                    col_width = 11
                    temp_string = "".join(str(word).ljust(col_width) for word in results)
                    if index == selection_index:
                        resultsBox.addstr(x, 2, "".join(str(word)[0:9].ljust(col_width) for word in results[0:6]), curses.A_STANDOUT)
                    else:
                        resultsBox.addstr(x, 2, "".join(str(word)[0:9].ljust(col_width) for word in results[0:6]))
                x += 1
                resultsBox.addstr(15, 8, "Press enter to select in-depth details on row.")
                resultsBox.addstr(16, 8, "Use up and down arrow to navigate between rows in table.")
                resultsBox.addstr(17, 8, "Use left and right arrow to navigate between pages in table.")
                resultsBox.addstr(18, 8, "Press escape to go back to table selection.")
                resultsBox.refresh()
                self.stdscr.refresh()
        else:
            resultsBox.addstr(1, 10, "This query contains no results")
            resultsBox.addstr(10, 25, "Press escape to go back")
            resultsBox.refresh()
            self.stdscr.refresh()

    def end_win(self):
        curses.endwin()
if __name__ == '__main__':
    cur = NCurses()
