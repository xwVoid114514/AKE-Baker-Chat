@echo off

set PYTHON_PATH="Python313/python.exe"

%PYTHON_PATH% -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

pause