import subprocess

td_python = f"{app.installFolder}/bin/python.exe"
python_program = f"{project.folder}/td-modules/base_hueControl/tdHueBridge.py"
address = op("udpout1").par.address.eval()
port = f'{op("udpout1").par.port.eval()}'
command_list = [td_python, python_program, '-a', address, '-p', port]

subprocess.Popen(command_list, shell=False)
