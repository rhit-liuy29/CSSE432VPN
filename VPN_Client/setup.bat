@echo off 
	
	set mypath=%cd%
	echo %mypath%
	
	if exist %mypath%\easy-rsa rmdir /s /q %mypath%\easy-rsa
	
	set easy_rsa_url='https://github.com/OpenVPN/easy-rsa/releases/download/v3.1.2/EasyRSA-3.1.2-win64.zip'
	mkdir easy-rsa 2> NUL
	
	powershell -command "curl -o ./easy-rsa/EasyRSA-3.1.2-win64.zip %easy_rsa_url%"
	powershell -command "Expand-Archive -Path ./easy-rsa/EasyRSA-3.1.2-win64.zip -DestinationPath ./easy-rsa/"
	powershell -command "del ./easy-rsa/*.zip"
	
    setlocal enableextensions disabledelayedexpansion
		
	cd easy-rsa\EasyRSA-3.1.2\bin
	
	set "search=%bin/sh"
	
	set "replace=%./easyrsa init-pki"
	
	for /f "delims=" %%x in ('powershell -command "(New-TimeSpan -Start '1/1/1970' -End (Get-Date)).TotalSeconds"') do set unixtime=%%x
	set unixtime=%unixtime:.=_%
	
	set "replace2=%./easyrsa --batch gen-req client_"

    set "textFile=easyrsa-shell-init.sh"

    for /f "delims=" %%i in ('type "%textFile%" ^& break ^> "%textFile%" ') do (
        set "line=%%i"
        setlocal enabledelayedexpansion
        >>"%textFile%" echo(!line:%search%=%replace%!
        endlocal
    )
	
	echo %replace2%%unixtime% nopass >>%textFile%
	
	cd ..
	call EasyRSA-Start.bat
	
	cd %mypath%
	
    python client.py 45.79.43.57 4455