rem Delete old build, in case one exists
rd /s /q build\exe.win32-2.7

rem Build the .exe
python setup.py build_exe

rem Copy important files with the binary
copy LICENSE.md build\exe.win32-2.7
copy README.md build\exe.win32-2.7
copy settings.example.py build\exe.win32-2.7
