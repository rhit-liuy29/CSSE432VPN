#!/bin/bash
cd easy-rsa/
cd pki/
rm client_req.req
cd reqs/
rm clientreq.req
cd ..
cd issued/
rm clientreq.crt
