:: Update dependencies

:: make sure pip is up to date
python -m pip install --upgrade pip

:: install requirements
pip install -r C:/projects/ragan/touchdesigner/touchdesigner-hueControl/dev/dep/requirements.txt --target="%~dp0\python"