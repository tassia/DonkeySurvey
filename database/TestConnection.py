#!/usr/bin/python
import MySQLdb 

con = MySQLdb.connect('localhost', 'vinicius', '123')
con.select_db('donkeystats')
cursor = con.cursor()
s = "test"
cursor.execute("""INSERT INTO filename(name) values(%s)""", (s,))
con.commit()
cursor.execute('select * from filename')
con.commit()
rs = cursor.fetchall()
print(rs[0])

