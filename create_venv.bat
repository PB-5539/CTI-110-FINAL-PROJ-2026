@echo off
echo ------------------------------------------------------------------------------------------
echo creating Virtual Environment
echo ------------------------------------------------------------------------------------------
if exist ".please_work\Scripts\activate.bat" (
echo Virtual Environment already exists. checking dependencies...
echo ------------------------------------------------------------------------------------------
)
if not exist ".please_work\Scripts\activate.bat" (
python313 -m venv .please_work)
if not exist ".please_work\Scripts\activate.bat" (
echo Failed to create Virtual Environment. Please open an issue on GitHub to report this problem.
echo ------------------------------------------------------------------------------------------
pause >nul
exit /b
)
echo Virtual Environment created successfully.
echo ------------------------------------------------------------------------------------------
echo Installing dependencies...
python.exe -m pip install --upgrade pip
if exist "finalproject\requirements.txt" (
@echo on
pip install -r finalproject\requirements.txt
@echo off
echo Dependencies installed successfully.
echo ------------------------------------------------------------------------------------------
pause >nul
exit /b)
if not exist "finalproject\requirements.txt" (
echo requirements.txt not found. Please open an issue on GitHub to report this problem.
echo ------------------------------------------------------------------------------------------
pause >nul
exit /b
)