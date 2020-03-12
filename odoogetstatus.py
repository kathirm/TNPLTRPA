import json, requests, time
starttime=time.time()

while True:
    resp = requests.get("http://10.6.7.88:8002/getCurrentstatus")
    print resp.text
    time.sleep(10 - ((time.time() - starttime) %10))

    ###   The script exection duration time ( 10 seconds )   ###









