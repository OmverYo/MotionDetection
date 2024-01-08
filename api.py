import requests
import json

def gamedata_api(path, method, variable):
    API_HOST = "http://localhost:8080/api"

    value = variable

    body = None

    headers = {
        "Content-Type": "application/json", "charset": "UTF-8", "Accept": "*/*"
    }

    if path == "/GameData":
        gameBody = {
            "play_id": 0,
            "capture_time": value[0],
            "accuracy": value[1],
            "content_url": value[2]
        }
        body = gameBody

    elif path == "/PlayerData":
        playerBody = {
            "play_id": 0,
            "total": value[0],
            "perfect_frame": value[1],
            "awesome_frame": value[2],
            "good_frame": value[3],
            "ok_frame": value[4],
            "bad_frame": value[5]
        }
        body = playerBody

    elif path == "/BackgroundData":
        backgroundBody = {
            "user_id": 0,
            "is_vr": 1,
            "bg_name": "",
            "coord_name": ""
        }
        body = backgroundBody

    elif path == "/ProgramData":
        programBody = {
            "program_id": 0,
            "is_running": value
        }
        body = programBody

    elif path == "/HandData":
        handBody = {
            "hand_id": 1,
            "rx": value[0],
            "ry": value[1],
            "lx": value[2],
            "ly": value[3]
        }
        body = handBody

    elif path == "/HandData/1":
        handBody = {
            "hand_id": 1,
            "rx": value[0],
            "ry": value[1],
            "lx": value[2],
            "ly": value[3]
        }
        body = handBody

    elif path == "/BasicData":
        basicBody = {
            "play_id": 0,
            "reaction_time": value[0],
            "on_air": value[1],
            "squat_jump": value[2],
            "knee_punch": value[3],
            "balance_test": value[4],
            "content_url": value[5],
            "content_name": value[6]
        }
        body = basicBody
    
    elif path == "/Recommend":
        recommendBody = {
            "user_id": 0,
            "content_url": value[0],
            "content_name": value[1]
        }
        body = recommendBody
    
    url = API_HOST + path

    try:
        global response
        response = None
        
        if method == "GET":
            response = requests.get(url, headers=headers)

            return response.text
        
        elif method == "POST":
            response = requests.post(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t"))

        elif method == "DELETE":
            response = requests.delete(url, headers=headers)

        elif method == "PUT":
            response = requests.put(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t"))
    
    except Exception as ex:
        print(ex)