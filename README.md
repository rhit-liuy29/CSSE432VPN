# CSSE432VPN

Network VPN Project

IMPORTANT: our scripts were written completely under Windows 10 OS, using any other OS would potentially cause unexpected results. So Windows 10 OS is REQUIRED for this to work. 

A complete guide to use our code to configure OpenVPN on your own:

1. Create a CA Server <br />
We used Linode for this step and we are recommending Linode here as well. Create a new Linode from there. This step is essentially creating a CA Server that can review and sign requests generated from both clients and server. <br />
Link: https://www.linode.com/lp/free-credit-100/?promo=sitelin100-02162023&promo_value=100&promo_length=60&utm_source=google&utm_medium=cpc&utm_campaign=11178784975_109179237043&utm_term=g_kwd-2629795801_e_linode&utm_content=466889956453&locationid=1017332&device=c_c&gclid=Cj0KCQjwmZejBhC_ARIsAGhCqnc4Q_5nuQPPVmH4cYGPt52DKIZo0YzBMU7XanelmhImg-ddZiz19boaAlSaEALw_wcB <br />
Make sure the server is using some versions of Ubuntu, we used Ubuntu 22.04 LTS. In the region, select the desination that you wish to change your CA Server to be in.<br />
After creating the CA Server, you'll need a new user other the default root user. <br />
Simply create a new user on the server by typing these commands into your command lines: 
```
useradd -G sudo -m rose -s /bin/bash
```
```
passwd rose
```
Here, enter the password that you want to use for your new non-root user. Make sure to keep track of this password somewhere. <br />
Afterwards, exit from the current server and re-login as the new non-root user: 
```
ssh rose@<YOUR CA SERVER IP>
```
Enter the password you just set and you are ready to proceed.

2. Setup easy-rsa on CA Server <br />
Type these commands into your command line on CA Server:
```
mkdir ~/easy-rsa
```
```
wget -qO- https://github.com/OpenVPN/easy-rsa/releases/download/v3.1.2/EasyRSA-3.1.2.tgz 2>null | tar xz -C ~/easy-rsa/ --strip-components 1
```
```
cd easy-rsa/
```
```
./easyrsa init-pki
```
```
./easyrsa build-ca nopass
```

3. Run CA server components on the server <br />
IMPORTANT: Before doing this step, make sure python3 is installed on your server<br />
Under CA_Server folder, you will find FIVE required bash scripts and ONE python file. Import ALL of them into your newly generated CA Server, put them all under the same directory WITH EASYRSA and then run the python file you just imported. This will act as the CA server that reviews and signs all the incoming requests.
KEEP THIS SERVER OPEN UNTIL YOU ARE DONE WITH ALL REQUESTS

4. Create a Server IP address <br />
We used Linode as our cloud server hosting service, that's why we would also recommend using Linode to do this. This step is essentially creating a cloud server that act as the destination IP when running the VPN. Create a new Linode just like what you did in step 1.
Make sure the server is using some versions of Ubuntu, we used Ubuntu 22.04 LTS. In the region, select the desination that you wish to change your IP address into.

5. Run server setup script on the cloud server <br />
IMPORTANT: Before doing this step, make sure python3 is installed on your server<br />
Under VPN_Server folder, you will find a bash script called: server_setup.sh. Import this script alongside with server.py in the same folder into the server hosted from the previous step. Run the script on server, it will initialize PKI and generate all the essential components for you. When asked about CA Server IP and port, just enter the corresponding ones that you had for your CA Server. 

6. Sign server request <br />
The python script should take care of this step automatically. You will receive a signed crt file under /easyrsa/pki/issued/ directory if all goes well. Also, logs will also be generated to help you identify what is wrong. 

7. Run client setup script locally <br />
Under VPN_Client folder, you will find a bash script setup.bat alongside a client.py python script. Download both of them into your local directory and place them under the same directory. Open CMD or Powershell, navigate to that directory and run the bash script setup.bat. This will download and unpack EasyRsa for you locally and generate a client requests that will be used for CA Server to sign. Again, logs will be generated to help you identify what went wrong. When asked about CA Server IP and port, just enter the corresponding ones that you had for your CA Server. At the end, you will see a client.ovpn file in your current directory. MAKE SURE CLIENT.PY IS UNDER THE SAME DIRECTORY.

8. Download OpenVPN Connect UI <br />
Now all the components are ready to go, download and install OpenVPN from the link below first. <br />
Link: https://openvpn.net/client/client-connect-vpn-for-windows/ <br />
After installing OpenVPN Connect into your machine, you will see a running application among your hidden icons in your taskbar. Click that icon to open the UI. Click on the drawer icon at the top-left corner of the UI, go to "Import File" and select "File". Import the local client.ovpn file that you just created in step 7. When this is done, you are ready to go, simply switch on the profile and you are connected!

A quick way to test whether your VPN was correctly configured is to go to https://whoer.net/. This will display your current IP. If the website displays your IP as the same one that you've chosen and created in step 4, you are good to go!
