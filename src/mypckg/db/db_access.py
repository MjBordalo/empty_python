import sys


try:
    import pymysql
    pymysql.install_as_MySQLdb()
    import MySQLdb
except Exception:
    print("You will not be able to SqlActions since you don't have pymysql installed")    
else: 


    class SqlActions:
        def __init__(self, db_host, db_user, db_pass, db_name, db_port=None, cnx_active=False, debug=False):

            self.db_host = db_host
            self.db_user = db_user
            self.db_pass = db_pass
            self.db_name = db_name
            self.db_port = db_port
            self.cnx_active = cnx_active
            self.debug = debug

            if self.cnx_active is True:
                self.connect()
    
            else:
                self.cnx = None    

        @staticmethod
        def debug_select(debug, table_changed, cursor):
            if debug is True and table_changed is not None:
                try:
                    cursor.execute("SELECT * FROM {}".format(table_changed))
                    info = cursor.fetchall()
                    print("Table {}: {}".format(table_changed, info))

                except Exception as e:
                    SqlActions.error_message("Probably {} does not exist:".format(table_changed), e)

        @staticmethod
        def error_message(error_txt, error):
            print("{}: Error on line {} ... type: {} ... arg e: {}".format(error_txt, sys.exc_info()[-1].tb_lineno, type(error).__name__, error))



        def connect(self):

            if self.db_port is None:
                self.cnx = MySQLdb.connect(host=self.db_host,
                            user=self.db_user,
                            passwd=self.db_pass,
                            db=self.db_name)
            else:            
                self.cnx = MySQLdb.connect(host=self.db_host,
                            user=self.db_user,
                            passwd=self.db_pass,
                            port=self.db_port,
                            db=self.db_name)

        def cnx_open(self):
            try:
                if self.cnx is None:
                    self.connect()
                elif self.cnx_active is False:
                    self.connect()
                else:
                    self.cnx.ping(True)
            except:
                self.cnx = None
                return False
            else:
                return True                


        def cnx_close(self, force_closure=False):    
            if self.cnx_active is False or force_closure is True:
                self.cnx.close()

        def select_query(self, query, error_txt="select_error"):
            """
                This function will execute and fetch the cursor.
                So can be used to any select query
            """
            if not self.cnx_open():
                return None
            try:
                self.cnx_open()
                
                cursor = self.cnx.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(query)
                info = cursor.fetchall()

            except Exception as e:
                SqlActions.error_message(error_txt, e)
                return None
            
            else:
                cursor.close()
                self.cnx_close()
                if self.debug is True:
                    print("The query: {} \nThe result: {} \n".format(query, info))
                return info

        def other_simple_query(self, query, error_txt="other_simple", table_changed=None):
            """
                This function will do execute and commit, on error rollback. 
                So you can insert/delete/update
            """
            if not self.cnx_open():
                return None
            try:

                cursor = self.cnx.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute(query)
                self.cnx.commit()

            except Exception as e:
                if self.cnx is not None:
                    self.cnx.rollback()
                SqlActions.error_message(error_txt, e)
                return None

            else:
                SqlActions.debug_select(self.debug, table_changed, cursor)

                cursor.close()
                self.cnx_close()
                return True

        def other_many_query(self, info_format, info_list, error_txt="other_many", table_changed=None):
            """
                This function will do executemany and commit, on error rollback. 
                So you can insert/delete/update
            """
            if not self.cnx_open():
                return None
            try:
                cursor = self.cnx.cursor(MySQLdb.cursors.DictCursor)
                cursor.executemany(info_format, info_list)
                self.cnx.commit()

            except Exception as e:
                if self.cnx is not None:
                    self.cnx.rollback()
                SqlActions.error_message(error_txt, e)
                return None

            else:
                SqlActions.debug_select(self.debug, table_changed, cursor)

                cursor.close()
                self.cnx_close()
                return True

try:
    import sqlite3
except Exception:
    print("You will not be able to db_sqlite3 since you don't have sqlite3 installed")    
else:    

    class db_sqlite3(object):   

        def __init__(self, db_log):
            
            self.db_log = db_log
            self.db_logger = db_log.logger

        def create_connection(self, db_file):
            """ create a database connection to a SQLite database """
            self.conn = None
            try:
                self.conn = sqlite3.connect(db_file)
                self.db_logger.info(sqlite3.version)
            except Exception as e:
                self.db_log.error_message("create_connection", e)

        def other_query(self, query_format, info_format=None, return_mode=False):
            if self.conn is not None:
                try:
                    cur = self.conn.cursor()
                    if info_format is not None:
                        cur.execute(query_format, info_format)
                    else:
                        cur.execute(query_format)

                except Exception as e:
                    self.db_log.error_message("other_query: {}".format(query_format), e)
                else:
                    self.conn.commit()
                    if return_mode is True:     
                        info = cur.lastrowid
                        cur.close()
                        return info
                    cur.close()    

        def select_query(self, query_format, info_format=None):
            if self.conn is not None:
                try:
                    cur = self.conn.cursor()
                    if info_format is not None:
                        cur.execute(query_format, info_format)
                    else:
                        cur.execute(query_format)
                except Exception as e:
                    self.db_log.error_message("select_query: {}".format(query_format), e)
                else:
                    rows = cur.fetchall()
                    cur.close()
                    return rows