import pymysql
import pymysql.cursors

def connect():
    conn = pymysql.connect(host='47.100.217.10', user='root', passwd='baidu2019', db='mysql')
    cur = conn.cursor()
    cur.execute("SELECT Host,User FROM user")
    for r in cur:
        print(r)
    cur.close()
    conn.close()

# Function return a connection.
def getConnection():
     
    # You can change the connection arguments.
    connection = pymysql.connect(host='47.100.217.10',
                                 user='root',
                                 password='baidu2019',                             
                                 db='test',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

def connect_cur():
    # Connect to the database.
    connection = pymysql.connect(host='47.100.217.10',
                        user='root',
                        password='baidu2019',                             
                        db='test',
                        charset='utf8mb4',
                        cursorclass=pymysql.cursors.DictCursor)
    print ("connect successful!!")

    try:
        with connection.cursor() as cursor:
        
            # SQL 
            sql = "SELECT Dept_No, Dept_Name FROM Department "
            
            # Execute query.
            cursor.execute(sql)
            
            print ("cursor.description: ", cursor.description)
    
            print()
    
            for row in cursor:
                print(row)
                
    finally:
        # Close connection.
        connection.close()

def query():
    #connection = myconnutils.getConnection()
    connection = getConnection()
 
    print ("Connect successful!")
    
    sql = "Select Emp_No, Emp_Name, Hire_Date from Employee Where Dept_Id = %s "
    
    try :
        cursor = connection.cursor()
    
        # Execute sql, and pass 1 parameter.
        cursor.execute(sql, ( 10 ) )
        
        print ("cursor.description: ", cursor.description)
        
        print()
        
        for row in cursor:
            print (" ----------- ")
            print("Row: ", row)
            print ("Emp_No: ", row["Emp_No"])
            print ("Emp_Name: ", row["Emp_Name"])
            print ("Hire_Date: ", row["Hire_Date"] , type(row["Hire_Date"]) )
    
    finally:
        # Close connection.
        connection.close()
if __name__ == "__main__":
    query()