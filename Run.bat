@echo off
echo ------------------------------------------------------------------------------------------
echo launching Virtual Environment
echo ------------------------------------------------------------------------------------------
if not exist ".please_work\Scripts\activate.bat" (
echo Virtual Environment not found. Running 'create_venv.bat'...
echo ------------------------------------------------------------------------------------------
call create_venv.bat
)
cd .please_work\Scripts
call activate.bat
cd ..
cd ..
if not exist "finalproject\code\main.py" (
echo main.py not found. did you pull the entire repo?
echo ------------------------------------------------------------------------------------------
pause >nul
echo press enter to close this window.
exit /b
)
echo running main.py
echo ------------------------------------------------------------------------------------------
python finalproject\code\main.py
echo closing Virtual Environment
echo ------------------------------------------------------------------------------------------
cd .please_work\Scripts
call deactivate.bat
cd ..
cd ..
echo done. Press enter to exit.
echo ------------------------------------------------------------------------------------------
pause >nul
echo press enter to close this window.