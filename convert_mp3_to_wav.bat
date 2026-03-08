@echo off
setlocal
:: Full path to ffmpeg.exe
set FFMPG="C:\Users\alexc\OneDrive\Desktop\ffmpeg\ffmpeg-2025-09-28-git-0fdb5829e3-full_build\bin\ffmpeg.exe"
:: Loop through all MP3 files in the current folder
for %%A in ("*.mp3") do (
    echo Converting "%%A" ...
    %FFMPG% -i "%%A" -ar 44100 -ac 2 "%%~nA.wav"
)
echo.
echo ✅ All done! Converted all MP3 files to WAV.
pause
