#Created By AnteiCodes
import requests
import  os
from concurrent.futures import ThreadPoolExecutor
folder_skipping = []
import argparse
arg=argparse.ArgumentParser()
arg.add_argument('--worker', type=int, default=3, help='Deafult Worker 3')
arg.add_argument('--dest', type=str, default=os.getcwd(), help='Default Dest Path'+os.getcwd())
arg.add_argument('--url', type=str, required=True)
woke=arg.parse_args()
worker = woke.worker
dest = woke.dest.strip('/')+'/'
BASE_URL = woke.url
def createfolder(fn:str):
    tree = fn.strip('/').split('/')
    for i,n in enumerate(tree,1):
        print(dest+'/'.join(tree[:i]))
        if not os.path.isdir(dest+'/'.join(tree[:i])):
            os.mkdir(dest+'/'.join(tree[:i]))
def download(url, path):
    if os.path.isfile(path):
        return False
    req=requests.get(url,headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'},stream=True)
    with open(path, 'wb') as file:
        for iter in req.iter_content(1024):
            file.write(iter)
        print(f'{path} downloaded')
def get_items(path):
    global folder_skipping
    with ThreadPoolExecutor(max_workers=worker) as th:
        for item in requests.post(BASE_URL+'?', json={'action':'get','items':{'what':1, 'href':path}}).json()['items'][1:]:
            if item['href'][-1] == '/' and path == item['href'][:path.__len__()] and not item['href'] in folder_skipping:
                folder_skipping.append(item['href'])
                print(f'create folder {item["href"]}')
                createfolder(item['href'].strip('/'))
                get_items(item['href'])
            elif not item['href'][-1] == '/':
                print(f'downloading {BASE_URL+item["href"][1:]}')
                th.submit(download, BASE_URL+item['href'][1:],item['href'][1:])
get_items('/')