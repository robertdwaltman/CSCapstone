from ui.ncurses import NCurses
from pgdb.pgdb import PgHandler


if __name__ == '__main__':

    # Create UI
    obj = NCurses()

    # Create DB interface
    db = PgHandler()

    db.create_table("places")
    db.create_table("things")
    #db.insert()
    #db.select()