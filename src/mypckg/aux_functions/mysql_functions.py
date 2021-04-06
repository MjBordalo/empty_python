
import MySQLdb
import versatile.params as params
import json

def mysql_connector():
    return MySQLdb.connect(host=params.R_DBHOST,
                           user=params.R_DBUSER,
                           passwd=params.R_DBPASS,
                           port=params.R_DBPORT,
                           db=params.R_DBNAME)



def get_example():
    '''
    Example of a search querier request to the Db
    :return: dictionary of programs
    '''
    try:
        cnx = mysql_connector()

        #Example of a search get
        cursor = cnx.cursor()
        query = example_querie(serial)
        cursor.execute(query)

        # example on fetching only one result
        cursor2 = cnx.cursor()
        cursor2.execute(example_querie())
        result = cursor2.fetchone()[0]


    except MySQLdb.Error as e:
        print(e)
        return e

    '''Program is a list defining the irrigation zones'''
    programs = {}
    for (column1_name,column2_name) in cursor:

        '''You probably want to json load'''
        stuff = json.loads(column1_name)



#Querie search example. You might want to save all queries in a separate document
def example_querie(a,b,c):
    """
    docstring here
        :param pivot_id:
        :param log:
        :param date:
    """
    return '''
    INSERT INTO pivot_log
    (pivot_id, operation, date_time)
    VALUES({}, "{}", "{}")
    '''.format(a, b, c)
