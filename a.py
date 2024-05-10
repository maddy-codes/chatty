import pyodbc
server = '34.105.250.198'
database = 'logging_database'
username = 'sqlserver'


password = 'csy2088'
driver =   'SQL Server'
# INITIALISING THE CONNECTION
cnxn = pyodbc.connect('DRIVER=' + driver +
                      ';SERVER=' + server +
                      ';DATABASE=' + database +
                      ';UID=' + username +
                      ';PWD=' + password +
                      ';Encrypt=mandatory;' +  # Enable encryption
                      ';TrustServerCertificate=yes;'  # Disable implicit trust of server certificate
)