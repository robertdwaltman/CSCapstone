from ui.ncurses import NCurses
from pgdb.pgdb import PgHandler


if __name__ == '__main__':

    # Create UI
    import argparse
    parser = argparse.ArgumentParser(description='Run as development or production.')
    parser.add_argument('-d', '--dev',action='store_true', help='run using development DB')
    args = parser.parse_args()
    cur = NCurses(dev=args.dev)


    # Create DB interface
    #db = PgHandler()

    #db.create_table("places")
    #db.create_table("things")
    #db.insert()
    #db.select()