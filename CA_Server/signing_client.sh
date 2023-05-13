#!/bin/bash

cd easy-rsa/
./easyrsa import-req /home/rose/easy-rsa/pki/client_req.req clientreq
printf 'yes\n' | ./easyrsa sign-req client clientreq
cd
