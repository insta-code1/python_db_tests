from database.mysql import MySQLDatabase

my_db_connection = MySQLDatabase('employees_db',
                                 'root',
                                 'root')


my_tables = my_db_connection.get_available_tables()

my_col = my_db_connection.get_columns_for_table('dept_emp')

kwrgs = {'where': "emp_no-2"}

results = my_db_connection.select('dept_manager', columns=['em', 'first_name'], named_tuples=True, **kwrgs)



print results
print my_tables
print my_col