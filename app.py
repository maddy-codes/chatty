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


@app.route("/")
def hello_world():
    return render_template('test.html')
