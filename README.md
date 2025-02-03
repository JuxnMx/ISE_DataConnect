# ISE_DataConnect

Testing Data Connect feature available on ISE 3.2 and above.

## Requirements
1. Enable Data Connect on ISE
   - In the Cisco ISE GUI, click the Hamburger menu and choose **Administration > System > Settings > Data Connect**.
2. After the Data Connect feature is enabled, an existing, self-signed certificate, called Data Connect Certificate, is imported and placed in the Trusted Certificates store of Cisco ISE. You must export this certificate from Cisco ISE and import it into the trusted certificate store of your SQL client before you try to establish a connection to the Cisco ISE database from that client.
   - In the Cisco ISE admin portal, click the Hamburger menu and choose **Administration > System > Certificates > Certificate Management > Trusted Certificates.**
   - Check the check box next to the certificate with the name Data Connect Certificate in the list of certificates.
   - Click Export.
3. To establish a database connection with the Python code, you must have ojdbcX.jar (X is the version) downloaded in your local client. (Select the correct version based on your client JDK eg: ojdbc11.jar). Therefore JDK is needed as well.
   - [JDK download](https://www.oracle.com/java/technologies/downloads/) 
   - [Oracle JDBC drivers download](https://www.oracle.com/database/technologies/maven-central-guide.html)
4. Install the following in your python enviroment.
```console
pip install JayDeBeApi
```
5. Use the below command to add all the downloaded certificates to the trust store.
   - Enter a new trust store password when prompted for the same.
   - Enter **Y** when prompted whether to trust this certificate or not.
```JDK
keytool -import -alias <Name> -file <Data Connect certificate file path and name> -storetype JKS -keystore <trust store name>
```
   >Note: To use PKCS12 as the storetype, replace JKs with PKCS12 in the code. Ensure that the alias name is unique.

6. The "sample.py" is a sample script to establish ODBC connection to the Cisco ISE monitoring data base and fetch the required details.