from flask import Flask, render_template
import pyodbc


app = Flask(__name__)


#server = '34.105.250.198'
#database = 'logging_database'
#username = 'sqlserver'
#password = 'csy2088'
#driver =   'SQL Server'
## INITIALISING THE CONNECTION
#cnxn = pyodbc.connect('DRIVER=' + driver +
#                      ';SERVER=' + server +
#                      ';DATABASE=' + database +
#                      ';UID=' + username +
#                      ';PWD=' + password +
#                      ';Encrypt=yes;' +  # Enable encryption
#                      ';TrustServerCertificate=yes;'  # Disable implicit trust of server certificate
#)
## making the database cursor
#cursor  = cnxn.cursor()
#


@app.route("/data/insert", methods=['POST'])
def hello_world():
    try:
        #cursor.execute("INSERT INTO logging_table (log_message) VALUES ('Hello World')")
        #cnxn.commit()
        pyodbc.connect('DRIVER=SQL SERVER;SERVER=34.105.250.198;DATABASE=logging_database;UID=sqlserver;PWD=csy2088;Encrypt=yes;TrustServerCertificate=yes;')
        print("jajajajajajaja")
        return "Data Inserted"
    except Exception as e:
        return f'NOOOOOOOOOOOOOOO\n{e}'
