import dbinfo
import psycopg2
import pprint
import sys


##################################
# Description: Main db class
# Parameters:  None
# Return values: None
##################################
class PgHandler(object):

    ##################################
    # Description: Initialization function for db
    # Parameters:  None
    # Return values: None
    ##################################
    def __init__(self):

        try:
            print "Connecting to database..."
            self.conn = psycopg2.connect(
                database=dbinfo.DB_NAME	,
                user=dbinfo.DB_USER,
                password=dbinfo.DB_PASSWORD,
                host=dbinfo.DB_HOST,
                port=dbinfo.DB_PORT
                )
        except:
            print "Could not connect to database"
            sys.exit()
        self.latest_query = None
        self.latest_results = None
        self.latest_error = None
        self.table_names = None
        self.results_per_page = 5
        self.start_index = -1
        self.end_index = -1
        self.current_index = self.results_per_page * -1
        self.table_index = self.results_per_page * -1
        self.skip = False
        self.cursor = self.conn.cursor()

    ##################################
    # Description: Runs a given query
    # Parameters:  query string
    # Return values: None
    ##################################
    def run_query(self, query):
        self.current_index = self.results_per_page * -1
        self.latest_query = query
        try:
            self.cursor.execute(self.latest_query)
        except Exception as e:
            self.latest_error = e
            self.conn.rollback()
            return False

        self.conn.commit()
        try:
            rowcount =  self.cursor.rowcount
            self.latest_results = self.cursor.fetchall()
        except Exception as e:
            self.conn.rollback()
            if rowcount > 0:
                self.latest_results = [(str(rowcount)+" rows were affected.")]
        return True

    ##################################
    # Description: Returns the error string
    # Parameters:  None
    # Return values: String of error from query
    ##################################
    def get_error(self):
        return str(self.latest_error).replace('\n','\n     ')

    ##################################
    # Description: Returns last query run
    # Parameters:  None
    # Return values: String of last query run
    ##################################
    def get_recent_query(self):
        return self.latest_query

    ##################################
    # Description: Returns the columns of the last run query
    # Parameters:  None
    # Return values: Tuple of column names.
    #                Returns empty tuple if there are no columns
    ##################################
    def get_returned_columns(self):
        if self.cursor.description:
            colnames = [desc[0] for desc in self.cursor.description]
            return tuple(colnames)
        else:
            return ()

    ##################################
    # Description: Returns a consolidated list of results
    # Parameters:  None
    # Return values: Full list of results
    ##################################
    def get_all_results(self):
        return self.latest_results

    ##################################
    # Description: Gets the next set of results
    # Parameters:  None
    # Return values: Returns a list of the next series of results
    #                Returns empty list if there are no results
    ##################################
    def get_next_results(self):
        if self.latest_results:
            self.current_index += self.results_per_page
            if self.current_index >= len(self.latest_results):
                self.current_index -= self.results_per_page
            return self.latest_results[self.current_index:self.current_index+self.results_per_page]
        else:
            return []

    ##################################
    # Description: Gets the previous set of results
    # Parameters:  None
    # Return values: Returns a list of the previous series of results
    #                Returns empty list if there are no results
    ##################################
    def get_prev_results(self):
        if self.latest_results:
            self.current_index -= self.results_per_page
            if self.current_index < 0:
                self.current_index = 0
            return self.latest_results[self.current_index:self.current_index+self.results_per_page]
        else:
            return []

    ##################################
    # Description: Returns table data
    # Parameters:  None
    # Return values: Returns a list of all table data
    ##################################
    def get_table_results(self, table_name):
        self.current_index = self.results_per_page * -1
        sql_str = "SELECT * FROM %s" %(table_name)
        self.cursor.execute(sql_str)
        self.latest_results = self.cursor.fetchall()

    ##################################
    # Description: Returns next set of table names
    # Parameters:  None
    # Return values: List of next set of table names
    ##################################
    def get_next_table_names(self):
        if self.table_names:
            self.table_index += self.results_per_page
            if self.table_index >= len(self.table_names):
                self.table_index -= self.results_per_page
            return self.table_names[self.table_index:self.table_index+self.results_per_page]
        else:
            return []

    ##################################
    # Description: Returns previous set of table names
    # Parameters:  None
    # Return values: List of previous set of table names
    ##################################
    def get_prev_table_names(self):
        if self.table_names:
            self.table_index -= self.results_per_page
            if self.table_index < 0:
                self.table_index = 0
            return self.table_names[self.table_index:self.table_index+self.results_per_page]
        else:
            return []

    ##################################
    # Description: Returns all table names
    # Parameters:  None
    # Return values: List of all table names
    ##################################
    def get_all_tables(self):
        self.table_index = self.results_per_page * -1
        self.table_names = []
        sql_str = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' \
        AND table_type='BASE TABLE';"
        self.cursor.execute(sql_str)
        results = self.cursor.fetchall()
        for r in results:
            if r:
                self.table_names.append(r[0])
        return self.table_names

    ##################################
    # Description: Creates a test table
    # Parameters:  Table names
    # Return values: None
    ##################################
    def create_table(self, table_name):
        sql_str = "CREATE TABLE %s (id SERIAL PRIMARY KEY, first TEXT, last TEXT)" %(table_name)
        self.cursor.execute(sql_str)
        self.conn.commit()

    # Test insert function
    def insert(self):
        sql_str = "INSERT INTO names (first,last) VALUES('test','name')"
        print  self.cursor.execute(sql_str)
        print self.conn.commit()
        print self.cursor.rowcount
        print "Inserted new record"

    # Test select function
    def select(self):
        sql_str = "SELECT * FROM  names"
        self.cursor.execute(sql_str)
        results = self.cursor.fetchall()
        print "Records:"
        pprint.pprint(results)


if __name__ == '__main__':
    # Testing
    import sys
    db = PgHandler()
    db.create_table("more_stuff")
    db.create_table("other_things")
    print db.get_all_tables()