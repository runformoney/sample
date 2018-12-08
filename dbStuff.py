import sqlite3
import MySQLdb

def db_connect():
    global conn
    conn = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="admin",  # your password
                     db="axis_bank",        # name of the data base
                    port = 3306)
    return(conn)

class DBHelper:

    def __init__(self, dbname="axis_bank"):
        self.dbname = dbname
        # self.conn = sqlite3.connect(dbname)
        # print("Connection Successful with DB")
        # self.conn.close()

    def setup(self):
        conn = db_connect()
        # tblstmt = "CREATE TABLE IF NOT EXISTS account_details (cust_fname varchar(50), cust_lname varchar(50)," \
        #           "cust_email varchar(50), cust_mobilenumber varchar(50), cust_accnum varchar(50), cust_atmnumber varchar(50)," \
        #           "cust_atmpin varchar(50), cust_acccif varchar(50), cust_accifsc varchar(50), cust_accactivationcode varchar(50))"

        tblstmt4 = "INSERT INTO account_details  (cust_fname,cust_lname,cust_email, cust_mobilenumber,cust_accnum," \
                   "cust_atm_number,cust_atm_pin,cust_acccif,cust_acc_ifsc,cust_acc_activationcode) " \
                   "VALUES ('Rukhshan','Rahman','rukshanurrahman@gmail.com','8884300686','12345678','12345678'," \
                   "'12345678','12345678','1234','12345678')"
        # conn.execute(tblstmt)
        #conn.execute(tblstmt4)
        conn.commit()

    def check_details(self, dataToQuery):
        print(dataToQuery)
        conn = db_connect()
        cur = conn.cursor()
        stmt = "select * from account_details where cust_fname=%s and cust_atm_number=%s and cust_atm_pin=%s and cust_acc_activationcode=%s"
        args = (dataToQuery[0],dataToQuery[5],dataToQuery[6],dataToQuery[9])
        # args = ("Rukhshan",'12345678','1234','12345678')
        cur.execute(stmt,args)
        result = cur.fetchone()
        if result == None:
            return 0
        elif len(result) > 1:
        #print(result)
            return 1
        else:
            return 0
        #conn.commit()
        #conn.close()

# dbhelper = DBHelper()
# dbhelper.check_details(1234)