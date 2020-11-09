@echo off

call venv\Scripts\activate.bat
fbs freeze
deactivate