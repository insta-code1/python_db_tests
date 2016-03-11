import MySQLdb as _mysql
import collections


class MySQLDatabase:
    def __init__(self, database_name, username, password, host='localhost'):
        try:
            self.db = _mysql.connect(db=database_name,
                                     host=host,
                                     user=username,
                                     passwd=password)

            self.database_name = database_name

            print " Connected to MySQL!"
        except _mysql.Error, e:
            print e

    def __del__(self):
        if hasattr(self, 'db'):  # close our connect to free it up in the pool
            self.db.close()
            print "MySQL Connect closed"

    def get_available_tables(self):
        cursor = self.db.cursor()
        cursor.execute("SHOW TABLES;")

        self.tables = cursor.fetchall()

        cursor.close()

        return self.tables

    def get_columns_for_table(self, table_name):
        try:
            cursor = self.db.cursor()
            cursor.execute("SHOW COLUMNS FROM %s " % table_name)

            columns = cursor.fetchall()

            cursor.close()

            return columns
        except _mysql.Error, e:
            print e

    def convert_to_named_tuples(self, cursor):
        results = None

        names = " ".join(d[0]for d in cursor.description)
        klass = collections.namedtuple('Result', names)

        try:
            results = map(klass._make, cursor.fetchall())
        except _mysql.ProgrammingError:
            pass

        return results

    def select(self, table, columns=None, named_tuples=False, **kwargs):
        """
        select(table_name, [list of column name])
        """
        sql_str = "SELECT "

        # add columns or just the wildcard
        if not columns:
            sql_str += "* "
        else:
            for column in columns:
                sql_str += "%s, " % column

            sql_str = sql_str[:-2] # remove the last comma!

        # add the table to select from
        sql_str += " FROM `%s`.`%s`" % (self.database_name, table)

        # there a JOIN clause attached

        if kwargs.has_key('join'):
            sql_str+= " JOIN %s" % kwargs.get('join')

        # there a WHERE clause attached
        if kwargs.has_key('where'):
            sql_str += " WHERE %s" % kwargs.get('where')

        sql_str += ";" #finalis our sql string

        cursor = self.db.cursor()

        cursor.execute(sql_str)

        if named_tuples:
            result = self.convert_to_named_tuples(cursor)
        else:
            result = cursor.fetchall()

        cursor.close()

        return result

    def delete(self, table, **wheres):
            sql_str = "DELETE FROM `%s`.`%s`" % (self.database_name, table)

            if wheres is not None:
                first_where_clause = True
                for wheres, term in wheres.iteritems():
                    if first_where_clause:
                        # this is first WHERE clause
                        sql_str += " WHERE `%s`.`%s`%s" % (table, wheres, term)
                        first_where_clause = False
                    else:
                        # this and additional clause so use AND
                        sql_str += " AND `%s`.`%s`%s" % (table, wheres, term)

            sql_str += ";"

            cursor = self.db.cursor(
            cursor.execute(sql_str)

            cursor.close()
