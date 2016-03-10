import MySQLdb as _mysql

db = _mysql.connect(db='employees_db',
                    host='localhost',
                    user='root',
                    passwd='root')

my_cursor = db.cursor()

my_cursor.execute("UPDATE employees SET first_name = 'Eoin' WHERE emp_no=10001")
my_cursor.execute("SELECT * FROM employees")
results = my_cursor.fetchone()

print results