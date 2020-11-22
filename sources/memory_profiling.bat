@echo off
echo Begin of profiling
del logs\memory-profile.log /f /q
mprof run --include-children -o logs/memory-profile.log --interval 0.05 python main.py
mprof plot --output logs/memory-profile.png logs/memory-profile.log
echo End of profiling
pause