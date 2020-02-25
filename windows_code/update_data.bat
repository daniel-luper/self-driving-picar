@echo off

for /f "delims=" %%x in (../hostname.txt) do set hostname=%%x

rmdir /S raw_data
scp -r %hostname%:Documents/sdc/data .
ren data raw_data
del raw_data\temp.txt