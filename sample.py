import jaydebeapi
import jpype
import traceback

conn = None
cursor = None

try:
    if jpype.isJVMStarted():
        print("already started!")
    jar = '/Users/xyz/Downloads/ojdbc8.jar'
    trustStore = "/Users/xyz/PycharmProjects/pkcs/store.jks" #Path of the trust store created using the keytool command
    trustStorePassword = "lab123" #Password that you set for the local client trust store
    ip_ise = "1.1.1.1"
    port_ise = "2484"
    dataconnect_user = "dataconnect" #The username is always dataconnect
    dataconnect_password = "C1sc01234#C$$" #The password is the same one that is set in the Data Connect window in the Cisco ISE GUI
    url = "jdbc:oracle:thin:@(DESCRIPTION=(ADDRESS=(PROTOCOL=tcps)(HOST="+ip_ise+")(PORT="+port_ise+"))(CONNECT_DATA=(SID=cpm10)))" #ODBC connection details that are available in the Cisco ISE GUI
    jvm_path = jpype.getDefaultJVMPath()
    jpype.startJVM(jvm_path,    "-Djava.class.path=%s" % jar,
                                "-Djavax.net.ssl.trustStore=%s" % trustStore,
                                "-Djavax.net.ssl.trustStorePassword=%s" % trustStorePassword)

    conn = jaydebeapi.connect('oracle.jdbc.driver.OracleDriver',
                                   url,
                                   {'user': dataconnect_user,
                                    'password': dataconnect_password,
                                    'secure': 'true'},
                                   jar)

    cursor = conn.cursor()

    #Sample Query 1: Listing all the Network Device Groups

    cursor.execute('SELECT * from NETWORK_DEVICE_GROUPS')
    output = cursor.fetchall()
    print("\nList of Network Device Groups:")
    print("\nCreated By\t\t\t Status\t\t Name\n")
    for row in output:
        print(row[3],"\t", row[6],"\t",row[2])

    #Sample Query 2: Information of all the nodes in deployment

    cursor.execute('SELECT * from NODE_LIST')
    output = cursor.fetchall()
    print("\n\nList of Nodes:")
    print("\nHOSTNAME\t\t NODE_TYPE\t\t NODE_ROLE\n")
    for row in output:
        print(row[0],"\t", row[1],"\t",row[3])

    #Sample Query 3: Details of all the administrators of ISE

    cursor.execute('SELECT * from ADMIN_USERS')
    output = cursor.fetchall()
    print("\n\nList of Admin Users:")
    print("\nSTATUS\t\t ADMIN_GROUP\t NAME\n")
    for row in output:
        print(row[1],"\t", row[7],"\t",row[2])


except Exception as e:
    print('An exception occurred: {}'.format(e))
    print(traceback.format_exc())

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    if jpype.isJVMStarted():
        jpype.shutdownJVM()