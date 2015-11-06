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

        self.latest_query = None
        self.latest_results = None
        self.latest_error = None
        self.results_per_page = 5
        self.start_index = -1
        self.end_index = -1
        self.current_index = self.results_per_page * -1
        self.skip = False
        self.test = [0,1,2,3,4,5,6,7,8,9]
        self.cursor = self.conn.cursor()

    def drop_table(self):
        sql_str = "DROP TABLE names"

    def run_query(self,query):
        self.latest_query = query
        try:
            self.cursor.execute(self.latest_query)
        except Exception as e:
            self.latest_error =  e
            return False
        self.current_index = 0
        self.latest_results = self.cursor.fetchall()
        return True


    def set_results_per_page(self,results_per_page):
        pass

    def get_error(self):
        return self.latest_error

    def get_recent_query(self):
        return self.latest_query

    def get_all_results(self):
        return self.latest_results

    def get_next_results(self):
        if self.latest_results:
            self.current_index += self.results_per_page
            if self.current_index >= len(self.test):
                self.current_index -= self.results_per_page
            return self.latest_results[self.current_index:self.current_index+self.results_per_page]
        else:
            return []

    def get_prev_results(self):
        if self.latest_results:
            self.current_index -= self.results_per_page
            if self.current_index <0:
                self.current_index = 0
            return self.latest_results[self.current_index:self.current_index+self.results_per_page]
        else:
            return []

    def list_tables(self):
        sql_str = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' \
        AND table_type='BASE TABLE';"
        self.cursor.execute(sql_str)
        results = self.cursor.fetchall()
        return results

    def create_table(self, table_name):
        sql_str = "CREATE TABLE %s (id SERIAL PRIMARY KEY, first TEXT, last TEXT)" %(table_name)
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
    import sys
    db = PgHandler()
