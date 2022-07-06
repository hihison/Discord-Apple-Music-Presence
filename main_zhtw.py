from pypresence import Presence
import random
import time
import hashlib
import win32com.client as wc
import pythoncom,sys
from infi.systray import SysTrayIcon
global indicator 
from urllib.request import urlopen
import urllib.parse
import json
import win32ui

#https://itunes.apple.com/search?term=Novel+Fergus+%E5%A2%9C%E8%90%BD&resultEntity=music&country=hk

indicator = True

def on_quit_callback(systray):
    #iTunesApp.Quit()
    #exit()
    #closeapp()
    global indicator 
    indicator = False
    print ('Bye, then.')
    
def checkstate(last):
    h = 0
    currentTrack = iTunesApp.CurrentTrack
    
    if (currentTrack != None):
        songName = ((iTunesApp.CurrentTrack.Name))
        status = (int(iTunesApp.PlayerState))
        songArtist = (iTunesApp.CurrentTrack.Artist)
        songAlbum = (iTunesApp.CurrentTrack.Album)
        songArtwork = (iTunesApp.CurrentTrack.Artwork)
        #print(currentTrack)

        try:
            m = hashlib.md5()
            #要計算 MD5 雜湊值的資料
            songdata = str(songName+songArtist+songAlbum+str(status)).encode("utf-8")
            # 更新 MD5 雜湊值
            m.update(songdata)

            # 取得 MD5 雜湊值
            
            h = m.hexdigest()

            
        except:
            print("No Soung")
            h = 0
        
        m = None
        #print(f"h = {h}")
        
        if(status)==1:
            status2 ="播放中"
        else:
            status2 ="暫停"
   
        if (last != h):
            
            s=time.gmtime(time.time())
            
            url = 'https://itunes.apple.com/search?term=' + urllib.parse.quote_plus(songArtist)+'-'+urllib.parse.quote_plus(songName)+'-'+urllib.parse.quote_plus(songAlbum)+'&resultEntity=music&country=hk'
            response = urlopen(url)
            data_json = json.loads(response.read())
            try:
                art30 = data_json["results"][0]["artworkUrl30"]
                art512 = art30.replace("30x30bb.jpg", "100x100bb.jpg")
                collectionViewUrl = data_json["results"][0]["collectionViewUrl"]
            except:
                art30 = "test.jpg"
                art512 = art30.replace("30x30bb.jpg", "100x100bb.jpg")
                collectionViewUrl = "google.com"
                
            if len(collectionViewUrl) >=33   :
                collectionViewUrl = "google.com"
            
            RPC.update(
                #buttons=[{"label": status2, "url": "http://google.com"}, {'label': songAlbum, "url": collectionViewUrl}],
                
                state = f' {songName}', details=f'{songArtist}',
                large_image=art512, large_text="iTunes Playing", small_image='https://media0.giphy.com/media/2JRUiWjV3kkQi4v74y/giphy.gif?cid=ecf05e47tsaxy3kazef7n0fnthiwgtlm0zqcn7fi9ar5s129&rid=giphy.gif&ct=s', small_text='Python 3.10',
                start=start_time)

    else:
        RPC.update(state="狀態", details="DETAILS HERE", large_image="https://img-07.stickers.cloud/packs/67665596-9ef6-4037-a654-f0f5170912cc/webp/21d03efa-71f9-4dd2-b1b2-87d7d9737fc6.webp", small_image="NAME OF SMALL IMAGE HERE", large_text="LARGE IMAGE TEXT HERE", start=start_time)  # Set the presence

    return h



print("==========================================")

print("Discord Apple Music Presence by hihison V1.01z")
print("https://siu4.me")
print("==========================================")



try:
    print("Waiting for Discord...")

    client_id = '0000000000000' #Put your client ID here
    RPC = Presence(client_id) 
    RPC.connect() 

    print("Waiting for iTunes...")


    try:
        iTunesApp = wc.GetActiveObject("iTunes.Application")
    except:
        iTunesApp = wc.Dispatch("iTunes.Application")
    
except:
    print("Discord is not running")
    win32ui.MessageBox("Discord is not running", "Error")
    exit()

songName    = None
status      = None
songArtist  = None
songAlbum   = None
songArtwork = None
status2 = None

last = 0 
quotes = [
    'Bot Developer',
    'Designer',
    'Linux User',
    'Valorant Gamer'
]

start_time=time.time()

print("Initialization Complete!")

#menu_options = (("Disable", None, disable),)

systray = SysTrayIcon("icon.ico", "AppleMusic Discord Watcher",on_quit=on_quit_callback)
systray.start()

def opena():
    global last
    while True:
        try:
            last = checkstate(last)
            print(last)
        except:
            print("Too Fast, Fuck You!")
        #print(last)
        #print(f"last = {last}")
        #print(last)
        #print(indicator)
           
        if indicator==False:
            print("Stopped")
            break
        time.sleep(1)   
        

opena()