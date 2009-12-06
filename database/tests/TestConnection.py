#!/usr/bin/python
import MySQLdb 
import unittest

con = MySQLdb.connect('pcgerosa', 'donkeystats', 'donkey')
con.select_db('donkeystats')
cursor = con.cursor()
cursor.execute('select * from session')
con.commit()
rs = cursor.fetchall()
