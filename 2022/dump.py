#!/usr/bin/env python3
import os
import json
import requests
from urllib.parse import urljoin
import sys
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

cookies = {
    'allow_ranking': 'Y',
}

headers = {
    'authority': 'ranking.nhspc.cc',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'zh-TW,zh;q=0.8',
    'cache-control': 'max-age=0',
    # 'cookie': 'allow_ranking=Y',
    # 'if-modified-since': 'Sun, 04 Dec 2022 02:39:04 GMT',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}

if len(sys.argv)<=1:
    print("Usage: cmsRankingDump.py URL")
    exit(0)
BaseURL = sys.argv[1]
SavePath = "ranking"
if len(sys.argv)>=3:
    SavePath = sys.argv[2]

def dumpdata(path, jsondecode=True, save=True, alt=''):
    url = urljoin(BaseURL,path)
    try:
        res = requests.get(url, stream=True, verify=False, cookies=cookies, headers=headers)
        while res.status_code != 200:
            print("[Warning] Response status is %d instead of 200 while dumping \"%s\""%(res.status_code,url))
            return None
    except:
        print("[Warning] 1st Request error while dumping %s"%path)
        try:
            res = requests.get(url, stream=True, verify=False, cookies=cookies, headers=headers)
        except:
            print("[Warning] 2nd Request error while dumping %s"%path)
            try:
                res = requests.get(url, stream=True, verify=False, cookies=cookies, headers=headers)
            except:
                print("[Warning] 3rd Request error while dumping %s"%path)
                return None
    if save:
        if (alt == ''): alt = path
        with open(alt,"wb") as f:
            f.write(res.content)
    if jsondecode:
        return json.loads(res.text)
    else:
        return res.text

def dumpdata_dir(path,jsondecode=True):
    data = dumpdata(path,jsondecode,False)
    if data == None:
        return None
    try:
        os.mkdir(path)
    except:
        pass
    open(os.path.join(path,"index.json"),"w").write(json.dumps(data))
    open(os.path.join(path,".htaccess"),"w").write("DirectoryIndex index.json")
    return data

try:
    os.mkdir(SavePath)
except:
    pass
os.chdir(SavePath)
try:
    os.mkdir("lib")
    os.mkdir("img")
except:
    pass

contests = dumpdata_dir("contests/")
if contests is None:
    exit(0)
print('Finished contests/index.json')

tasks = dumpdata_dir("tasks/")
if tasks is None:
    exit(0)
print('Finished tasks/index.json')

teams = dumpdata_dir("teams/")
if teams is None:
    exit(0)
print('Finished teams/index.json')

users = dumpdata_dir("users/")
if users is None:
    exit(0)
print('Finished users/index.json')

subchanges = dumpdata_dir("subchanges/")
if subchanges is None:
    exit(0)
print('Finished subchanges/index.json')

submissions = dumpdata_dir("submissions/")
if submissions is None:
    exit(0)
print('Finished submissions/index.json')

dumpdata("history");
print('Finished history')

dumpdata("scores");
print('Finished scores')

dumpdata("img/close.png",False);
dumpdata("img/face.png",False);
dumpdata("img/favicon.ico",False);
dumpdata("img/flag.png",False);
dumpdata("img/logo.png",False);
dumpdata("img/tick_black.png",False);
dumpdata("img/tick_white.png",False);
dumpdata("lib/eventsource.js",False);
dumpdata("lib/explorercanvas.js",False);
dumpdata("lib/jquery.js",False);
dumpdata("lib/raphael.js",False);
dumpdata("Chart.js",False);
dumpdata("Config.js",False);
dumpdata("DataStore.js",False);
dumpdata("HistoryStore.js",False);
dumpdata("Overview.js",False);
dumpdata("Ranking.css",False);
dumpdata("Ranking.html",False,alt="index.html");
dumpdata("Ranking.js",False);
dumpdata("Scoreboard.js",False);
dumpdata("TeamSearch.js",False);
dumpdata("TimeView.js",False);
dumpdata("UserDetail.js",False);
dumpdata("logo",False);
# dumpdata("events");

try:
    os.mkdir("sublist")
except:
    pass
for u in users:
    dumpdata(os.path.join("sublist",u))
print('Finished sublist/*')

try:
    os.mkdir("flags")
except:
    pass
for t in teams:
    dumpdata(os.path.join("flags",t),False)
print('Finished flags/*')

for c in contests:
    with open('contests/' + c, 'w') as f:
        json.dump(contests[c], f, indent = 4)
print('Finished contests/*')

for t in tasks:
    with open('tasks/' + t, 'w') as f:
        json.dump(tasks[t], f, indent = 4)
print('Finished tasks/*')

for t in teams:
    with open('teams/' + t, 'w') as f:
        json.dump(teams[t], f, indent = 4)
print('Finished teams/*')

for u in users:
    with open('users/' + u, 'w') as f:
        json.dump(users[u], f, indent = 4)
print('Finished users/*')

# for s in subchanges:
    # with open('subchanges/' + s, 'w') as f:
        # json.dump(subchanges[s], f, indent = 4)
# print('Finished subchanges/*')

# for s in submissions:
    # with open('submissions/' + s, 'w') as f:
        # json.dump(submissions[s], f, indent = 4)
# print('Finished submissions/*')

print('Finished *')
