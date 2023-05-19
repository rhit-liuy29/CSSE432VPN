# CSSE432VPN

Network VPN Project

IMPORTANT: our scripts were written completely under Windows 10 OS, using any other OS would potentially cause unexpected results. So Windows 10 OS is REQUIRED for this to work. 

A complete guide to use our code to configure OpenVPN on your own:

1. Create a Server IP address <br />
We used Linode as our cloud server hosting service, that's why we would also recommend using Linode to do this. This step is essentially creating a cloud server that act as the destination IP when running the VPN
Link to Linode: https://www.linode.com/lp/free-credit-100/?promo=sitelin100-02162023&promo_value=100&promo_length=60&utm_source=google&utm_medium=cpc&utm_campaign=11178784975_109179237043&utm_term=g_kwd-2629795801_e_linode&utm_content=466889956453&locationid=1017332&device=c_c&gclid=Cj0KCQjwmZejBhC_ARIsAGhCqnc4Q_5nuQPPVmH4cYGPt52DKIZo0YzBMU7XanelmhImg-ddZiz19boaAlSaEALw_wcB
Make sure the server is using some versions of Ubuntu, we used Ubuntu 22.04 LTS. In the region, select the desination that you wish to change your IP into. 

2. Run server setup script on the cloud server <br />
Under VPN_Server folder, you will find a bash script called: server_setup.sh. Import this script into the server hosted from the previous step. Run the script on server, it will initialize PKI and generate all the essential components for you. 
Also, for future uses, also import server.py under the same folder into your hosted server.

3. Create a CA Server <br />
We also used Linode for this step and we are recommending Linode here as well. Create another cloud hosted server using the Link from step 1. This step is essentially creating a CA Server that can review and sign requests generated from both clients and server. 

4. Run CA server components on the server <br />
Under CA_Server folder, you will find FIVE required bash scripts and ONE python file. Import ALL of them into your newly generated CA Server, put them all under the same directory and then run the python file you just imported. This will act as the CA server that reviews and signs all the incoming requests. 
KEEP THIS SERVER OPEN UNTIL YOU ARE DONE WITH ALL REQUESTS

5. Sign server request <br />
Go back to the destination server created in step 1, run server.py that was imported in step 2. server.py requires both IP and port number to run, make sure you put your CA Server IP as IP and the same port number of the running CA Server in step 4. Then the python script should take care of the rest. You will receive a signed crt file under /easyrsa/pki/issued/ directory if all goes well. Also, logs will also be generated to help you identify what is wrong. 

6. Run client setup script locally <br />
Under VPN_Client folder, you will find a bash script setup.bat alongside a client.py python script. Download both of them into your local directory and place them under the same directory. Open CMD or Powershell, navigate to that directory and run the bash script setup.bat. This will download and unpack EasyRsa for you locally and generate a client requests that will be used for CA Server to sign. Again, logs will be generated to help you identify what went wrong.

7. Run the client python script <br />
Run client.py that was downloaded in the previous step with the same IP and port you entered in step 5. If your CA Server is still up and running, everything should be taken care of for you. When this step is done, you will receive client configuration file in the same directory as the python script you just ran. It will be called client.ovpn most likely. 

8. Download OpenVPN Connect UI <br />
Now all the components are ready to go, download and install OpenVPN from the link below first.
Link: https://openvpn.net/client/client-connect-vpn-for-windows/
After installing OpenVPN Connect into your machine, you will see a running application among your hidden icons in your taskbar. Click that icon to open the UI. Click on the drawer icon at the top-left corner of the UI, go to "Import File" and select "File". Import the local ovpn file that you just created in step 7. When this is done, you are ready to go, simply switch on the profile and you are connected!

A quick way to test whether your VPN was correctly configured is to go to https://whoer.net/. This will display your current IP. If the website displays your IP as the same one that you've chosen and created in step 1, you are good to go!
