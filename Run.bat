@echo off
echo ------------------------------------------------------------------------------------------
echo launching Virtual Environment
echo ------------------------------------------------------------------------------------------
cd .please_work\Scripts
call activate.bat
cd ..
cd ..
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