#!/usr/bin/python


import requests
import json
import subprocess
import time
import os
from dotenv import load_dotenv

load_dotenv()

hostname = "localhost"
port = "8055"


bw_location = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
bw_password = os.getenv("BW_PASSWORD")

class Server():

    

    def get_vault_items():
        p = subprocess.Popen([bw_location + '/bw', "list", "items"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, _ = p.communicate(input=bw_password.encode())
        output = output.decode()

        jsonOutput = json.loads(output)
        return jsonOutput

    def get_vault_folders():
        subprocess.Popen([bw_location + '/bw', "sync"])
        p = subprocess.Popen([bw_location + '/bw', "list", "folders"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, _ = p.communicate(input=bw_password.encode())
        output = output.decode()

        jsonOutput = json.loads(output)
        return jsonOutput

    def get_item_by_id(id):
        p = subprocess.Popen([bw_location + '/bw', "get", "item", id], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, _ = p.communicate(input=bw_password.encode())
        output = output.decode()

        jsonOutput = json.loads(output)
        return jsonOutput