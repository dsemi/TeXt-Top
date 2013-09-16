@echo off

SET seconds=1

IF NOT "%1"=="" SET "seconds=%1"

shutdown.exe /s /t %seconds%