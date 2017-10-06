import requests
import json
import hashlib
import hmac
import base64
import argparse

SETTINGS = {}

def getQuestion(task):
    url = "http://192.168.204.198:6543/task/" + str(task)
    payload = {
        'user_id' : SETTINGS["user_id"]
    }
    sig = generateSig(payload)
    headers = {
        'content-type': 'application/json; charset=utf-8',
        'X-PYCON': sig
    }
    r = requests.post(url=url, data=json.dumps(payload), headers=headers)
    print('============ QUESTION ============')
    print(r.json())
    print('==================================')
    return True

def generateSig(payload):
    message = bytes(json.dumps(payload), 'utf-8')
    sig = hmac.new(bytes(SETTINGS["code"], 'utf-8'), message, hashlib.sha256).hexdigest()
    return sig

def submitAnswer(task, answer):
    url = "http://192.168.204.198:6543/task/{task}/solution".format(task=task)
    payload = {
        'user_id' : SETTINGS["user_id"],
        'solution' : answer
    }
    sig = generateSig(payload)
    headers = {
        'content-type': 'application/json; charset=utf-8',
        'X-PYCON': sig
    }
    r = requests.post(url=url, data=json.dumps(payload), headers=headers)
    print('======== ANSWER RESPONSE =========')
    print(r.json())
    print('==================================')
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, help="The question number", required=True)
    parser.add_argument("--a", type=str, help="The questions solution", required=False)
    ARGUMENTS = parser.parse_args()
    try:
        with open("settings.json") as settings_file:
            SETTINGS = json.load(settings_file)
    except:
        raise Exception("NO SETTINGS JSON FILE FOUND")

    answer = None
    if ARGUMENTS.q and ARGUMENTS.a:
        print("======= Submitting Question %s ... =========="%(ARGUMENTS.q))
        answer = submitAnswer(ARGUMENTS.q, ARGUMENTS.a)
    if ARGUMENTS.q:
        print("========== Getting Question %s ... =========="%(ARGUMENTS.q))
        answer = getQuestion(ARGUMENTS.q)
