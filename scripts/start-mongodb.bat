@echo off
title MongoDB Server
cd ../astron

"mongo\Server\3.0\bin\mongod.exe" --dbpath mongo/astrondb
pause
