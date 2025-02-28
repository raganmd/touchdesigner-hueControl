import argparse
import socket
import json
import datetime
import requests
import urllib3

# create arg parser for CLI args
parser = argparse.ArgumentParser()

# add arg for address
parser.add_argument(
    "-a", type=str,
    default='localhost',
    help="the ip address for communication")

# add arg for port
parser.add_argument(
    "-p",
    type=int,
    default=5005,
    help="the port for communication")

# pars args
args = parser.parse_args()

udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_client.bind((args.a, args.p))

urllib3.disable_warnings()

start_up_banner = '''
 _________    __ ____  ______
/_  __/ _ \  / // / / / / __/
 / / / // / / _  / /_/ / _/  
/_/ /____/ /_//_/\____/___/ 
'''


def msg_to_dict(msg: bytes) -> dict:
    """Converts incoming bytes message to python dictionary
    """
    return json.loads(msg.decode(encoding="utf-8"))


def get_now() -> datetime.datetime:
    """Returns current datetime.datetime.now() for timestamp
    """
    return datetime.datetime.now()


def log_msg(payload: dict) -> None:
    """Displays a log message
    """
    log_test = payload.get("text")
    output_msg = f'{get_now()} | {log_test}'
    print(output_msg)


def update_single_light(payload: dict) -> None:

    output_msg = f'{get_now()} | updating {payload.get("light_url")}'
    update_request = requests.put(
        payload.get("light_url"),
        headers=payload.get("headers"),
        data=json.dumps(payload.get("data")),
        verify=payload.get("verify"))
    print(output_msg)


def quit_python(payload: dict) -> None:
    """Quits python shell application
    """
    quit()


def parse_msg(msg: dict) -> None:
    command_map = {
        "log": log_msg,
        "quit": quit_python,
        "update_single_light": update_single_light
    }

    try:
        command_func = command_map.get(msg.get("command"))
        command_func(msg.get("payload"))
    except Exception as e:
        output_msg = f'{get_now()} | {e}'
        print(output_msg)


print(start_up_banner)
print("\nSTARTING TouchDesigner -> Hue Python Bridge\n")
print(f"listening on {args.a} {args.p}\n")

while True:
    data, addr = udp_client.recvfrom(1024)
    msg_dict = msg_to_dict(data)
    parse_msg(msg_dict)
