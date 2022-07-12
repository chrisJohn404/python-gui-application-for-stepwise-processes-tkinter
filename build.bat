
REM Build an application executable using pyinstaller
REM Author(s): Chris Johnson (chrisjohn404)
REM September 2020
REM License: GPLv2

SET cur_dir=%cd%
cd ..
SET prev_dir=%cd%
cd %cur_dir%

rm -r %cur_dir%\dist

REM Specify the absolute path Python executable.
SET python_exe=C:\Python37\python.exe
SET python_exe=C:\Users\chris\AppData\Local\Programs\Python\Python37-32\python.exe
SET python_exe=C:\Python310\python.exe

SET ICO_F=example_python_test_program.ico
SET V_FILE=version.txt
SET O_NAME=example_python_test_program.exe
SET MAIN_P=main.py

REM Specify a "-w" flag to start application in enew context/remove the console window.
REM Docs: https://pyinstaller.org/en/stable/usage.html#cmdoption-c
%python_exe% -m PyInstaller --clean --onefile --windowed -i %ICO_F% --version-file %V_FILE% -n %O_NAME% %MAIN_P%

cp %cur_dir%\tp_core\test.py %cur_dir%\dist\test.py
cp %cur_dir%\tp_core\test_runner.py %cur_dir%\dist\test_runner.py

REM Clean up generated .spec file
rm %cur_dir%\%O_NAME%.spec

rem Run Test Program
.\dist\%O_NAME%


REM ''' Author(s): Chris Johnson (chrisjohn404) September 2020'''