@echo off

for /f "delims=" %%x in (hostname.txt) do set hostname=%%x

scp -r "pi_code" %hostname%:Documents/sdc