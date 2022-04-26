
REM Build an application executable using pyinstaller

SET cur_dir=%cd%
cd ..
SET prev_dir=%cd%
cd %cur_dir%

REM Specify the absolute path Python executable.
SET python_exe=C:\Python37\python.exe
SET python_exe=C:\Users\chris\AppData\Local\Programs\Python\Python37-32\python.exe

%python_exe% -m PyInstaller --clean --onefile --nowindow -w -i example_python_test_program.ico --version-file version.txt -n example_python_test_program.exe main.py

rem PAUSE

rem Run Test Program
rem .\dist\main.exe
.\dist\example_python_test_program.exe

