from blessed import Terminal
import os
import sys
import requests
from consolemenu import *
from consolemenu.items import *
import time
import zipfile
import shutil
import subprocess

def updatedetors(force=False):
    t = Terminal()
    print(t.green+"Updating Detors...")
    print("Finding latest release... ",end = "")
    r = requests.get("https://api.github.com/repos/Mauler125/detours_r5/releases/latest")
    if r.status_code != 200:
        print(t.red+"Error!")
        print("Error getting latest release: {}".format(r.status_code))
        print(t.normal)
        time.sleep(1)
        return False
    data = r.json()
    print(t.normal + data["tag_name"])
    if not force and os.path.exists("myr5_data/det_version") and data["tag_name"] == open("myr5_data/det_version").read():
        print(t.green+"Detors already up to date!")
        print(t.normal)
        time.sleep(1)
        return True
    
    #print(t.normal+"Changelog:\n"+data["body"].strip())
    print(t.green+"Downloading latest release...")
    dturl = data["assets"][0]["browser_download_url"]
    with open("myr5_data/tmp/det.zip","wb") as f:
        r = requests.get(dturl)
        f.write(r.content)
    print("Extracting content...")
    with zipfile.ZipFile("myr5_data/tmp/det.zip","r") as z:
        z.extractall("myr5_data/tmp")
    dfolder = os.path.abspath(os.path.join("myr5_data/tmp",data["name"]))
    shutil.copytree(dfolder,".",dirs_exist_ok=True)
    print("Cleaning up...")
    shutil.rmtree("myr5_data/tmp",ignore_errors=True)
    os.mkdir("myr5_data/tmp")
    with open("myr5_data/det_version","w") as fl:
        fl.write(data["tag_name"])
        
    print("Detors updated!")
    print(t.normal)
    time.sleep(1)
    return True
def updatescripts(force=False):
    t = Terminal()
    if not force:
        a = input(f"Update scripts? \n{t.red}This will erase all changes!\n(but will not erase created files)\n{t.normal}(Y/N)")
    else:
        a = "y"
    if a.upper() != "Y":
        print(t.red + "Stopping!")
        print(t.normal)
        time.sleep(1)
        return False
    print(t.green+"Updating Scripts...")
    print("Finding latest commit... ",end = t.normal)
    r = requests.get("https://api.github.com/repos/Mauler125/scripts_r5/commits")
    if r.status_code != 200:
        print(t.red+"Error!")
        print("Error getting latest commit: {}".format(r.status_code))
        print(t.normal)
        time.sleep(1)
        return False
    data = r.json()
    latestcommit = data[0]["sha"]
    print(latestcommit)
    if not force and os.path.exists("myr5_data/scripts_version") and latestcommit == open("myr5_data/scripts_version").read():
        print(t.green+"Scripts already up to date!")
        print(t.normal)
        time.sleep(1)
        return True
    print(t.green+"Downloading latest release...")
    dturl = "https://github.com/Mauler125/scripts_r5/archive/{}.zip".format(latestcommit)
    with open("myr5_data/tmp/scripts.zip","wb") as f:
        r = requests.get(dturl)
        f.write(r.content)
    print("Extracting content...")
    with zipfile.ZipFile("myr5_data/tmp/scripts.zip","r") as z:
        z.extractall("myr5_data/tmp")
    dfolder = os.path.abspath(os.path.join("myr5_data/tmp","scripts_r5-"+latestcommit))
    shutil.copytree(dfolder,"platform/scripts",dirs_exist_ok=True)
    print("Cleaning up...")
    shutil.rmtree("myr5_data/tmp",ignore_errors=True)
    os.mkdir("myr5_data/tmp")
    with open("myr5_data/scripts_version","w") as fl:
        fl.write(latestcommit)
        
    print("Scripts updated!")
    print(t.normal)
    time.sleep(1)
    return True

def launchr5(debug=False):
    print("Launching R5 ({})".format("Dev" if debug else "Retail"))
    args = ["Run R5 Reloaded.exe", "-debug" if debug else "-release"]
    subprocess.check_output(args)

def main():
    if "r5apex.exe" not in os.listdir():
        print("Error! Could not find r5apex.exe")
        sys.exit(1)
    if "myr5_data" not in os.listdir():
        os.mkdir("myr5_data")
    if "tmp" not in os.listdir("myr5_data"):
        os.mkdir("myr5_data/tmp")
    if "Run R5 Reloaded.exe" not in os.listdir():
        print("Detours not found, installing...")
        updatedetors(True)
    if "scripts" not in os.listdir("platform"):
        print("Scripts not found, installing...")
        os.mkdir("platform/scripts")
        updatescripts(True)
    menu = ConsoleMenu("R5Reloaded")
    updatemenu = ConsoleMenu("Update")
    updatemenu.append_item(FunctionItem("Update Detors", updatedetors))
    updatemenu.append_item(FunctionItem("Update Scripts", updatescripts))
    menu.append_item(FunctionItem("Launch", launchr5, [False]))
    menu.append_item(FunctionItem("Launch Dev", launchr5, [True]))
    menu.append_item(SubmenuItem("Update", updatemenu))
    menu.show()
if __name__ == '__main__':
    main()