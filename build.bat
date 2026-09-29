@echo off
echo Installing requirements...
pip install pyinstaller

echo Building EXE...
pyinstaller --onefile --noconsole plan_creator_full.py

echo DONE!
pause
explorer dist
