import requests
from bs4 import BeautifulSoup
import json,pickle,os,sys,time
# soup = BeautifulSoup(html_doc.content, features="lxml")


def create_path(path,name):
    if not os.path.isdir(path):
        os.makedirs(path,exist_ok=True)
    return os.path.join(path,name)

def save_pkl(path,data,name):
    file_path =create_path(path,name)
    with open(file_path,"wb") as f:
        f.write(pickle.dumps(data))

def save_pic(path,url,name):
    try:
        file_path = create_path(path, name)
        if os.path.isfile(file_path):
            return
        with open(file_path,"wb") as f:
            f.write(requests.get(url).content)
        time.sleep(10)
    except Exception as e:
        print("save_pic err: ",e,file_path)

def read_pkl(path,name):
    with open(os.path.join(path,name),"rb") as f:
        return pickle.loads(f.read())