import jaydebeapi
import jpype
import traceback
import pandas as pd
import sys
import os
import warnings
from urllib3.exceptions import InsecureRequestWarning
from tqdm import tqdm

conn = None
cursor = None

def get_data2csv(ise_url,auth_ise,ise_index,file_path,Verify_SSL):
    getMethod_url ='/api/v1/certs/trusted-certificate' #method URL path
    ise_cert_url = f'{ise_url}{getMethod_url}'
    getMethod_header = {
                        'Content-Type' : 'application/json', 
                        'Accept' : 'application/json'
                    }
    
    response = requests.get(url = ise_cert_url, headers = getMethod_header, auth = auth_ise, verify = Verify_SSL)
    if response.status_code == 200: #Code of successful process according to documentation
        file_name = f'TrustedCertificates_ISE_{ise_index}' #Name of the obtained file
        file_path = os.path.join(file_path,file_name)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        print(f'code #{response.status_code}: Getting ISE Trusted Certificates in {fqdn}')
        certificates = response.json()['response']
        certificates_table = pd.DataFrame.from_dict(pd.json_normalize(certificates),orient='columns')
        certificates_table.to_csv(os.path.join(file_path,f'{file_name}.csv'))
        print(f'-> Creating the file:{file_name}.csv in {file_path}')
        certificates_id = certificates_table['id'].tolist() #Getting the IDs
        with tqdm(total=len(certificates_id),desc=f'-> Downloading Trusted Certificates in the folder', unit="cert") as pbar:
            for certificate_id in certificates_id:
                certificate_url = f'{ise_cert_url}/export/{certificate_id}'
                export_cert(certificate_url, certificate_id, auth_ise, ise_index, file_path, Verify_SSL)
                pbar.update(1)
    else:
        print(f'On ISE node {ise_index}: {fqdn}')
        print(f'code #{response.status_code}: {eval(response.text)["message"]}')


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

    #Sample Query 1: Listing all the Network Device Groups

    cursor.execute('SELECT * from NETWORK_DEVICE_GROUPS')
    output = cursor.fetchall()
    print("\nList of Network Device Groups:")
    print("\nCreated By\t\t\t Status\t\t Name\n")
    for row in output:
        print(row[3],"\t", row[6],"\t",row[2])




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