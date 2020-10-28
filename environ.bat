@ECHO OFF

if NOT EXIST "%cd%\venv\" (
    ECHO Virtual Environment not found....
    ECHO Creating...
    python -m venv venv
    ECHO Installing Requirements...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ECHO DONE... starting Virtual Environment
)

"%cd%\venv\Scripts\activate.bat"