@echo off
setlocal

rem Set the path to your input file
set "input_file=D:\GeekTrust\python-pip-starter-kit\sample_input\input1.txt"

rem Run the script with input redirection
type "%input_file%" | python -m geektrust

endlocal
