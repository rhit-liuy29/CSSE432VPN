#!/bin/bash

cd easy-rsa/
./easyrsa import-req /home/rose/easy-rsa/pki/server_req.req serverreq
printf 'yes\n' | ./easyrsa sign-req server serverreq
cd
