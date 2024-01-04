import requests
import json
import mysql.connector
import pymysql
from sshtunnel import SSHTunnelForwarder

mydb = mysql.connector.connect(host = "db-kl7j1.vpc-cdb.ntruss.com", port=3306, user = "mp_admin", password = "humanf1002~", database = "metaports")

if mydb:
    print("Yes")

else:
    print("No")

mycursor = mydb.cursor()

def gamedata_api(path, method):
    API_HOST = "http://localhost:8080/api"

    url = API_HOST + path

    headers = {
        "Content-Type": "application/json", "charset": "UTF-8", "Accept": "*/*"
    }
    
    gameBody = {
        "play_id": 0,
        "capture_time": 1,
        "accuracy": 0
    }

    playerBody = {
        "play_id": 0,
        "total": 0,
        "perfect_frame": 0,
        "awesome_frame": 0,
        "good_frame": 0,
        "ok_frame": 0,
        "bad_frame": 0
    }
    
    backgroundBody = {
        "user_id": 0,
        "is_vr": 1,
        "bg_name": "",
        "coord_name": ""
    }

    programBody = {
        "program_id": 0,
	    "is_running": 1
    }

    handBody = {
        "hand_id": 1,
        "rx": 0,
        "ry": 0,
        "lx": 0,
        "ly": 0
    }

    if path == "/GameData":
        body = gameBody

    elif path == "/PlayerData":
        body = playerBody

    elif path == "/BackgroundData":
        body = backgroundBody

    elif path == "/ProgramData":
        body = programBody

    elif path == "/HandData":
        body == handBody

    try:
        if method == "GET":
            response = requests.get(url, headers = headers)
        
        elif method == "POST":
            response = requests.post(url, headers = headers, data = json.dumps(body, ensure_ascii = False, indent = "\t"))
        
        print("response status %r" % response.status_code)
        print("response text %r" % response.text)
    
    except Exception as ex:
        print(ex)