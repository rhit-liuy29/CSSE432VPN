#!/bin/bash
cd easy-rsa/
cd pki/
rm server_req.req
cd reqs/
rm serverreq.req
cd ..
cd issued/
rm serverreq.crt
