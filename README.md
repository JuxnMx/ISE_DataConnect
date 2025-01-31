# ISE_DataConnect

Testing Data Connect feature ISE 3.2

## Requirements

1. Enable Data Connect on ISE
   - In the Cisco ISE GUI, click the Hamburger menu and choose **Administration > System > Settings > Data Connect**.
2. After the Data Connect feature is enabled, an existing, self-signed certificate, called Data Connect Certificate, is imported and placed in the Trusted Certificates store of Cisco ISE. You must export this certificate from Cisco ISE and import it into the trusted certificate store of your SQL client before you try to establish a connection to the Cisco ISE database from that client.
   - In the Cisco ISE admin portal, click the Hamburger menu and choose **Administration > System > Certificates > Certificate Management > Trusted Certificates.**
   - Check the check box next to the certificate with the name Data Connect Certificate in the list of certificates.
   - Click Export.
3. Install the following in your python enviroment

```console
pip install JayDeBeApi
```

Installing DB in windows
https://docs.oracle.com/en/cloud/paas/autonomous-database/dedicated/adbbz/
