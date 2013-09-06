ECHO OFF
IF NOT EXIST twistd.py copy C:\Python26\Scripts\twistd.py %CD%
IF EXIST twistd.py python twistd.py -y hub.tac
pause