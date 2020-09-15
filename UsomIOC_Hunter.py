import requests
import urllib3
import sys
import os
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style, init

urllib3.disable_warnings()

def isThereFile():
    fileName = "Usom_IP_Feeds.csv"
    if os.path.isfile(fileName) == False:
        f= open(fileName,"w+")
        f.close()

    fileName = "Usom_Domain_Feeds.csv" 
    if os.path.isfile(fileName) == False:
        f= open(fileName,"w+")
        f.close()

def validIPAddress(Feed_Value):
    def isIPv4(s):
        try: return str(int(s)) == s and 0 <= int(s) <= 255
        except: return False
    def isIPv6(s):
        if len(s) > 4:
            return False
        try : return int(s, 16) >= 0 and s[0] != '-'
        except:
            return False
    if Feed_Value.count(".") == 3 and all(isIPv4(i) for i in Feed_Value.split(".")) or Feed_Value.count(":") == 7 and all(isIPv6(i) for i in Feed_Value.split(":")):
        return "IP"
    return "Neither"


def writeCSV(Feed_Date,Feed_ID,Feed_Source,Feed_Description,Feed_Value):

    valueType = validIPAddress(Feed_Value)
    if valueType == "IP":
        fileName = "Usom_IP_Feeds.csv"
    else:
        fileName = "Usom_Domain_Feeds.csv"

    datas = Feed_ID + " " + Feed_Value
    
    dup = isDuplicate(fileName,Feed_ID)
    
    if dup == "NoDuplicate":   
        with open(fileName,"r",encoding="utf-8") as f:
            if Feed_ID in f.read():       # Duplicate controls
                print("\n\n ===== > Feed Updates Completed")
                sys.exit()
            else:   #write file
                with open(fileName,"a",encoding="utf-8") as w:   #open file
                    print("New Feed : Date : {} | ID : {} | Source: {} | Description : {} | Feed : {}".format(Feed_Date,Feed_ID,Feed_Source,Feed_Description,Feed_Value))
                    w.write(datas+"\n")     # write csv

          
def GetFeeds():
    p = 1
    while True:       
        url = "https://usom.gov.tr/zararli-baglantilar/"+ str(p) +".html"
        r = requests.get(url, verify=False)

        if r.status_code == 200:
            source = BeautifulSoup(r.content,"lxml")
            context = source.find_all("tr",attrs={"align":"center"})           
            for i in range (0,len(context)):

                Feed = context[i].find_all("td")
                Feed_ID = Feed[0].text
                Feed_Value = Feed[1].text
                Feed_Description = Feed[2].text
                Feed_Source = Feed[3].text
                Feed_Date = Feed[4].text
                  
                writeCSV(Feed_Date,Feed_ID,Feed_Source,Feed_Description,Feed_Value)
            p += 1
        else:
            print("\n\n ===== > Feed Collection Finished")
            break
            
def isDuplicate(fileName,Feed_ID):
    with open(fileName,"r",encoding="utf-8") as fp:
        line = fp.readline()
        cnt = 1
        while line:
            if Feed_ID == line.strip().split(" ")[0]:
                print("\n\n ===== > Feed Updates Completed")
                sys.exit()
            else:
                line = fp.readline()
                cnt += 1
    return "NoDuplicate"
    

if __name__ == "__main__":
    init(autoreset=True)
    print(Fore.RED +"\n############################################################################")
    print("""
         _    _                       ______            _           
        | |  | |                     |  ____|          | |          
        | |  | |___  ___  _ __ ___   | |__ ___  ___  __| | ___ _ __ 
        | |  | / __|/ _ \| '_ ` _ \  |  __/ _ \/ _ \/ _` |/ _ \ '__|
        | |__| \__ \ (_) | | | | | | | | |  __/  __/ (_| |  __/ |   
         \____/|___/\___/|_| |_| |_| |_|  \___|\___|\__,_|\___|_|   
    """)
    print(Fore.RED +"\n############################ Author : Ali Haydar TOPRAK ####################")                                                         
    isThereFile()                                       
    GetFeeds()

    