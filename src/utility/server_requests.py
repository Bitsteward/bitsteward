#!/usr/bin/python


import requests
import json
import subprocess
import time
import os
from dotenv import load_dotenv

load_dotenv()


class Server():

    bw_server_pid = ""

    server_ready = False

    def __init__(self):
        self.load_json_data

    # load the JSON data from the BW Server
    def load_json_data(self):
        bw_location = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.bw_server_pid = subprocess.Popen([bw_location + "/bw", "serve", "--port", self.port, "--session", os.getenv("BW_SESSION")])
        

        while True:
            try:
                requests.get(f"http://{self.hostname}:{self.port}/status")
            except:
                time.sleep(0.1)

    def get_vault_items(hostname, port):
        requests.post(f"http://{hostname}:{port}/sync")
        cmdOutput = requests.get(f"http://{hostname}:{port}/list/object/items")

        jsonOutput = json.loads(cmdOutput.content)
        return jsonOutput["data"]["data"]

    def get_vault_folders(hostname, port):
        requests.post(f"http://{hostname}:{port}/sync")
        cmdOutput = requests.get(f"http://{hostname}:{port}/list/object/folders")

        jsonOutput = json.loads(cmdOutput.content)
        return jsonOutput["data"]["data"]
