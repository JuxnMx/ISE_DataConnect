import jaydebeapi
import jpype
import traceback
import pandas as pd
import os

conn = None
cursor = None

def get_data2csv(output_SQL,table_name,file_path,headers):
    file_name = f'{table_name}' #Name of the obtained file
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    output_table = pd.DataFrame(output_SQL,columns=headers)
    output_table.to_csv(os.path.join(file_path,f'{file_name}.csv'))


try:
    if jpype.isJVMStarted():
        print("already started!")
    jar = '/Users/administrator/Documents/Database_Resources/ojdbc11.jar'
    trustStore = "/Users/administrator/Documents/Database_Resources/ISE_DataLink" #Path of the trust store created using the keytool command
    trustStorePassword = "Cisco123" #Password that you set for the local client trust store
    ip_ise = "198.18.133.16"
    port_ise = "2484"
    dataconnect_user = "dataconnect" #The username is always dataconnect
    dataconnect_password = "Cisco123456#" #The password is the same one that is set in the Data Connect window in the Cisco ISE GUI
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

    #Sample Query 1: Getting all details of all the TACACS authorization records into a CSV

    cursor.execute('SELECT * from TACACS_AUTHORIZATION')
    output = cursor.fetchall()
    # print(type(output))
    file_name = 'TACACS_AUTH'
    file_path = 'C:/Users/administrator/Documents/Database_Resources/testing_tables' #Path and name of the folder 
    # for row in output:
    #     print(row[30],"\t", row[1],"\t",row[2])
    headers =['ID','GENERATED_TIME','LOGGED_TIME','ISE_NODE',
              'ATTRIBUTES','EXECUTION_STEPS','STATUS','EVENT',
              'MESSAGE_TEXT','DEVICE_IPV6','DEVICE_NAME','DEVICE_IP',
              'DEVICE_GROUP','DEVICE_PORT','EPOCH_TIME','FAILURE_REASON',
              'USERNAME','AUTHORIZATION_POLICY','AUTHECNTICATION_PRIVILEGE_LEVEL',
              'AUTHORIZATION_REQUEST_ATTR','AUTHORIZATION_RESPONSE_ATTR','SESSION_KEY',
              'REMOTE_ADDRESS','SHELL_PROFILE','AUTHENTICATION_METHOD','AUTHENTICATION_TYPE',
              'AUTHENTICATION_SERVICE','DEVICE_TYPE','LOCATION',
              'MATCHED_COMMAND_SET','COMMAND_FROM_DEVICE']
    get_data2csv(output,file_name,file_path,headers)



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