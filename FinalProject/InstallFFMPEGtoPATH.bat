:: install_ffmpeg.bat
@echo off
SETLOCAL

:: 1. Download FFmpeg release (64-bit static build)
set FF_URL=https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
set TEMP_ZIP=%TEMP%\ffmpeg.zip

echo Downloading FFmpeg...
powershell -Command "Invoke-WebRequest -Uri '%FF_URL%' -OutFile '%TEMP_ZIP%'"

:: 2. Extract to C:\ffmpeg
echo Extracting...
powershell -Command "Expand-Archive -LiteralPath '%TEMP_ZIP%' -DestinationPath 'C:\ffmpeg_temp' -Force"

:: Move the 'bin' folder to C:\ffmpeg
for /d %%D in (C:\ffmpeg_temp\ffmpeg-*-essentials_build) do (
    move "%%D" "C:\ffmpeg"
)

:: Clean up temp folder
rmdir /s /q C:\ffmpeg_temp
del /q %TEMP%\ffmpeg.zip

:: 3. Add C:\ffmpeg\bin to system PATH
setx PATH "%PATH%;C:\ffmpeg\bin"

echo FFmpeg installed and added to PATH. Please restart your terminal or IDE.

ENDLOCAL
pause