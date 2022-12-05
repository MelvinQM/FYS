import mysql.connector

cnx = mysql.connector.connect(user='admini', password='odroid123',
                              host='192.168.137.2',
                              database='sensoren')
print(cnx.is_connected())
