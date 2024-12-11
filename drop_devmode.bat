@ECHO OFF

:START
CLS
IF [%1]==[] GOTO BLANK
PUSHD "%~dp0"
python-3.12.6.amd64\python.exe cli devmode %1
POPD
GOTO END

:BLANK
ECHO Drop Data folder into me or give it as argument
GOTO END

:END
pause
