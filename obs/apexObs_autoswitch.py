from obswebsocket import obsws, requests
import re
from time import sleep
from obswebsocket.core import exceptions

host = "localhost"
port = 4444
password = "password"
filename = 'C:/Users/ユーザー名/AppData/Local/Overwolf/Log/highlights.log'


def tail(fn, n):
    with open(fn, 'r', encoding="utf-8") as f:
        lines = f.readlines()
    return lines[-n:]


ws = obsws(host, port, password)
switch=0
try:
    ws.connect()
    while True:
        result = re.search(r'.*Match (started|ended).*', str(tail(filename, 1)))
        if result:
            if  switch==0 and result.group(1) == 'started':
                ws.call(requests.SetSceneItemProperties(item='overLay', visible=True))
                ws.call(requests.PlayPauseMedia('music', True))
                switch=1
            elif switch==1 and result.group(1) == 'ended':
                ws.call(requests.SetSceneItemProperties(item='overLay', visible=False))
                ws.call(requests.PlayPauseMedia('music', False))
                switch=0
            sleep(2)
except exceptions.ConnectionFailure as e:
    print(e)
    print("5秒後に終了")
    sleep(5)