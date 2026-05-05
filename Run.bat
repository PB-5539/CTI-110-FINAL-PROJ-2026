@echo off
echo ------------------------------------------------------------------------------------------
echo launching Virtual Environment
echo ------------------------------------------------------------------------------------------
if not exist ".please_work\Scripts\activate.bat" (
echo Virtual Environment not found. Please open an issue on GitHub to report this problem.
echo ------------------------------------------------------------------------------------------
pause >nul
exit /b
)
cd .please_work\Scripts
call activate.bat
cd ..
cd ..
if not exist "main.py" (
echo main.py not found. did you pull the entire repo?
echo ------------------------------------------------------------------------------------------
pause >nul
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
echo done. Press any key to exit.
echo ------------------------------------------------------------------------------------------
pause >nul