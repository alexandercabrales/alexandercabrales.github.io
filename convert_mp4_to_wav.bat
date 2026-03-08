@echo off
setlocal
:: Full path to ffmpeg.exe
set FFMPG="C:\Users\alexc\OneDrive\Desktop\ffmpeg\ffmpeg-2025-09-28-git-0fdb5829e3-full_build\bin\ffmpeg.exe"
:: Loop through all MP4 files in the current folder
for %%A in ("*.mp4") do (
    echo Converting "%%A" ...
    %FFMPG% -i "%%A" -vn -ar 44100 -ac 2 "%%~nA.wav"
)
echo.
echo ✅ All done! Converted all MP4 files to WAV.
pause
