import dbinfo
import psycopg2
import pprint
class PgHandler(object):
    """docstring for NCurses"""
    def __init__(self):
        print "Created database interface"

        conn_string = "host='%s' dbname='%s' user='%s' password='%s'" % (dbinfo.DB_HOST ,dbinfo.DB_NAME, dbinfo.DB_USER, dbinfo.DB_PASSWORD)
        self.conn = psycopg2.connect(
            database=dbinfo.DB_NAME	,
            user=dbinfo.DB_USER,
            password=dbinfo.DB_PASSWORD,
            host=dbinfo.DB_HOST,
            port=dbinfo.DB_PORT
            )

        self.cursor = self.conn.cursor()

    def drop_table(self):
        sql_str = "DROP TABLE names"

    def create_table(self):
        sql_str = "CREATE TABLE names (id SERIAL PRIMARY KEY, first TEXT, last TEXT)"
        self.cursor.execute(sql_str)
        self.conn.commit()

    def insert(self):
        sql_str = "INSERT INTO names (first,last) VALUES('test','name')"
        self.cursor.execute(sql_str)
        self.conn.commit()
        print "Inserted new record"

    def select(self):
        sql_str = "SELECT * FROM  names"
        self.cursor.execute(sql_str)
        results = self.cursor.fetchall()
        print "Records:"
        pprint.pprint(results)

if __name__ == '__main__':
    db = PgHandler()

    # db.dropTable()
    # db.createTable()
    db.insert()
    db.select()