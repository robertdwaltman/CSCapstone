from ui.ncurses import NCurses
from pgdb.pgdb import PgHandler


if __name__ == '__main__':

    # Create UI
    obj = NCurses()

    # Create DB interface
    db = PgHandler()

    #db.create_table()
    db.insert()
    db.select()