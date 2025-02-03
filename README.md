# ISE_DataConnect

Testing Data Connect feature available on ISE 3.2 and above.

## Requirements
1. Enable Data Connect on ISE
   - In the Cisco ISE GUI, click the Hamburger menu and choose **Administration > System > Settings > Data Connect**.
2. After the Data Connect feature is enabled.
   - In ISE 3.2, an existing self-signed certificate, called Data Connect Certificate, is imported and placed in the Trusted Certificates store of Cisco ISE. You must export this certificate from Cisco ISE and import it into the trusted certificate store of your SQL client before you try to establish a connection to the Cisco ISE database from that client.
      - In the Cisco ISE admin portal, click the Hamburger menu and choose **Administration > System > Certificates > Certificate Management > Trusted Certificates.**
      - Check the check box next to the certificate with the name Data Connect Certificate in the list of certificates.
      - Click Export.
   - In ISE 3.3 and above, based on whether the admin certifiate is issued by a CA or is a selfsigned certificate, the certificates that must be imported for connecting to Data Connect are different.
      - **When the admin certificate is issued by a CA:** When the admin certificate is issued by a CA, the client must obtain all the certificates that are a part of the certificate chain that was used to sign the admin certificate. This certificate chain must be imported to the client's trusted wallet. However, you don't have to import the admin certificate.
      - **When the admin certificate is a self-signed certificate:** When the admin certificate is a self-signed certificate, you must import the admin certificate to the client's trust store. Import the admin certificate by using the following procedure:
         - In the Cisco ISE admin portal, click the hamburger Menu and choose **Administration > System > Certificates > Certificate Management > System Certificates.**
         - Check the check box next to the certificate with the name Admin Certificate.
         - Click Export. 
3. To establish a database connection with the Python code, you must have ojdbcX.jar (X is the version) downloaded in your local client. (Select the correct version based on your client JDK eg: ojdbc11.jar). Therefore JDK is needed as well.
   - [JDK download](https://www.oracle.com/java/technologies/downloads/) 
      > i.e. for windows 10/11: Install on  the machine [JDK 21 - x64 MSI Installer](https://download.oracle.com/java/21/latest/jdk-21_windows-x64_bin.msi), then change path and add variable under **Edit the system enviroment variables > Advance > Environment Variables**. path: 'C:\Program Files\Java\jdk-21\bin' variable name: JAVA_HOME in 'C:\Program Files\Java\jdk-21'
   - [Oracle JDBC drivers guide](https://www.oracle.com/database/technologies/maven-central-guide.html) and [Oracle JDBC drivers download](https://www.oracle.com/database/technologies/appdev/jdbc-downloads.html)
      > Download [ojdbc11.jar](https://download.oracle.com/otn-pub/otn_software/jdbc/236/ojdbc11.jar) in a folder such as 'C:\Users\administrator\Documents\Database_Resources'
4. Install the following in your python enviroment.
```console
pip install JayDeBeApi
```
5. Use the below command under admin priviledge to add all the downloaded certificates to the trust store.
   - Enter a new trust store password when prompted for the same.
   - Enter **Y** when prompted whether to trust this certificate or not.
```JDK
keytool -import -alias <Name> -file <Data Connect certificate file path and name> -storetype JKS -keystore <trust store name>
```
   >Note: To use PKCS12 as the storetype, replace JKs with PKCS12 in the code. Ensure that the alias name is unique.

```JDK
keytool -import -alias "ISE_DataConnect" -file "C:\Users\administrator\Documents\Database_Resources" -storetype PKCS12 -keystore "ISE_DataLink"
```
6. The "sample.py" is a sample script to establish ODBC connection to the Cisco ISE monitoring data base and fetch the required details.