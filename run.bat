@echo off
setlocal

rem Define paths
set venv_dir=guivenv
set requirements_file=requirements.txt
set gui_script=gui.py

rem Check if virtual environment exists
if not exist %venv_dir% (
    echo Creating virtual environment...
    python -m venv %venv_dir%
)

rem Activate the virtual environment
call %venv_dir%\Scripts\activate

rem Install requirements if not already installed
python -m pip install -r %requirements_file%

rem Run the GUI script
python %gui_script%

rem Deactivate the virtual environment
deactivate

endlocal
