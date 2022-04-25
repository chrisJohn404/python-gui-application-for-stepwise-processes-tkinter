REM py -3.7 -m py2exe.build_exe hello.py

REM This script builds the ESP32 testing.exe executable using pyinstaller and puts it in a zip file.
REM Files are in the dist folder.
REM Building with 64-bit Python 3.7.

SET cur_dir=%cd%
cd ..
SET prev_dir=%cd%
cd %cur_dir%

REM Specify the absolute paht Python executable.
SET python_exe=C:\Python37\python.exe
SET python_exe=C:\Users\chris\AppData\Local\Programs\Python\Python37-32\python.exe

%python_exe% -m PyInstaller --clean --onefile --nowindow -w -i example_python_test_program.ico --version-file version.txt -n example_python_test_program.exe main.py

rem PAUSE

rem Run Test Program
rem .\dist\main.exe
.\dist\example_python_test_program.exe

