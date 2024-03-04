@echo off

REM Check if the virtual environment exists
IF EXIST myenv (
    echo Virtual environment found. Activating it...
    REM Activate the virtual environment
    call myenv\Scripts\activate.bat
) ELSE (
    REM Create a virtual environment
    echo Virtual environment not found. Creating a new one...
    python -m venv myenv

    REM Activate the virtual environment
    echo Activating the virtual environment...
    call myenv\Scripts\activate.bat

    REM Install requirements
    echo Installing requirements...
    pip install -r requirements.txt
    
    cls
)

REM Run main.py
echo Running main.py...
echo ----------------------------------------
myenv\Scripts\python.exe main.py

REM Deactivate the virtual environment
echo ----------------------------------------
echo Deactivating the virtual environment...
call myenv\Scripts\deactivate.bat

REM Wait for enter key to exit
set /p key=Done! Press Enter to exit...
exit /b 0